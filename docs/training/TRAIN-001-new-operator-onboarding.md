# TRAIN-001: New Operator Onboarding

**Version:** 1.0 | **Last Updated:** 2026-09-08 | **Audience:** New Triple Screen Operators

---

## Welcome to the Triple Screen Trading System

This comprehensive training guide will transform you from complete beginner to confident operator of the Triple Screen trading system. No prior trading knowledge required - we'll teach you everything you need to know.

By the end of this training, you'll independently manage watchlists, respond to signals, journal trades, monitor VPS infrastructure, and handle alerts with confidence.

**Training Duration:** 4-6 hours (complete at your own pace)

---

## Learning Objectives

By completing this training, you will be able to:

1. Navigate the dashboard and locate all 8 pages without assistance
2. Run the weekly relative strength scan and update the manual watchlist with 30+ symbols
3. Remove unwanted signals from the pending queue before market open (9:25 AM ET deadline)
4. Score a trade using the 5-criteria Apgar system within 1 week of entry
5. Document trade exits with charts and tactical classification on the same day
6. Interpret portfolio heat and recognize when risk exceeds 6% threshold
7. SSH to VPS and restart a failed service within 5 minutes
8. Query the database to verify daily data loaded successfully (507 records expected)
9. Respond to CRITICAL email alerts within 15 minutes and halt trading until resolved
10. Monitor real-time logs during market hours to track signal generation

---

## Prerequisites

Before starting this training, ensure you have:

-  **Dashboard access:** Password to `https://trading.tradingwars.app` (or localhost URL)
-  **VPS SSH access:** Credentials for `ssh triple-screen@vps-hostname.com`
-  **Database credentials:** PostgreSQL password (stored securely, not in git)
-  **Email access:** Account receiving Triple Screen alerts
-  **Computer with:**
  - Modern web browser (Chrome, Firefox, Safari, Edge)
  - Terminal application (macOS Terminal, Windows PowerShell, or Linux shell)
  - Internet connection
-  **Time commitment:** 4-6 hours in 1-2 sessions

**Optional but helpful:**
- Basic understanding of stock markets (buy/sell, profit/loss concepts)
- Familiarity with command line basics (cd, ls, grep)
- SQL query experience (SELECT statements)

---

## Module 1: System Overview

### What is the Triple Screen Trading System?

The Triple Screen Trading System is an automated swing trading strategy based on Dr. Alexander Elder's methodology and Van K. Tharp's position sizing principles. It identifies medium-term trend-following opportunities in S&P 500 stocks.

**Three Screens Explained:**
- **Screen 1 (Weekly Trend):** Is the stock in a sustained uptrend? (EMA-13, EMA-26, MACD Force Index)
- **Screen 2 (Daily Pullback):** Has price pulled back within the weekly uptrend? (Force Index dip)
- **Screen 3 (Daily Breakout):** Is price breaking out from the pullback? (Force Index crosses above zero)

**Your Role as Operator:**
You provide discretionary judgment at key decision points while the system handles data processing, indicator calculation, and execution monitoring. Think of yourself as the quality control layer between algorithmic signals and capital deployment.

### Van K. Tharp Position Sizing Methodology

Every trade is sized using the R-multiple framework:
- **1R** = Initial risk (distance from entry to stop-loss)
- **Position size** = (Account equity × Risk % per trade) ÷ R
- **Max portfolio heat** = 10% (total risk across all open positions)

**Example:**
```
Account: £10,000
Risk per trade: 2% = £200
Entry: £150
Stop: £145
Initial risk (R): £5 per share
Position size: £200 ÷ £5 = 40 shares
Total position value: 40 × £150 = £6,000
```

### Weekly Operator Workflow

**Sunday Evening (After Market Close):**
1. Run weekly relative strength scan (10 min)
2. Update manual watchlist with 30-50 best stocks (15 min)

**Monday-Friday Morning (9:00-9:25 AM ET):**
1. Review overnight signals (5-10 signals expected)
2. Remove unwanted signals using discretionary judgment (10 min)
3. Verify dashboard shows clean signal queue by 9:25 AM

**Monday-Friday During Market Hours:**
1. System monitors for Screen 3 breakouts automatically
2. Check email for execution alerts (trade triggered)
3. Score new positions with Apgar (within 1 week of entry)

