# REF-002: Training Tracking Integration Design

**Version:** 1.0 | **Owner:** System Architect | **Review Date:** 2026-12-08

---

## Purpose

This reference document outlines the architectural design for integrating Adobe Captivate SCORM training modules with the Triple Screen trading system, enabling operator training completion tracking, compliance audit trails, and enforced training prerequisites.

---

## Architecture Overview

### Components

1. **Training Content**: Adobe Captivate courses exported as HTML5/SCORM
2. **Database Layer**: PostgreSQL `training_completions` table in `supertrader_portfolio`
3. **API Endpoint**: FastAPI endpoint to receive completion events
4. **Dashboard Integration**: Streamlit "Training Records" page for compliance monitoring
5. **Access Control**: Training prerequisites enforced before system access

### Data Flow

```
Captivate Course (Browser)
    |
    | [Completion Event via JavaScript API]
    |
    v
FastAPI Endpoint (/api/training/complete)
    |
    | [Validate & Store]
    |
    v
PostgreSQL (training_completions table)
    |
    | [Query for Dashboard]
    |
    v
Streamlit Dashboard (Training Records Page)
```

---

## Database Schema

### Table: `training_completions`

Add to `supertrader_portfolio` database:

```sql
CREATE TABLE training_completions (
    id SERIAL PRIMARY KEY,
    operator_name VARCHAR(100) NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    course_title VARCHAR(200) NOT NULL,
    completed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    score DECIMAL(5,2),  -- Percentage score (0-100)
    time_spent_minutes INTEGER,  -- Total time in course
    passing_score DECIMAL(5,2),  -- Required passing score
    status VARCHAR(20) NOT NULL CHECK (status IN ('passed', 'failed', 'completed')),

    -- Audit fields
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(100),

    -- Constraints
    CONSTRAINT unique_completion UNIQUE (operator_name, course_id, completed_at)
);

-- Indexes for common queries
CREATE INDEX idx_operator_completions ON training_completions(operator_name, completed_at DESC);
CREATE INDEX idx_course_completions ON training_completions(course_id, completed_at DESC);
CREATE INDEX idx_completion_status ON training_completions(status, completed_at DESC);
```

### Table: `training_courses`

Course catalog metadata:

```sql
CREATE TABLE training_courses (
    course_id VARCHAR(50) PRIMARY KEY,
    course_title VARCHAR(200) NOT NULL,
    course_version VARCHAR(20) NOT NULL,
    description TEXT,
    duration_minutes INTEGER,
    passing_score DECIMAL(5,2) DEFAULT 80.00,
    is_mandatory BOOLEAN DEFAULT FALSE,
    prerequisite_course_ids VARCHAR(50)[],  -- Array of required course IDs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Example courses
INSERT INTO training_courses (course_id, course_title, course_version, description, duration_minutes, is_mandatory) VALUES
('SOP-001-TRAINING', 'VPS Service Management Training', '1.0', 'Hands-on training for SOP-001 procedures', 30, TRUE),
('SOP-002-TRAINING', 'Log Monitoring & Troubleshooting', '1.0', 'Interactive training for system monitoring', 25, TRUE),
('SOP-003-TRAINING', 'Database Access & Queries', '1.0', 'PostgreSQL access and data quality checks', 40, TRUE),
('INTRO-TRIPLE-SCREEN', 'Introduction to Triple Screen Trading', '1.0', 'Overview of Elder\'s Triple Screen methodology', 60, TRUE);
```

### Table: `operator_training_status`

Track operator progress and access permissions:

```sql
CREATE TABLE operator_training_status (
    operator_name VARCHAR(100) PRIMARY KEY,
    all_mandatory_complete BOOLEAN DEFAULT FALSE,
    last_training_date TIMESTAMP,
    system_access_granted BOOLEAN DEFAULT FALSE,
    access_granted_at TIMESTAMP,
    access_granted_by VARCHAR(100),
    notes TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## API Endpoint Design

### Endpoint: POST /api/training/complete

**Purpose:** Receive training completion events from Captivate courses

**Request Body:**
```json
{
  "operator_name": "John Smith",
  "course_id": "SOP-001-TRAINING",
  "score": 95.5,
  "time_spent_minutes": 32,
  "status": "passed",
  "session_id": "abc123def456"
}
```

**Response (Success):**
```json
{
  "success": true,
  "completion_id": 42,
  "message": "Training completion recorded",
  "all_mandatory_complete": false,
  "remaining_courses": ["SOP-002-TRAINING", "SOP-003-TRAINING"]
}
```

**Response (Failure):**
```json
{
  "success": false,
  "error": "Invalid course_id or operator_name"
}
```

**Implementation (FastAPI):**

```python
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/training", tags=["training"])

