# Triple Screen Trading System Documentation

Welcome to the complete operational documentation for the **Triple Screen Trading System** - a quantitative trading platform implementing Dr. Alexander Elder's Triple Screen methodology with Van K. Tharp position sizing principles.

---

##  Documentation Overview

This documentation suite provides comprehensive guides for operating, monitoring, and maintaining the Triple Screen trading system. Whether you're managing VPS infrastructure, analyzing trade signals, or reviewing performance metrics, you'll find step-by-step procedures and quick reference materials here.

### What's Included

=== "VPS Operations"
    **4 Standard Operating Procedures (SOPs)**

    - [Service Management](SOPs/SOP-001-vps-service-management.md) - Restart, monitor, and troubleshoot systemd services
    - [Log Monitoring](SOPs/SOP-002-log-monitoring.md) - journalctl commands for real-time and historical log analysis
    - [Database Access](SOPs/SOP-003-database-access.md) - PostgreSQL connection and common queries
    - [Email Alert Response](SOPs/SOP-004-email-alert-response.md) - CRITICAL/WARNING/INFO alert triage and resolution

=== "Dashboard Guides"
    **5 User Guides**

    - [Navigation](guides/GUIDE-001-dashboard-navigation.md) - Access and navigate the Streamlit dashboard
    - [Watchlist Management](guides/GUIDE-002-watchlist-management.md) - Weekly relative strength scanning workflow
    - [Daily Signal Removal](guides/GUIDE-003-daily-signal-removal.md) - Discretionary signal filtering (9:00-9:25 AM ET)
    - [Trade Journaling](guides/GUIDE-004-trade-journaling.md) - Apgar scoring and 5-section trade documentation
    - [Performance Metrics](guides/GUIDE-005-performance-metrics.md) - Plain English explanations of R-multiples, expectancy, heat

=== "Quick Reference"
    **2 Cheat Sheets (2 pages max)**

    - [VPS Commands](reference/REF-001-vps-commands.md) - Essential systemctl, journalctl, and psql commands
    - [Database Queries](reference/REF-002-database-queries.md) - 26 copy-paste queries for data quality and troubleshooting

=== "Training"
    **Comprehensive Onboarding Guide**

    - [New Operator Onboarding](training/TRAIN-001-new-operator-onboarding.md) - 4-6 hour training curriculum with exercises

---

##  Quick Navigation

### Daily Tasks (9:00-9:25 AM ET)
1.  [Review Pending Signals](guides/GUIDE-003-daily-signal-removal.md#step-by-step-signal-removal) - Remove unwanted signals before market open
2.  [Check Portfolio Heat](guides/GUIDE-005-performance-metrics.md#portfolio-heat) - Ensure <6% threshold
3.  Monitor for Screen 3 breakouts during trading hours

### Weekly Tasks (Sunday Evening)
1.  [Run Relative Strength Scan](guides/GUIDE-002-watchlist-management.md#step-1-run-weekly-scan) - Generate watchlist from 507 symbols
2.  [Bulk Add to Watchlist](guides/GUIDE-002-watchlist-management.md#step-2-add-symbols-to-watchlist) - Paste comma-separated symbols
3.  [Trigger Signal Scan](guides/GUIDE-002-watchlist-management.md#step-5-trigger-signal-scan) - Generate Monday signals

### Emergency Responses
- **[CRITICAL] Alert**: [15-minute response SOP](SOPs/SOP-004-email-alert-response.md#step-2-critical-alert-response) - Halt trading immediately
- **Service Down**: [Service restart procedure](SOPs/SOP-001-vps-service-management.md#service-troubleshooting-flowchart)
- **Database Error**: [PostgreSQL troubleshooting](SOPs/SOP-003-database-access.md#troubleshooting)

---

##  System Overview

### Triple Screen Methodology

The system implements Dr. Alexander Elder's three-screen approach:

1. **Screen 1 (Weekly)**: Identify market tide using 13-week EMA and MACD histogram
2. **Screen 2 (Daily)**: Find pullbacks against the tide using daily indicators
3. **Screen 3 (Intraday)**: Enter on breakouts in the direction of the tide

### Van K. Tharp Position Sizing

- Risk per trade: 1% of portfolio value (1R = £100 on £10,000 account)
- Position size calculated from ATR-based stop distance
- Portfolio heat limit: 6% maximum combined risk

### Technology Stack

- **Data Pipeline**: Yahoo Finance → PostgreSQL (market data)
- **Signal Generation**: Python scanner → PostgreSQL (portfolio data)
- **Dashboard**: Streamlit (8 pages: Home, Overview, Positions, Signals, Trades, Apgar, Journal, Showcase)
- **VPS Deployment**: Ubuntu 22.04 LTS, systemd services, journalctl logging

---

##  Getting Started

### For New Operators

Start with the [New Operator Onboarding Guide](training/TRAIN-001-new-operator-onboarding.md) - a comprehensive 4-6 hour training curriculum covering:

- System architecture and trading methodology
- Dashboard navigation and daily workflows
- VPS operations and troubleshooting
- Alert response and escalation procedures

### For Experienced Users

Jump directly to:

- [VPS Command Quick Reference](reference/REF-001-vps-commands.md) - Essential commands on 2 pages
- [Database Query Cheat Sheet](reference/REF-002-database-queries.md) - 26 copy-paste queries
- [Daily Signal Removal Flowchart](guides/GUIDE-003-daily-signal-removal.md#signal-filtering-decision-flowchart) - Visual decision tree

---

##  Job Application Showcase

This documentation was created to demonstrate competencies for a **Change & Adoption Manager** role:

 **Clear, engaging communications** - Plain English, active voice, concrete examples
 **Training material creation** - Comprehensive onboarding guide with exercises
 **Practical SOPs and guides** - 10+ documents covering all operational tasks
 **Governance and compliance** - Version control, review cycles, change logs
 **AI-enabled tool support** - Claude Code skill prevents database schema errors

**Project Metrics:**
- 13 deliverables created in 2 weeks
- 4 flowcharts for decision-based procedures
- 36 dashboard screenshots with annotations
- 100% coverage of system interactions
- Professional metadata and version tracking

---

##  Support

**Issues & Questions**
GitHub Issues: [ouegy/triple-screen/issues](https://github.com/ouegy/triple-screen/issues)

**Emergency Escalation**
[VPS Service Management SOP](SOPs/SOP-001-vps-service-management.md) - See "Escalation Criteria"

---

**Documentation Version:** 1.0
**Last Updated:** 2026-09-08
**Maintained By:** Ian Butler