**After Position Exits:**
1. Document exit reason and tactic same day
2. Upload exit charts
3. Complete post-trade review 60+ days later

**Daily (Ongoing):**
1. Monitor VPS service health
2. Respond to email alerts within required timeframes
3. Review portfolio heat and performance metrics

### Practice Exercise 1.1: System Concepts Quiz

Before proceeding, verify your understanding:

**Q1:** Screen 2 identifies what type of market condition?
- A) Weekly uptrend
- B) Daily pullback within weekly uptrend
- C) Daily breakout entry trigger

**Q2:** If your account is £10,000 and you risk 2% per trade with a stop £5 away from entry, how many shares do you buy?
- A) 40 shares
- B) 200 shares
- C) 100 shares

**Q3:** What is the maximum portfolio heat allowed?
- A) 5%
- B) 10%
- C) 15%

**Answers:** Q1: B, Q2: A, Q3: B

If you missed any, re-read the relevant section before continuing.

---

## Module 2: Dashboard Navigation

### Accessing the Dashboard

**Production Environment:**
1. Open browser and navigate to: `https://trading.tradingwars.app`
2. Enter dashboard password when prompted (characters hidden as bullets)
3. Press Enter or click outside password field
4. **Success:** You see "Triple Screen Trading System" home page

**Local Development Environment:**
```bash
cd backend/dashboard
streamlit run Home.py
# Open browser to: http://localhost:8501
```

**Troubleshooting:**
- Password incorrect: Contact system administrator
- Page won't load: Check VPS status (Module 7)
- Certificate warning: Production uses HTTPS - accept security exception if self-signed cert

### Dashboard Page Reference

**Home Page:**
- Welcome message and system status
- Quick navigation guide
- Use when: First login or orientation

**Overview Page:**
- Portfolio summary (equity, cash, open positions, portfolio heat)
- Performance metrics (Total Return %, Win Rate, Sharpe Ratio, Recovery Factor)
- Market classification (bull/bear/sideways + volatility)
- Equity curve chart
- Use when: Daily health check, weekly performance review

**Positions Page:**
- All open positions with live P&L
- Trade Bill format (Identification, Apgar, Entry Setup, After Entry sections)
- Entry charts and market context
- Partial exits and stop movements
- Use when: Monitoring active trades intraday

**Signals Page:**
- Manual Watchlist management (add/remove symbols)
- Pending signals awaiting Screen 3 breakout
- Position sizing and risk calculations
- Signal expiration countdown
- Use when: Weekly watchlist update, daily signal removal (9:00-9:25 AM ET)

**Trades Page:**
- Complete historical trade performance
- Advanced filtering (Apgar score, exit tactic, review status, A-trades only)
- Expandable Trade Bill for each closed position
- Performance analytics and CSV export
- Use when: Post-trade analysis, identifying performance patterns

**Trade Apgar Page:**
- 5-criteria scoring form (0-10 total points)
- Market context fields (earnings date, dividend date, conditions)
- Entry rationale text and chart upload
- List of unscored positions
- Use when: Scoring trades within 1 week of entry

**Trade Journal Page:**
- Post-exit documentation workflow
- 5 sections: Entry reason, Entry/exit data, Exit reason, Exit tactic, Post-trade review
- Chart management (upload/delete)
- Use when: Documenting exits same day, conducting 60-day retrospective reviews

**A Trade Showcase Page:**
- Reference A-grade trade example (VLO backtest trade)
- Complete Trade Bill demonstration
- Full Apgar scoring breakdown
- Use when: Learning trade documentation standards

### Practice Exercise 2.1: Navigation Drill

Complete these tasks without looking at the guide:

1. Navigate to Overview page and find your current portfolio heat percentage
2. Navigate to Signals page and count how many symbols are in your watchlist
3. Navigate to Trade Apgar page and identify how many positions need scoring
4. Navigate to Trades page and filter to show only A-trades (Apgar 7+)

**Success criteria:** Completed all 4 tasks in under 3 minutes

---

## Module 3: Weekly Watchlist Management

### Running the Weekly Relative Strength Scan

**When:** Sunday evening after market close (5:00-10:00 PM ET)

**What it does:** Scans all S&P 500 stocks for sustained weekly uptrends (EMA-26 rising 3+ weeks) with early bullish momentum (MACD histogram uptick below zero).

