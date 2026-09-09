# SOP-003: Database Access and Queries

**Version:** 1.0 | **Owner:** System Operator | **Review Date:** 2026-12-08

---

## Purpose

This SOP defines the standard procedure for accessing and querying the PostgreSQL databases on the VPS, performing data quality checks, and executing common diagnostic queries for the Triple Screen trading system.

Expected outcomes:
- Secure database access via SSH and psql
- Ability to verify data integrity and completeness
- Quick diagnosis of data quality issues
- Monitoring of pending signals and active positions

---

## Scope

**When to use this SOP:**
- Daily data verification after market data refresh
- Investigating missing or incorrect data
- Checking pending signals before market open
- Reviewing recent trades and positions
- Debugging orchestrator execution issues
- Performing ad-hoc data analysis

**When NOT to use:**
- Modifying data (use application scripts instead)
- Creating or altering database schema
- Performance tuning or maintenance tasks

---

## Prerequisites

Before starting, ensure you have:
-  SSH access to VPS (keys configured)
-  VPS hostname/IP address
-  Database password (stored securely, not committed to git)
-  Basic SQL knowledge
-  PostgreSQL client (psql) available on VPS

---

## Procedure

### Step 1: Connect to VPS via SSH

```bash
ssh triple-screen@your-vps-hostname.com
```

**Expected output:**
```
Welcome to Ubuntu 24.04 LTS
Last login: [timestamp]
```

**Success criteria:** You see the VPS command prompt

---

### Step 2: Export Database Password

Set the PostgreSQL password as an environment variable to avoid password prompts:

```bash
export PGPASSWORD='your_database_password_here'
```

**IMPORTANT:**
- Replace `your_database_password_here` with actual password
- This password is NOT committed to git
- Password remains active only for current SSH session
- Re-export if you disconnect and reconnect

**Success criteria:** Command executes with no output (password set silently)

---

### Step 3: Connect to Market Database

Access the market data database containing OHLCV prices and indicators:

```bash
psql -U triple_screen -d supertrader_market
```

**Expected output:**
```
psql (16.x)
Type "help" for help.

supertrader_market=>
```

**Success criteria:** You see the `supertrader_market=>` prompt

To exit psql:
```sql
\q
```

---

### Step 4: Connect to Portfolio Database

Access the portfolio database containing trades and positions:

```bash
psql -U triple_screen -d supertrader_portfolio
```

**Expected output:**
```
psql (16.x)
Type "help" for help.

supertrader_portfolio=>
```

**Success criteria:** You see the `supertrader_portfolio=>` prompt

---

### Step 5: Execute Common Data Quality Queries

The following queries can be run from the command line without entering interactive psql mode, or within the psql prompt.

#### 5.1 Count Today's Daily Price Records

**Purpose:** Verify daily data refresh completed successfully

**From command line:**
```bash
psql -U triple_screen -d supertrader_market -c "
  SELECT COUNT(*) as record_count
  FROM daily_prices
  WHERE date = CURRENT_DATE;
"
```

**Expected output:**
```
 record_count
--------------
          507
(1 row)
```

**Success criteria:** Count matches active symbol count (typically 400-507)

---

#### 5.2 Find Symbols with NULL Values

**Purpose:** Detect data quality issues from failed API calls

**From command line:**
```bash
psql -U triple_screen -d supertrader_market -c "
  SELECT s.symbol, dp.date, dp.close, dp.volume
  FROM daily_prices dp
  JOIN symbols s ON s.id = dp.symbol_id
  WHERE dp.date = CURRENT_DATE
    AND (dp.close IS NULL OR dp.volume IS NULL)
  LIMIT 20;
"
```

**Expected output:**
```
 symbol | date | close | volume
--------+------+-------+--------
(0 rows)
```

**Success criteria:** Zero rows returned (no NULL values)

---

#### 5.3 Check for Missing Indicators

**Purpose:** Verify technical indicators calculated correctly

**From command line:**
```bash
psql -U triple_screen -d supertrader_market -c "
  SELECT
    COUNT(DISTINCT dp.symbol_id) as symbols_with_prices,
    COUNT(DISTINCT i_atr.symbol_id) as symbols_with_atr,
    COUNT(DISTINCT i_ema.symbol_id) as symbols_with_ema
  FROM daily_prices dp
  LEFT JOIN indicators i_atr ON i_atr.symbol_id = dp.symbol_id
    AND i_atr.date = dp.date
    AND i_atr.indicator_name = 'atr_14_daily'
  LEFT JOIN indicators i_ema ON i_ema.symbol_id = dp.symbol_id
    AND i_ema.date = dp.date
    AND i_ema.indicator_name = 'ema_13_daily'
  WHERE dp.date = CURRENT_DATE;
"
```

