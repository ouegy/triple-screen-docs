# Database Query Quick Reference

**Version:** 1.0 | **Last Updated:** 2026-09-08

---

## Connection Quick Start

```bash
# Export password + connect to market database (one-liner)
export PGPASSWORD='your_db_password' && psql -U triple_screen -d supertrader_market

# Export password + connect to portfolio database (one-liner)
export PGPASSWORD='your_db_password' && psql -U triple_screen -d supertrader_portfolio

# Clean up (unset password when done)
unset PGPASSWORD
```

---

## Data Quality Checks

| Check | Query | Expected Output |
|-------|-------|-----------------|
| **Today's data loaded** | `psql -U triple_screen -d supertrader_market -c "SELECT COUNT(*) as record_count FROM daily_prices WHERE date = CURRENT_DATE;"` | `record_count` = 400-507 |
| **Find NaN/NULL values** | `psql -U triple_screen -d supertrader_market -c "SELECT s.symbol, dp.date, dp.close, dp.volume FROM daily_prices dp JOIN symbols s ON s.id = dp.symbol_id WHERE dp.date = CURRENT_DATE AND (dp.close IS NULL OR dp.volume IS NULL) LIMIT 20;"` | 0 rows (no NULLs) |
| **Verify ATR calculated** | `psql -U triple_screen -d supertrader_market -c "SELECT COUNT(DISTINCT symbol_id) FROM indicators WHERE date = CURRENT_DATE AND indicator_name = 'atr_14_daily';"` | Matches symbol count |
| **Verify EMA calculated** | `psql -U triple_screen -d supertrader_market -c "SELECT COUNT(DISTINCT symbol_id) FROM indicators WHERE date = CURRENT_DATE AND indicator_name = 'ema_13_daily';"` | Matches symbol count |
| **Count rows by date** | `psql -U triple_screen -d supertrader_market -c "SELECT date, COUNT(*) as records FROM daily_prices WHERE date >= CURRENT_DATE - INTERVAL '7 days' GROUP BY date ORDER BY date DESC;"` | ~500 per date |
| **Weekly indicators latest** | `psql -U triple_screen -d supertrader_market -c "SELECT COUNT(DISTINCT symbol_id) FROM indicators WHERE indicator_name IN ('ema_26_weekly', 'macd_histogram_weekly') AND date >= CURRENT_DATE - INTERVAL '7 days';"` | 400-507 per indicator |

---

## Signal & Position Queries

| Task | Query | Expected Output |
|------|-------|-----------------|
| **List pending signals** | `psql -U triple_screen -d supertrader_portfolio -c "SELECT id, symbol, signal_date, status, expires_at FROM live_signals WHERE status = 'pending' ORDER BY signal_date DESC;"` | Active signals awaiting Screen 3 |
| **View open positions** | `psql -U triple_screen -d supertrader_portfolio -c "SELECT lp.symbol, p.entry_date, p.entry_price, lp.current_price, lp.unrealized_pnl, lp.unrealized_r, lp.stop_type FROM live_positions lp JOIN positions p ON p.id = lp.position_id ORDER BY lp.unrealized_r DESC;"` | Live positions with P&L |
| **Recent trades (7 days)** | `psql -U triple_screen -d supertrader_portfolio -c "SELECT th.action_date, p.symbol, th.action, th.shares, th.price, th.commission FROM trades_history th JOIN positions p ON p.id = th.position_id WHERE th.action_date >= CURRENT_DATE - INTERVAL '7 days' ORDER BY th.action_date DESC LIMIT 10;"` | Recent fills |
| **Check signal expiration** | `psql -U triple_screen -d supertrader_portfolio -c "SELECT symbol, expires_at, EXTRACT(EPOCH FROM (expires_at - NOW()))/3600 AS hours_remaining FROM live_signals WHERE status = 'pending' AND expires_at > NOW() ORDER BY expires_at;"` | Hours until expiration |
| **Today's triggered signals** | `psql -U triple_screen -d supertrader_portfolio -c "SELECT symbol, signal_date, updated_at FROM live_signals WHERE status = 'triggered' AND signal_date::date = CURRENT_DATE;"` | Signals entered today |
| **Position count by status** | `psql -U triple_screen -d supertrader_portfolio -c "SELECT status, COUNT(*) FROM positions GROUP BY status;"` | Open/closed/cancelled counts |