**Steps:**

1. SSH to VPS:
   ```bash
   ssh triple-screen@your-vps-hostname.com
   ```

2. Navigate to backend and activate environment:
   ```bash
   cd /path/to/triple-screen/backend
   source venv/bin/activate
   ```

3. Run weekly scan:
   ```bash
   python scripts/run_weekly_ema_macd_scan.py
   ```

4. Review scan output table showing:
   - Rank (by MACD histogram change)
   - Symbol and company name
   - Sector
   - Current price
   - EMA-26 current vs previous
   - MACD histogram current vs previous

5. Locate comma-separated list at bottom:
   ```
   Comma-separated symbols (for copy/paste):
   ----------------------------------------
   AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, ...
   ```

6. Copy this list (select text, Ctrl+C or Cmd+C)

**Expected output:** 20-60 symbols depending on market conditions (bull markets produce more, bear markets fewer)

### Adding Symbols to Watchlist (Bulk Method)

1. Open dashboard → Signals page
2. Locate "Manual Watchlist" section at top
3. Click **Add Multiple Stocks** tab
4. Paste comma-separated symbol list in "Symbols" text area
5. Add notes (optional): "Weekly scan 2026-09-08 - Strong EMA + MACD uptick"
6. Click **Add All Stocks** button
7. Review results:
   - Green: "Added N stocks: AAPL, MSFT, ..."
   - Yellow: "Skipped N (already in watchlist): ..."
   - Red: "Invalid N symbols: ..." (with reasons)

**Common issues:**
- Invalid symbols: Check spelling, verify symbol exists in market database
- Duplicates: Automatically skipped (no error)
- All symbols rejected: Check VPS database connection

### Removing Outdated Symbols

**When to remove:**
- Stock broke below weekly EMA-26
- MACD histogram turned negative 2+ weeks
- Sector rotation (money flowing elsewhere)
- Position limit reached for that sector

**Steps:**
1. Review watchlist table on Signals page
2. Click **Remove** button next to symbol
3. Confirmation message: "Removed SYMBOL"
4. Page refreshes with updated list

**Bulk cleanup:**
1. Click **Clear All** button (trash icon) to remove entire watchlist
2. Confirm in popup: "Removed N stocks from watchlist"
3. Use this sparingly (typically only during strategy changes)

### Practice Exercise 3.1: Watchlist Management

Complete this workflow:

1. Add 3 symbols manually: AAPL, MSFT, GOOGL (use "Add Single Stock" tab)
2. Add notes for each: "Practice exercise - learning watchlist management"
3. Verify watchlist count increased by 3
4. Remove GOOGL from watchlist
5. Verify watchlist count decreased by 1

**Success criteria:** Watchlist contains AAPL and MSFT with notes, GOOGL removed

---

## Module 4: Daily Signal Removal

### Understanding Pending Signals

**What is a pending signal?**
A stock that passed Screen 1 (weekly trend) and Screen 2 (daily pullback), now awaiting Screen 3 (daily breakout) to trigger entry.

**Signal lifecycle:**
1. Generated overnight after daily data refresh (6:00 PM ET)
2. Reviewed by operator next morning (9:00-9:25 AM ET)
3. Operator removes unwanted signals
4. System monitors remaining signals for Screen 3 breakout during market hours
5. Signal triggers → Position entry OR signal expires after 24 hours

### Daily Signal Removal Workflow

**When:** Every trading day, 9:00-9:25 AM ET (must complete before 9:30 AM market open)

**Steps:**

1. Navigate to dashboard → Signals page
2. Scroll to "Signals Awaiting Breakout" section
3. Review table columns:
   - Symbol
   - Signal Date (when Screen 1+2 passed)
   - Expires At (24-hour countdown)
   - Remove button

4. For each signal, apply discretionary filters:
   - **Market classification:** Keep more in bull markets, fewer in bear markets
   - **Sector rotation:** Remove lagging sectors, keep leaders
   - **News events:** Remove if earnings within 48 hours, FDA decisions pending, lawsuits
   - **Chart quality:** Expand "Daily Chart" to verify clean pullback pattern
   - **Portfolio heat:** Remove if approaching 10% risk limit

5. Click **Remove** button for unwanted signals