class TrainingCompletion(BaseModel):
    operator_name: str = Field(..., min_length=1, max_length=100)
    course_id: str = Field(..., min_length=1, max_length=50)
    score: Optional[Decimal] = Field(None, ge=0, le=100)
    time_spent_minutes: Optional[int] = Field(None, ge=0)
    status: str = Field(..., pattern="^(passed|failed|completed)$")
    session_id: Optional[str] = Field(None, max_length=100)

@router.post("/complete")
async def record_training_completion(
    completion: TrainingCompletion,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Record training course completion from Captivate module.

    Validates course exists, stores completion, and checks if all
    mandatory training is complete for operator.
    """

    # Validate course exists
    course = db.query(TrainingCourse).filter_by(
        course_id=completion.course_id,
        is_active=True
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check passing score
    if completion.score is not None and course.passing_score is not None:
        if completion.score < course.passing_score:
            completion.status = "failed"
        else:
            completion.status = "passed"

    # Create completion record
    completion_record = TrainingCompletionModel(
        operator_name=completion.operator_name,
        course_id=completion.course_id,
        course_title=course.course_title,
        completed_at=datetime.utcnow(),
        score=completion.score,
        time_spent_minutes=completion.time_spent_minutes,
        passing_score=course.passing_score,
        status=completion.status,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        session_id=completion.session_id
    )

    db.add(completion_record)
    db.commit()
    db.refresh(completion_record)

    # Check if all mandatory training complete
    mandatory_courses = db.query(TrainingCourse).filter_by(
        is_mandatory=True,
        is_active=True
    ).all()

    completed_mandatory = db.query(TrainingCompletionModel).filter(
        TrainingCompletionModel.operator_name == completion.operator_name,
        TrainingCompletionModel.status == "passed",
        TrainingCompletionModel.course_id.in_([c.course_id for c in mandatory_courses])
    ).distinct(TrainingCompletionModel.course_id).all()

    all_complete = len(completed_mandatory) == len(mandatory_courses)
    remaining = [c.course_id for c in mandatory_courses
                 if c.course_id not in [comp.course_id for comp in completed_mandatory]]

    # Update operator status
    operator_status = db.query(OperatorTrainingStatus).filter_by(
        operator_name=completion.operator_name
    ).first()

    if not operator_status:
        operator_status = OperatorTrainingStatus(
            operator_name=completion.operator_name
        )
        db.add(operator_status)

    operator_status.all_mandatory_complete = all_complete
    operator_status.last_training_date = datetime.utcnow()
    operator_status.updated_at = datetime.utcnow()
    db.commit()

    return {
        "success": True,
        "completion_id": completion_record.id,
        "message": "Training completion recorded",
        "all_mandatory_complete": all_complete,
        "remaining_courses": remaining
    }
```

---

## Captivate Integration

### JavaScript API Call

Add to Captivate course's "On Course Complete" advanced action:

```javascript
// Execute JavaScript to send completion data
function sendCompletionToAPI() {
    const completionData = {
        operator_name: cpCmndGotoSlide.cpInfoCurrentSlide.m_VarHandle.mvarpUserName.m_variableValue,
        course_id: "SOP-001-TRAINING",
        score: cpInfoPercentage,  // Built-in Captivate variable
        time_spent_minutes: Math.round(cpInfoElapsedTimeMS / 60000),
        status: (cpInfoPercentage >= 80) ? "passed" : "failed",
        session_id: generateSessionId()
    };

    fetch('https://your-vps-hostname.com/api/training/complete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(completionData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.all_mandatory_complete) {
                alert('Congratulations! You have completed all mandatory training.');
            } else {
                alert('Training recorded. Remaining courses: ' + data.remaining_courses.join(', '));
            }
        } else {
            alert('Error recording completion: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to record training completion. Please contact administrator.');
    });
}

function generateSessionId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Execute on course completion
sendCompletionToAPI();
```

### Captivate Variables to Capture

| Variable | Description | Captivate Built-in |
|----------|-------------|--------------------|
| `cpInfoCurrentSlide.m_VarHandle.mvarpUserName.m_variableValue` | User name (captured at start) | Custom |
| `cpInfoPercentage` | Quiz score percentage | Built-in |
| `cpInfoElapsedTimeMS` | Time spent in milliseconds | Built-in |
| `cpQuizInfoPassFail` | Pass/Fail status | Built-in |
| `cpInfoAttempts` | Number of attempts | Built-in |

---

## Dashboard Integration

### Streamlit Page: Training Records

**File:** `backend/dashboard/pages/Training_Records.py`

```python
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

st.set_page_config(page_title="Training Records", page_icon="🎓", layout="wide")
st.title("🎓 Training Records & Compliance")

# Database connection
engine = create_engine("postgresql://triple_screen:password@localhost/supertrader_portfolio")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["Operator Progress", "Course Completions", "Compliance Report"])

with tab1:
    st.header("Operator Training Progress")

    # Query operator status
    operator_status = pd.read_sql("""
        SELECT
            ots.operator_name,
            ots.all_mandatory_complete,
            ots.last_training_date,
            ots.system_access_granted,
            COUNT(DISTINCT tc.course_id) as courses_completed,
            STRING_AGG(DISTINCT tc.course_id, ', ') as completed_courses
        FROM operator_training_status ots
        LEFT JOIN training_completions tc ON tc.operator_name = ots.operator_name
            AND tc.status = 'passed'
        GROUP BY ots.operator_name, ots.all_mandatory_complete,
                 ots.last_training_date, ots.system_access_granted
        ORDER BY ots.all_mandatory_complete DESC, ots.operator_name
    """, engine)

    st.dataframe(operator_status, use_container_width=True)

with tab2:
    st.header("Recent Course Completions")

    # Date filter
    days_back = st.slider("Show completions from last N days", 7, 90, 30)

    completions = pd.read_sql(f"""
        SELECT
            tc.completed_at,
            tc.operator_name,
            tc.course_title,
            tc.score,
            tc.time_spent_minutes,
            tc.status
        FROM training_completions tc
        WHERE tc.completed_at >= CURRENT_DATE - INTERVAL '{days_back} days'
        ORDER BY tc.completed_at DESC
    """, engine)

    st.dataframe(completions, use_container_width=True)

with tab3:
    st.header("Compliance Report")

    # Mandatory training completion rates
    compliance = pd.read_sql("""
        SELECT
            tc_course.course_title,
            COUNT(DISTINCT tc_comp.operator_name) as operators_completed,
            ROUND(COUNT(DISTINCT tc_comp.operator_name) * 100.0 /
                  (SELECT COUNT(*) FROM operator_training_status), 2) as completion_rate
        FROM training_courses tc_course
        LEFT JOIN training_completions tc_comp
            ON tc_comp.course_id = tc_course.course_id
            AND tc_comp.status = 'passed'
        WHERE tc_course.is_mandatory = TRUE
        GROUP BY tc_course.course_title
        ORDER BY completion_rate DESC
    """, engine)

    st.dataframe(compliance, use_container_width=True)

    # Generate downloadable report
    if st.button("Export Compliance Report (CSV)"):
        csv = compliance.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"training_compliance_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
```

---

## Access Control Enforcement

### Prerequisite Check Before System Access

**Use Case:** Operator must complete all mandatory training before accessing VPS or dashboard.

**Implementation Options:**

#### Option 1: Dashboard Login Gate

Add to `backend/dashboard/Home.py`:

```python
def check_operator_training(operator_name: str) -> dict:
    """Check if operator has completed mandatory training."""

    result = db.query(OperatorTrainingStatus).filter_by(
        operator_name=operator_name
    ).first()

    if not result or not result.all_mandatory_complete:
        return {
            "access_granted": False,
            "message": "You must complete all mandatory training before accessing the system.",
            "pending_courses": get_pending_mandatory_courses(operator_name)
        }

    return {"access_granted": True}

# In main dashboard
if not st.session_state.get("authenticated"):
    operator_name = st.text_input("Operator Name")

    if st.button("Login"):
        training_status = check_operator_training(operator_name)

        if not training_status["access_granted"]:
            st.error(training_status["message"])
            st.warning("Pending courses:")
            for course in training_status["pending_courses"]:
                st.write(f"- {course}")
        else:
            st.session_state.authenticated = True
            st.session_state.operator_name = operator_name
            st.rerun()
```

#### Option 2: VPS SSH Access Control

Add to VPS SSH authorized_keys with command restriction:

```bash
# /home/triple-screen/.ssh/authorized_keys
command="/usr/local/bin/check_training.sh john_smith" ssh-rsa AAAAB3... john_smith@workstation
```

**Script:** `/usr/local/bin/check_training.sh`

```bash
#!/bin/bash
OPERATOR_NAME=$1

# Query database for training status
TRAINING_COMPLETE=$(psql -U triple_screen -d supertrader_portfolio -tAc \
  "SELECT all_mandatory_complete FROM operator_training_status WHERE operator_name = '$OPERATOR_NAME'")

if [ "$TRAINING_COMPLETE" != "t" ]; then
    echo "ACCESS DENIED: Mandatory training not complete."
    echo "Please complete all required training modules before accessing the system."
    exit 1
fi

# Grant shell access
exec $SHELL
```

---

## Compliance Reporting

### Monthly Training Report Query

```sql
-- Generate monthly compliance report
SELECT
    DATE_TRUNC('month', tc.completed_at) as month,
    tc.course_title,
    COUNT(DISTINCT tc.operator_name) as unique_completions,
    ROUND(AVG(tc.score), 2) as avg_score,
    ROUND(AVG(tc.time_spent_minutes), 2) as avg_time_minutes,
    COUNT(*) FILTER (WHERE tc.status = 'passed') as passed,
    COUNT(*) FILTER (WHERE tc.status = 'failed') as failed
FROM training_completions tc
WHERE tc.completed_at >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', tc.completed_at), tc.course_title
ORDER BY month DESC, tc.course_title;
```

### Operator Training Transcript Query

```sql
-- Individual operator training transcript
SELECT
    tc.completed_at,
    tc.course_title,
    tc.score,
    tc.time_spent_minutes,
    tc.status,
    CASE
        WHEN tc.score >= tc.passing_score THEN 'PASS'
        ELSE 'FAIL'
    END as result
FROM training_completions tc
WHERE tc.operator_name = 'John Smith'
ORDER BY tc.completed_at DESC;
```

---

## Security Considerations

### Data Protection

1. **HTTPS Only:** All API calls must use TLS encryption
2. **Authentication:** API endpoint requires valid session token
3. **Rate Limiting:** Prevent spam/abuse of completion endpoint
4. **Input Validation:** Strict validation of operator names and course IDs
5. **Audit Trail:** IP address and user agent logged for all completions

### Cheating Prevention

1. **Session IDs:** Unique session ID prevents duplicate submissions
2. **Time Validation:** Minimum time spent required (e.g., 80% of course duration)
3. **Score Validation:** Score must match Captivate quiz results
4. **IP Whitelisting:** Optional - restrict to company network
5. **Manual Review:** Dashboard flags suspicious completions (too fast, perfect scores)

### Database Security

```sql
-- Prevent deletion of training records (audit requirement)
CREATE RULE prevent_training_deletion AS
    ON DELETE TO training_completions
    DO INSTEAD NOTHING;

-- Only allow inserts (no updates to historical records)
REVOKE UPDATE ON training_completions FROM triple_screen;
```

---

## Deployment Checklist

- [ ] Add tables to `supertrader_portfolio` database
- [ ] Insert course catalog entries into `training_courses`
- [ ] Deploy FastAPI endpoint to VPS
- [ ] Configure HTTPS/SSL certificate for API
- [ ] Update Captivate courses with completion JavaScript
- [ ] Export Captivate courses as HTML5
- [ ] Upload courses to VPS (e.g., `/var/www/training/`)
- [ ] Add "Training Records" page to Streamlit dashboard
- [ ] Test completion flow end-to-end
- [ ] Configure access control enforcement
- [ ] Document training URLs for operators
- [ ] Schedule monthly compliance report automation

---

## Future Enhancements

1. **Email Notifications:** Alert operators when new training assigned
2. **Certificate Generation:** Auto-generate PDF certificates on completion
3. **Expiration/Recertification:** Require annual re-training for critical SOPs
4. **Mobile Support:** Responsive design for tablet/phone training
5. **Offline Mode:** Download courses for offline completion, sync on reconnect
6. **Video Integration:** Embed video tutorials alongside Captivate modules
7. **Gamification:** Leaderboards, badges for training achievements
8. **AI Assistant:** ChatBot to answer questions during training

---

## Related Documents

- **SOP-001 through SOP-004**: Procedures that require training modules
- **GUIDE-001 through GUIDE-005**: User guides that inform training content
- **TRAIN-001**: New Operator Onboarding (references training system)
- **DATABASE_SCHEMA.md**: Will be updated with training tables

---

## Change Log

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-09-08 | 1.0 | IB | Initial design documentation |