**Expected output:**
```
 symbols_with_prices | symbols_with_atr | symbols_with_ema
---------------------+------------------+------------------
                 507 |              507 |              507
(1 row)
```

**Success criteria:** All three counts match

---

#### 5.4 List Pending Signals

**Purpose:** Check for trade opportunities awaiting Screen 3 breakout

**From command line:**
```bash
psql -U triple_screen -d supertrader_portfolio -c "
  SELECT id, symbol, signal_date, status, expires_at
  FROM live_signals
  WHERE status = 'pending'
  ORDER BY signal_date DESC;
"
```

**Expected output:**
```
 id | symbol | signal_date         | status  | expires_at
----+--------+---------------------+---------+---------------------
  5 | AAPL   | 2026-09-08 09:30:00 | pending | 2026-09-09 09:30:00
  6 | MSFT   | 2026-09-08 09:30:00 | pending | 2026-09-09 09:30:00
(2 rows)
```

**Success criteria:** Query runs successfully, review signals for action

---

#### 5.5 View Open Positions

**Purpose:** Monitor active trades and current P&L

**From command line:**
```bash
psql -U triple_screen -d supertrader_portfolio -c "
  SELECT
    lp.symbol,
    p.entry_date,
    p.entry_price,
    lp.current_price,
    lp.unrealized_pnl,
    lp.unrealized_r,
    lp.stop_type
  FROM live_positions lp
  JOIN positions p ON p.id = lp.position_id
  ORDER BY lp.unrealized_r DESC;
"
```

**Expected output:**
```
 symbol | entry_date | entry_price | current_price | unrealized_pnl | unrealized_r | stop_type
--------+------------+-------------+---------------+----------------+--------------+-----------
 AAPL   | 2026-09-01 |      150.00 |        165.00 |        1500.00 |         3.50 | trailing
 MSFT   | 2026-09-05 |      320.00 |        325.00 |         250.00 |         1.25 | breakeven
(2 rows)
```

**Success criteria:** Query runs successfully, verify positions match expectations

---

#### 5.6 Check for Data Gaps (Missing Dates)

**Purpose:** Detect missing historical data for a symbol

**From command line (replace 'AAPL' with target symbol):**
```bash
psql -U triple_screen -d supertrader_market -c "
  WITH date_series AS (
    SELECT generate_series(
      CURRENT_DATE - INTERVAL '30 days',
      CURRENT_DATE,
      '1 day'::interval
    )::date AS expected_date
  )
  SELECT ds.expected_date, s.symbol
  FROM date_series ds
  CROSS JOIN symbols s
  LEFT JOIN daily_prices dp ON dp.symbol_id = s.id
    AND dp.date = ds.expected_date
  WHERE s.symbol = 'AAPL'
    AND dp.date IS NULL
    AND EXTRACT(DOW FROM ds.expected_date) NOT IN (0,6)
  ORDER BY ds.expected_date;
"
```

**Expected output (if no gaps):**
```
 expected_date | symbol
---------------+--------
(0 rows)
```

**Success criteria:** Zero rows (no missing weekday dates)

---

#### 5.7 Verify Weekly Indicators for Latest Week

**Purpose:** Check Screen 1 data after weekly indicator calculation

**From command line:**
```bash
psql -U triple_screen -d supertrader_market -c "
  SELECT
    s.symbol,
    wp.date as week_start,
    wp.close,
    i_ema.indicator_value as ema_26,
    i_macd.indicator_value as macd_histogram
  FROM weekly_prices wp
  JOIN symbols s ON s.id = wp.symbol_id
  LEFT JOIN indicators i_ema ON i_ema.symbol_id = wp.symbol_id
    AND i_ema.date = wp.date
    AND i_ema.indicator_name = 'ema_26_weekly'
  LEFT JOIN indicators i_macd ON i_macd.symbol_id = wp.symbol_id
    AND i_macd.date = wp.date
    AND i_macd.indicator_name = 'macd_histogram_weekly'
  WHERE s.symbol IN ('AAPL', 'MSFT', 'GOOGL')
    AND wp.date >= CURRENT_DATE - INTERVAL '14 days'
  ORDER BY s.symbol, wp.date DESC;
"
```

**Expected output:**
```
 symbol | week_start |  close  |  ema_26  | macd_histogram
--------+------------+---------+----------+----------------
 AAPL   | 2026-09-07 |  165.50 |   162.30 |           1.25
 GOOGL  | 2026-09-07 | 2850.00 |  2820.50 |          15.30
 MSFT   | 2026-09-07 |  425.00 |   418.75 |           3.50
(3 rows)
```