6. Verify final signal queue by 9:25 AM ET

**Decision framework:**

| Market Regime | Keep % | Example |
|---------------|--------|---------|
| Bull Market | 80-90% | 8 signals generated → keep 6-7 |
| Choppy Market | 50-60% | 8 signals generated → keep 4-5 |
| Bear Market | 20-40% | 8 signals generated → keep 1-3 |

**Red flags (always remove):**
- Earnings report within 48 hours
- FDA/regulatory decision pending
- Executive scandal or lawsuit headlines
- Sector showing clear distribution/selling pressure
- Chart breaking major support levels

### Practice Exercise 4.1: Signal Evaluation

Review these hypothetical signals and decide keep/remove:

**Signal 1:** AAPL, earnings tomorrow, clean chart, tech sector leading
- Decision: REMOVE (earnings binary risk)

**Signal 2:** XOM, no news, clean pullback, energy sector rotating in, portfolio heat 4%
- Decision: KEEP (all criteria favorable)

**Signal 3:** CVS, lawsuit headline today, healthcare sector weak, chart messy
- Decision: REMOVE (multiple red flags)

If your decisions match, you understand the discretionary filtering framework.

---

## Module 5: Trade Journaling

### The Apgar Scoring System

**Purpose:** Systematically evaluate trade setup quality after entry. A-trades (score 7+) should statistically outperform lower-quality setups.

**5 Criteria (0-2 points each):**

**Criterion 1: Daily Price**
- 0 points: Above value zone
- 1 point: In the value zone
- 2 points: Below the value zone (best entry)

**Criterion 2: MACD Uptick**
- 0 points: Shallow above centre line
- 1 point: Shallow below centre line
- 2 points: Deep below centre line (best momentum)

**Criterion 3: Weekly Impulse**
- 0 points: Red (downtrend)
- 1 point: Green (uptrend)
- 2 points: Blue after red (trend reversal, best setup)

**Criterion 4: RSI**
- 0 points: Overbought (>70)
- 1 point: Neutral (30-70)
- 2 points: Oversold (<30, best value)
- Enter exact RSI value in number field

**Criterion 5: Perfection**
- 0 points: Neither timeframe perfect
- 1 point: One timeframe perfect
- 2 points: Both timeframes perfect

**Scoring:**
- 0-6 points: Non-A-trade (acceptable but not ideal)
- 7-10 points: A-trade (high-quality setup)

**Target:** 30-40% of trades should be A-trades. Too high (>50%) means overly selective; too low (<20%) means accepting poor setups.

### Completing Trade Apgar Workflow

**When:** Within 1 week of position entry (while setup details fresh)

**Steps:**

1. Navigate to dashboard → Trade Apgar page
2. Select position from dropdown (unscored positions listed first)
3. Score each of 5 criteria using radio buttons
4. Enter exact RSI value in number field (criterion 4)
5. Review auto-calculated total score and A-trade status
6. Document market context:
   - **Earnings Date:** Check Briefing.com or company IR calendar
   - **Dividend Date:** Check Yahoo Finance for ex-div date
   - **Market Conditions:** "Spike bounce in effect, S&P above 50MA, sector showing relative strength"
7. Write entry rationale: "Perfect pullback to EMA-26, strong Force Index divergence, early breakout with volume confirmation"
8. Upload entry charts (daily and weekly)
9. Click **Save Apgar & Context** button

**Success:** Position marked with Apgar score, ready for exit analysis

### Documenting Trade Exits

**When:** Same day you close position (memory fades quickly)

**Steps:**

1. Navigate to dashboard → Trade Journal page
2. Select closed position from dropdown
3. Review Section A (Entry reason - pre-filled from Apgar)
4. Review Section B (Entry/exit data - auto-populated)
5. Complete Section C (Reason for Exit):
   - Write detailed description: "Hit R1 target, showing signs of reversal in morning session. MACD histogram weakening, Force Index turning negative."
   - Upload exit chart showing entry + exit together
   - Click **Save Exit Details**
6. Complete Section D (Exit Tactic):
   - Choose from Elder's 8 standard tactics:
     - 2:1 Hit target
     - 2:2 Hit stop
     - 2:3 Hit value zone
     - 2:3a Hit envelope
     - 2:4 Trade going nowhere
     - 2:5 Started turning
     - 2:6 Couldn't stand the pain
     - 2:7 Junk trade
   - Click **Save Exit Tactic**

