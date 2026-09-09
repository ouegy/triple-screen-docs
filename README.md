# Triple Screen Trading System Documentation

Complete operational documentation for the Triple Screen quantitative trading system implementing Dr. Alexander Elder's methodology with Van K. Tharp position sizing.

## 📚 Documentation

**Live Documentation:** [https://ouegy.github.io/triple-screen-docs](https://ouegy.github.io/triple-screen-docs)

## What's Included

### VPS Operations (SOPs)
- Service Management - systemd service control and troubleshooting
- Log Monitoring - journalctl commands and log analysis
- Database Access - PostgreSQL queries and data verification
- Email Alert Response - CRITICAL/WARNING/INFO alert triage

### Dashboard Guides
- Navigation - Streamlit dashboard overview
- Watchlist Management - Weekly relative strength scanning
- Daily Signal Removal - Discretionary signal filtering (9:00-9:25 AM ET)
- Trade Journaling - Apgar scoring and documentation
- Performance Metrics - R-multiples, expectancy, portfolio heat

### Quick Reference
- VPS Commands - Essential systemctl, journalctl, psql commands
- Database Queries - 26 copy-paste queries for troubleshooting

### Training
- New Operator Onboarding - Comprehensive 4-6 hour training curriculum

## Local Development

```bash
# Install dependencies
pip install mkdocs-material

# Run local server
mkdocs serve

# Build static site
mkdocs build
```

## Deployment

Documentation is automatically deployed to GitHub Pages via GitHub Actions on push to `main` branch.

## Contributing

This documentation was created to demonstrate:
- Clear, engaging technical writing
- Practical SOPs and operational guides
- Professional documentation standards
- AI-enabled tool support

## License

© 2026 Ian Butler. All rights reserved.