---

## Common Troubleshooting Queries

| Issue | Query | Expected Output |
|-------|-------|-----------------|
| **Symbols missing today's data** | `psql -U triple_screen -d supertrader_market -c "SELECT s.symbol FROM symbols s WHERE s.is_active = true AND NOT EXISTS (SELECT 1 FROM daily_prices dp WHERE dp.symbol_id = s.id AND dp.date = CURRENT_DATE) LIMIT 20;"` | 0 rows (all symbols present) |
| **Last successful data refresh** | `psql -U triple_screen -d supertrader_market -c "SELECT MAX(date) as last_refresh, COUNT(DISTINCT symbol_id) as symbols FROM daily_prices;"` | Today's date + symbol count |
| **Database size/disk usage** | `psql -U triple_screen -d supertrader_market -c "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) AS size FROM pg_database WHERE datname IN ('supertrader_market', 'supertrader_portfolio');"` | DB sizes in MB/GB |
| **Gaps in daily data (30d)** | `psql -U triple_screen -d supertrader_market -c "WITH date_series AS (SELECT generate_series(CURRENT_DATE - INTERVAL '30 days', CURRENT_DATE, '1 day'::interval)::date AS expected_date) SELECT ds.expected_date, s.symbol FROM date_series ds CROSS JOIN symbols s LEFT JOIN daily_prices dp ON dp.symbol_id = s.id AND dp.date = ds.expected_date WHERE s.symbol = 'AAPL' AND dp.date IS NULL AND EXTRACT(DOW FROM ds.expected_date) NOT IN (0,6) ORDER BY ds.expected_date;"` | 0 rows (no gaps) |
| **Indicator calculation lag** | `psql -U triple_screen -d supertrader_market -c "SELECT COUNT(DISTINCT dp.symbol_id) as symbols_with_prices, COUNT(DISTINCT i_atr.symbol_id) as symbols_with_atr, COUNT(DISTINCT i_ema.symbol_id) as symbols_with_ema FROM daily_prices dp LEFT JOIN indicators i_atr ON i_atr.symbol_id = dp.symbol_id AND i_atr.date = dp.date AND i_atr.indicator_name = 'atr_14_daily' LEFT JOIN indicators i_ema ON i_ema.symbol_id = dp.symbol_id AND i_ema.date = dp.date AND i_ema.indicator_name = 'ema_13_daily' WHERE dp.date = CURRENT_DATE;"` | All counts equal |
| **Check IBKR position sync** | `psql -U triple_screen -d supertrader_portfolio -c "SELECT symbol, ibkr_position_size, last_sync, EXTRACT(EPOCH FROM (NOW() - last_sync))/60 AS minutes_since_sync FROM live_positions WHERE ibkr_position_size IS NOT NULL ORDER BY last_sync DESC;"` | Sync within last 5 minutes |

---

## Key Tables

| Database | Table | Purpose |
|----------|-------|---------|
| market | symbols | Symbol universe |
| market | daily_prices | OHLCV bars |
| market | indicators | ATR/EMA/MACD |
| portfolio | live_signals | Pending signals |
| portfolio | live_positions | Open positions |
| portfolio | trades_history | All fills |

**Full schema:** [DATABASE_SCHEMA.md](../../backend/DATABASE_SCHEMA.md)

---

## Related Documents

- **Full Procedures:** [SOP-003: Database Access and Queries](../SOPs/SOP-003-database-access.md)
- **Schema Details:** [DATABASE_SCHEMA.md](../../backend/DATABASE_SCHEMA.md)
- **Data Validation:** [alerts.py](../../backend/src/monitoring/alerts.py) - Query examples in alert templates

---

**Document Owner:** Ian Butler
**Feedback:** Open GitHub issue or contact via project channels
**Next Review:** 2026-12-08