**Section E (Post-Trade Review) - wait 60 days:**
After 2+ months, return to position and write hindsight analysis:
- "In hindsight, this was a great entry. Could have held for R3 target instead of exiting early at R1. Weekly uptrend continued for 6 more weeks after my exit."
- Upload follow-up chart showing how trade developed

### Practice Exercise 5.1: Mock Apgar Scoring

Score this hypothetical trade:

**Trade:** AAPL entry on 2026-09-08
- Daily price: In value zone (1 point)
- MACD uptick: Deep below centre line (2 points)
- Weekly Impulse: Green (1 point)
- RSI: 42 (neutral, 1 point)
- Perfection: Daily perfect, weekly not (1 point)

**Total score:** 6 points (non-A-trade, acceptable quality)

Practice this workflow on the dashboard with a real or test position.

---

## Module 6: Performance Metrics

### Understanding Portfolio Heat

**What it is:** Total percentage of your account at risk across all open positions.

**Calculation:**
```
For each position:
  Risk per position = Shares × (Entry - Stop)

Total portfolio heat = Sum of all position risks ÷ Total equity
```

**Example:**
```
Account: £10,000
Position 1: 100 shares, entry £150, stop £145 → Risk: £500
Position 2: 50 shares, entry £200, stop £192 → Risk: £400
Position 3: 75 shares, entry £80, stop £77 → Risk: £225

Total heat = (£500 + £400 + £225) ÷ £10,000 = 11.25%
```

**Thresholds:**
- Below 6%: Normal (room for new trades)
- 6-8%: Moderate (be selective)
- 8-10%: High (keep best signals only)
- Above 10%: **CRITICAL - Remove ALL signals, wait for exits**

**Where to find:** Overview page → Portfolio Summary section → Portfolio Heat percentage with color coding (green <10%, red ≥10%)

### Key Performance Metrics Explained

**Total Return:**
- Percentage: How much you've grown relative to starting capital
- Amount: Actual profit/loss in pounds
- Example: Started £10,000, now £10,800 → +8% or +£800

**Win Rate:**
- Percentage of trades that make money
- Example: 10 closed trades, 6 winners → 60% win rate
- Note: High win rate doesn't guarantee profitability (small winners + huge losers = net loss)

**Profit Factor:**
- Total profits ÷ Total losses
- Example: All winners = £1,200, all losers = £400 → Profit factor = 3.0
- Target: Above 2.0 = excellent, 1.5-2.0 = good, below 1.0 = losing money

**Expectancy:**
- Average profit per trade over many trades
- Formula: (Win Rate × Avg Win) - (Loss Rate × Avg Loss)
- Example: 60% win rate, £197 avg win, £100 avg loss → Expectancy = £78.20
- Target: Positive = profitable, above £50 (for £10k account) = good

**Sharpe Ratio:**
- Risk-adjusted return (how smooth is your equity curve)
- Above 1.5 = excellent, 1.0-1.5 = good, below 0.5 = too volatile
- Example: Two traders both made 20% annually, but Trader A with steady growth (Sharpe 1.8) beats Trader B with wild swings (Sharpe 0.4)