**Success criteria:** All symbols have weekly indicators for latest Monday

---

#### 5.8 View Recent Trade History

**Purpose:** Review completed trades and fills

**From command line:**
```bash
psql -U triple_screen -d supertrader_portfolio -c "
  SELECT
    th.action_date,
    p.symbol,
    th.action,
    th.shares,
    th.price,
    th.commission,
    th.notes
  FROM trades_history th
  JOIN positions p ON p.id = th.position_id
  WHERE th.action_date >= CURRENT_DATE - INTERVAL '7 days'
  ORDER BY th.action_date DESC
  LIMIT 10;
"
```

**Expected output:**
```
 action_date | symbol |    action     | shares |  price  | commission |      notes
-------------+--------+---------------+--------+---------+------------+------------------
 2026-09-08  | AAPL   | PARTIAL_SELL  |    100 |  165.00 |       1.00 | 3R partial exit
 2026-09-07  | MSFT   | BUY           |    200 |  320.00 |       1.00 | Screen 3 entry
(2 rows)
```

**Success criteria:** Query runs successfully, verify trades are accurate

---

### Step 6: Execute Multi-Table Diagnostic Query

For complex analysis, use joins across databases (from market data to portfolio):

**Purpose:** Find which symbols have pending signals and recent price action

```bash
psql -U triple_screen -d supertrader_portfolio -c "
  SELECT
    ls.symbol,
    ls.signal_date,
    ls.status,
    ls.expires_at
  FROM live_signals ls
  WHERE ls.status = 'pending'
  ORDER BY ls.signal_date DESC;
" && psql -U triple_screen -d supertrader_market -c "
  SELECT
    s.symbol,
    dp.date,
    dp.close,
    i_atr.indicator_value as atr_14
  FROM daily_prices dp
  JOIN symbols s ON s.id = dp.symbol_id
  LEFT JOIN indicators i_atr ON i_atr.symbol_id = dp.symbol_id
    AND i_atr.date = dp.date
    AND i_atr.indicator_name = 'atr_14_daily'
  WHERE s.symbol IN (
    SELECT symbol FROM live_signals WHERE status = 'pending'
  )
    AND dp.date >= CURRENT_DATE - INTERVAL '5 days'
  ORDER BY s.symbol, dp.date DESC;
"
```

Note: This runs two queries sequentially using `&&` to combine market and portfolio data.

---

### Step 7: Exit Database and Clean Up

1. Exit psql (if in interactive mode):
   ```sql
   \q
   ```

2. Clear password from environment (security best practice):
   ```bash
   unset PGPASSWORD
   ```

3. Exit SSH session:
   ```bash
   exit
   ```

**Success criteria:** Back to your local machine command prompt

---

## Verification

After completing database access, verify success by:

1. All queries returned expected number of rows
2. No authentication errors encountered
3. Data quality checks passed (no NULL values, counts match)
4. Password unset before ending SSH session

**Expected results:**
-  Daily prices loaded for current date (400-507 records)
-  Indicators calculated for all symbols
-  Pending signals list reviewed
-  No data quality issues detected

---

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|----------------|----------|
| `psql: FATAL: password authentication failed` | Incorrect PGPASSWORD or password expired | Verify password, check with admin if reset needed |
| `psql: could not connect to server` | PostgreSQL service down | Check service: `sudo systemctl status postgresql` |
| `permission denied for table` | User lacks SELECT privileges | Contact admin to grant permissions |
| `relation "table_name" does not exist` | Wrong database or schema | Verify connected to correct database (`\c database_name`) |
| Query returns 0 rows when data expected | Data refresh failed or wrong date filter | Check orchestrator logs, verify date filter in WHERE clause |
| `ERROR: column does not exist` | Typo in column name or schema changed | Check DATABASE_SCHEMA.md for correct column names |

**Escalation:**
- Database connection issues persisting >5 minutes → Check VPS status, restart PostgreSQL service
- Data quality issues (missing data) → Review orchestrator logs (SOP-002)
- Schema/permission errors → Contact system administrator

---

## Rollback

This is a read-only procedure (no rollback needed).

**If you accidentally ran a write query:**
1. DO NOT COMMIT (if in transaction)
2. Exit psql immediately: `\q`
3. Restore from backup (see disaster recovery SOP)
4. Contact administrator

---

## Related Documents

- **DATABASE_SCHEMA.md**: Complete schema reference with all tables and columns
- **SOP-001: Daily Data Refresh**: Procedure that populates these databases
- **SOP-002: Restart Services**: How to restart PostgreSQL if connection fails
- **Quick Reference: Database Queries**: One-page cheat sheet of common queries

---

## Change Log

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-09-08 | 1.0 | IB | Initial creation |