**Max Drawdown:**
- Largest drop from peak to valley
- Example: Account peaked at £12,000, dropped to £11,000 → Max drawdown = -£1,000 or -8.3%
- Use this to set expectations: If max drawdown is 10%, expect occasional 10% dips (don't panic)

### Practice Exercise 6.1: Metrics Interpretation

Review your dashboard Overview page and answer:

1. What is your current portfolio heat? Is it within acceptable limits?
2. What is your win rate? Does your profit factor support profitability?
3. What is your expectancy? Is it positive?
4. What is your max drawdown? Are you comfortable with that level of volatility?

**Success criteria:** Answered all 4 questions and can explain what each metric means in plain English

---

## Module 7: VPS Operations

### Essential VPS Skills

**Connecting to VPS:**
```bash
ssh triple-screen@your-vps-hostname.com
# Enter password when prompted
# Success: You see command prompt
```

**Checking Service Status:**
```bash
sudo systemctl status triple-screen-orchestrator
sudo systemctl status triple-screen-dashboard
sudo systemctl status triple-screen-api
```

Expected output (healthy service):
```
Active: active (running) since Mon 2026-09-08 09:00:00 UTC; 2h 15min ago
```

**Restarting a Service:**
```bash
sudo systemctl restart triple-screen-orchestrator
sudo systemctl status triple-screen-orchestrator  # Verify restart
```

Expected: Status changes to "active (running)" within 30 seconds

**Viewing Real-Time Logs:**
```bash
# Follow orchestrator logs
sudo journalctl -u triple-screen-orchestrator -f

# Stop following: Press Ctrl+C
```

**Common Log Queries:**
```bash
# Errors from last hour
journalctl -u "triple-screen-*" -p err --since "1 hour ago"

# Logs from market open (9:30-10:00 AM)
journalctl -u triple-screen-orchestrator --since "today 09:30" --until "today 10:00"

# Find logs mentioning AAPL
journalctl -u triple-screen-orchestrator --since "today" | grep AAPL
```

### Database Access for Verification

**Connect to database:**
```bash
# Export password (one-time per SSH session)
export PGPASSWORD='your_database_password'

# Connect to market database
psql -U triple_screen -d supertrader_market
```

**Common verification queries:**

Count today's daily prices:
```sql
SELECT COUNT(*) FROM daily_prices WHERE date = CURRENT_DATE;
-- Expected: 507 records
```

Check for NULL values:
```sql
SELECT symbol, close FROM daily_prices
WHERE date = CURRENT_DATE AND close IS NULL
LIMIT 10;
-- Expected: 0 rows (no NULLs)
```

List pending signals:
```bash
psql -U triple_screen -d supertrader_portfolio -c "
  SELECT symbol, signal_date, expires_at
  FROM live_signals
  WHERE status = 'pending'
  ORDER BY signal_date DESC;
"
```

**Exit database:**
```sql
\q
```

**Exit SSH:**
```bash
exit
```

### Practice Exercise 7.1: VPS Operations Drill

Complete these tasks on your VPS:

1. SSH to VPS
2. Check orchestrator service status (verify it's running)
3. View last 50 lines of orchestrator logs
4. Connect to market database and count daily_prices records for current date
5. Exit database and SSH session

**Time limit:** 5 minutes
**Success criteria:** Completed all 5 tasks, verified orchestrator running, confirmed 400+ price records

---

## Module 8: Alert Response

### Email Alert Severity Levels

**[CRITICAL] Alerts:**
- Response time: **15 minutes**
- Impact: System-wide data corruption, all signals invalid
- Action: **HALT TRADING immediately**
- Example: "NaN Data Detected - 235/507 symbols (46.4%)"

**[WARNING] Alerts:**
- Response time: **2 hours**
- Impact: Partial data failure, some symbols affected
- Action: Continue trading (monitor closely)
- Example: "Data Validation Failures - 12/507 (2.4%)"

**[INFO] Alerts:**
- Response time: Next business day (verify only)
- Impact: Normal operation confirmation
- Action: Normal operations
- Example: "Daily Ingestion Complete - 507/507 (100.0%)"

### CRITICAL Alert Response Workflow

**Alert received:** "[CRITICAL] Triple Screen - NaN Data Detected"

**Immediate actions (within 15 minutes):**

1. **DO NOT TRADE** new signals until resolved
2. SSH to VPS and verify issue:
   ```bash
   psql -U triple_screen -d supertrader_market -c "
     SELECT symbol, close
     FROM daily_prices
     WHERE date = CURRENT_DATE AND close IS NULL
     LIMIT 10;
   "
   ```
3. Check orchestrator logs for root cause:
   ```bash
   sudo journalctl -u triple-screen-orchestrator --since "today 02:00" | grep ERROR
   ```
4. Run backfill script (if implemented):
   ```bash
   cd /opt/triple-screen/backend
   source .venv/bin/activate
   poetry run python -m src.scripts.backfill_corrupted_data --date $(date +%Y-%m-%d)
   ```
5. Verify fix:
   ```bash
   psql -U triple_screen -d supertrader_market -c "
     SELECT COUNT(*)
     FROM daily_prices
     WHERE date = CURRENT_DATE AND close IS NULL;
   "
   # Expected: 0 (no NULLs)
   ```
6. Resume trading only after verification passes

### WARNING Alert Response Workflow

**Alert received:** "[WARNING] Data Validation Failures - 12/507 (2.4%)"

**Response (within 2 hours):**

1. Assess scope:
   ```bash
   psql -U triple_screen -d supertrader_market -c "
     SELECT COUNT(*) FROM daily_prices WHERE date = CURRENT_DATE;
   "
   ```
2. Decision tree:
   - <5% failed: Log and monitor (acceptable)
   - 5-10% failed: Investigate within 2 hours
   - >10% failed: Escalate to CRITICAL response
3. Verify no pending signals for failed symbols:
   ```bash
   psql -U triple_screen -d supertrader_portfolio -c "
     SELECT symbol FROM live_signals
     WHERE status = 'pending' AND symbol IN ('ABBV', 'ACN');
   "
   ```
4. Document in trading journal: "WARNING: 12 symbols failed validation - Yahoo API instability"

### INFO Alert Verification

**Alert received:** "[INFO] Daily Ingestion Complete - 507/507 (100.0%)"

**Verification (next business day, optional):**
1. Confirm success rate ≥95%
2. Note execution time (baseline: 30-60 seconds)
3. Review pending signals for trading opportunities
4. Delete email (or archive)

### Practice Exercise 8.1: Alert Triage

Classify these alerts and state response time:

1. "[CRITICAL] NaN Data Detected - 150/507 symbols"
   - **Response:** Immediate (15 min), halt trading

2. "[WARNING] Data Validation Failures - 8/507 (1.6%)"
   - **Response:** Within 2 hours, continue trading

3. "[INFO] Daily Ingestion Complete - 507/507 (100%)"
   - **Response:** Next day verification (optional)

If your responses match, you understand alert prioritization.

---

## Assessment Checklist

Before concluding your training, verify you can perform these tasks independently:

### Dashboard Operations
- [ ] Navigate to any dashboard page within 30 seconds
- [ ] Locate portfolio heat on Overview page and interpret threshold
- [ ] Find pending signals on Signals page
- [ ] Filter Trades page to show only A-trades

### Weekly Watchlist
- [ ] SSH to VPS and run weekly scan script
- [ ] Copy comma-separated symbol list from scan output
- [ ] Add 10+ symbols to watchlist using bulk method
- [ ] Remove 3 symbols from watchlist individually
- [ ] Verify watchlist count updated correctly

### Daily Signal Removal
- [ ] Access Signals page before 9:25 AM ET
- [ ] Review 5+ pending signals and apply discretionary filters
- [ ] Remove unwanted signals by clicking Remove button
- [ ] Verify final signal queue clean before market open

### Trade Journaling
- [ ] Score a trade using 5-criteria Apgar system
- [ ] Calculate total Apgar score and identify A-trade status
- [ ] Upload entry chart (daily and weekly)
- [ ] Document exit reason and tactic same day
- [ ] Explain when post-trade review becomes available (60 days)

### Performance Metrics
- [ ] Locate portfolio heat and recognize 10% threshold
- [ ] Explain difference between win rate and profit factor
- [ ] Calculate expectancy given win rate, avg win, avg loss
- [ ] Interpret Sharpe ratio (higher = smoother equity curve)

### VPS Operations
- [ ] SSH to VPS using terminal
- [ ] Check status of all 3 core services
- [ ] Restart orchestrator service and verify success
- [ ] View real-time logs using journalctl -f
- [ ] Filter logs for errors only
- [ ] Exit SSH session cleanly

### Database Queries
- [ ] Export PGPASSWORD and connect to market database
- [ ] Count daily_prices records for current date
- [ ] Check for NULL values in close prices
- [ ] List pending signals from portfolio database
- [ ] Exit psql and unset password

### Alert Response
- [ ] Identify alert severity from email subject
- [ ] State response time for CRITICAL, WARNING, INFO
- [ ] Execute CRITICAL response workflow (verify NULLs, run backfill)
- [ ] Assess WARNING scope and apply decision tree
- [ ] Verify INFO alert and delete email

**Training Complete:** If you checked all boxes, you're ready to operate the Triple Screen system independently!

---

## Quick Reference: Daily Task Checklist

**Every Sunday Evening:**
- [ ] Run weekly scan: `python scripts/run_weekly_ema_macd_scan.py`
- [ ] Copy comma-separated symbols
- [ ] Update watchlist on Signals page (30-50 stocks)
- [ ] Verify watchlist count updated

**Every Trading Day (9:00-9:25 AM ET):**
- [ ] Open dashboard → Signals page
- [ ] Review pending signals (typically 5-10)
- [ ] Remove unwanted signals using discretionary filters
- [ ] Verify signal queue clean by 9:25 AM

**After New Position Entry (Within 1 Week):**
- [ ] Navigate to Trade Apgar page
- [ ] Score trade with 5 criteria
- [ ] Upload entry charts
- [ ] Document market context and entry rationale

**After Position Exit (Same Day):**
- [ ] Navigate to Trade Journal page
- [ ] Document exit reason and upload chart
- [ ] Select exit tactic from Elder's 8 categories
- [ ] Save exit details

**Daily (Ongoing):**
- [ ] Check email for Triple Screen alerts
- [ ] Respond to CRITICAL alerts within 15 minutes
- [ ] Monitor portfolio heat on Overview page
- [ ] Review VPS service health (if time permits)

**Weekly (Sunday):**
- [ ] Review performance metrics on Overview page
- [ ] Identify A-trades on Trades page and analyze patterns
- [ ] Complete post-trade reviews for positions 60+ days old

---

## Quick Reference: Weekly Task Checklist

**Every Sunday Evening:**
- [ ] Run weekly scan and update watchlist (Module 3)
- [ ] Review weekly performance metrics (Module 6)
- [ ] Complete pending post-trade reviews (Module 5)

---

## Troubleshooting Common Issues

**Issue:** Dashboard won't load
- **Solution:** Check VPS status, verify orchestrator and dashboard services running, restart if needed

**Issue:** Cannot add symbols to watchlist (all rejected)
- **Solution:** Verify symbols exist in market database, check for typos, ensure VPS database connection active

**Issue:** No pending signals showing
- **Solution:** Verify watchlist has stocks, check market conditions (bear markets produce fewer signals), review logs for scan completion

**Issue:** SSH connection refused
- **Solution:** Verify VPS hostname/IP, check SSH credentials, ensure VPS is running (contact hosting provider)

**Issue:** Database query returns 0 rows (expected data)
- **Solution:** Check date filter in WHERE clause, verify daily data refresh completed, review orchestrator logs

**Issue:** Service status shows "failed"
- **Solution:** Check logs (`journalctl -u service-name -n 100`), look for errors, fix root cause, restart service

**Issue:** Email alerts not received
- **Solution:** Check ALERT_EMAIL_ENABLED in .env.production, verify SendGrid quota, check spam folder

---

## Related Documents

**User Guides (Complete Walkthroughs):**
- GUIDE-001: Dashboard Navigation
- GUIDE-002: Weekly Watchlist Management
- GUIDE-003: Daily Signal Removal
- GUIDE-004: Trade Journaling & Post-Trade Analysis
- GUIDE-005: Performance Metrics

**SOPs (Operational Procedures):**
- SOP-001: VPS Service Management
- SOP-002: Log Monitoring and Analysis
- SOP-003: Database Access and Queries
- SOP-004: Email Alert Response

**Reference:**
- DOCUMENTATION_STYLE_GUIDE.md (Section 2.4: Training Materials)
- DATABASE_SCHEMA.md (Complete schema reference)

---

## Next Steps After Training

**Week 1:**
- Shadow experienced operator during daily signal removal
- Practice Apgar scoring on historical trades
- Document 2-3 exits with charts and tactics

**Week 2:**
- Operate independently with daily check-ins
- Run first weekly scan solo
- Respond to first INFO alert independently

**Week 3:**
- Full independent operation
- Handle first WARNING alert (if occurs)
- Complete first post-trade review (60-day retrospective)

**Month 2+:**
- Analyze your A-trade vs non-A-trade performance
- Identify personal strengths/weaknesses in discretionary filtering
- Optimize exit tactics based on journal data

---

## Change Log

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-09-08 | 1.0 | IB | Initial creation - comprehensive new operator onboarding consolidating all guides and SOPs |

---

**Document Owner:** Ian Butler
**Next Review:** 2026-12-08
**Feedback:** Open GitHub issue or contact via project channels
