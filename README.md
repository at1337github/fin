# Fin - Financial Transaction Analysis & Dashboard

## Overview
Comprehensive financial transaction analysis system combining PayPal (Personal & Business) and Cash App data. This project provides data cleaning, categorization, audit verification, and an interactive spending dashboard for July-December 2025 transactions.

## Project Purpose
- ✅ **Verify data accuracy**: 99.98% match rate between audit and source files
- ✅ **Clean & deduplicate**: Remove authorization holds, pending transactions, duplicates
- ✅ **Categorize spending**: 90.2% of transactions automatically categorized
- ✅ **Exclude transfers**: Filter out P2P transfers, ATM withdrawals, Apple Cash transfers
- ✅ **Visualize insights**: Interactive dashboard with 8 different charts and analytics

## Quick Start

### 🚀 View Your Spending Dashboard
**Just open this file in any browser:**
```bash
open spending-dashboard.html
```

✅ No setup needed • ✅ Works offline • ✅ Mobile Safari compatible

See `SPENDING_DASHBOARD_GUIDE.md` for full documentation.

### 📊 Dashboard Highlights
- **Time Period**: July - December 2025 (6 months)
- **Total Spending**: $30,917
- **Top Category**: Groceries (16.1%, $4,988)
- **Transactions**: 1,390 categorized transactions
- **Visualizations**: Sankey flow, Pareto chart, trend analysis, category drivers, and more

## 📁 Repository Structure

### 📊 Dashboards (Ready to Use)
- **spending-dashboard.html** (265KB) - Self-contained dashboard with embedded data
  - Works offline, no file upload needed
  - Mobile Safari optimized
  - 8 interactive visualizations
- **unified-dashboard-ultimate.html** - Template for dashboard generation

### 📄 Documentation
- **SPENDING_DASHBOARD_GUIDE.md** - Complete dashboard usage guide
- **GITHUB_WORKFLOW_GUIDE.md** - Branch management & GitHub Desktop sync workflow
- **DASHBOARD_INSTRUCTIONS.md** - Dashboard viewing instructions
- **AUDIT_CLEANING_LOGIC.md** - Data cleaning methodology
- **README.md** - This file

### 💾 Current Data Files
- **July_December_2025_Audit.csv** (1,404 rows) - Current audit for July-Dec 2025
- **dashboard_data.csv** (1,390 rows) - Formatted data for dashboard
- **PayPal_True_Spend_Audit.csv** (9,151 rows) - Original full PayPal audit

### 📥 Source Files
- **personal-6.CSV** (4,818 rows) - Personal PayPal transactions
- **Download-6.CSV** (4,334 rows) - Business PayPal transactions
- **cash_app_report_1741759362166.csv** (1,050 rows) - Cash App report #1
- **cash_app_report_1746328330627.csv** (1,203 rows) - Cash App report #2

### 🐍 Active Scripts
- **analyze_paypal.py** - Verify PayPal audit accuracy (99.98% match rate)
- **prepare_dashboard_data.py** - Prepare and categorize data for dashboard
- **create_july_dec_audit.py** - Filter audit to July-Dec 2025
- **create_embedded_dashboard.py** - Generate self-contained dashboard
- **archive_old_versions.sh** - Automatic file archiving script

### 🗄️ Archive Directory
Historical versions of files organized in subdirectories:
- `archive/old_scripts/` - Previous Python script versions (6 files)
- `archive/old_docs/` - Superseded documentation (7 files)
- `archive/old_data/` - Historical audit files (5 files)
- `archive/old_dashboards/` - Old dashboard versions (1 file)
- `archive/output_logs/` - Script execution logs (6 files)

See `archive/README.md` for details.

## 📈 Key Insights (July-Dec 2025)

### Top Spending Categories
1. **Groceries** - $4,988 (16.1%) - Supermarkets, delis, convenience stores
2. **Rideshare (Uber)** - $3,901 (12.6%) - Major transportation expense
3. **Dining Out** - $3,710 (12.0%) - Restaurants, fast food, cafes
4. **Services** - $2,885 (9.3%) - BNPL, PayPal fees, financial services
5. **Shopping** - $2,098 (6.8%) - Clothing, electronics, retail

### Combined Categories
- **Food Total**: $10,451 (33.8%) - Groceries + Dining + Delivery
- **Transportation Total**: $6,195 (20.1%) - Rideshare + Car Rental + Transit

### Data Quality
- **Audit Accuracy**: 99.98% match rate between audit and source files
- **Categorization**: 90.2% of transactions categorized (9.8% "Other")
- **Deduplication**: 27.7% of raw transactions removed (auth holds, pending, duplicates)
- **Exclusions**: P2P transfers, ATM withdrawals, Apple Cash transfers excluded

## 🚀 How to Use

### View Spending Dashboard
**No installation required!**
```bash
# Just open the dashboard file
open spending-dashboard.html
```

The dashboard shows:
- KPI cards (total spend, income, monthly burn, net cash flow)
- Category trend comparisons (recent vs previous 3 months)
- Sankey flow diagram showing money movement
- Pareto chart (80/20 spending concentration)
- Monthly trends and patterns
- Top spending categories with merchant details

### Run Data Analysis

**Prerequisites:**
```bash
pip install -r requirements.txt  # pandas
```

**Verify PayPal Audit Accuracy:**
```bash
python3 analyze_paypal.py
```

**Regenerate Dashboard Data:**
```bash
# 1. Prepare and categorize data
python3 prepare_dashboard_data.py

# 2. Create embedded dashboard
python3 create_embedded_dashboard.py

# 3. Open new dashboard
open spending-dashboard.html
```

**Archive Old Files:**
```bash
# Preview what will be archived
./archive_old_versions.sh --dry-run

# Actually archive old versions
./archive_old_versions.sh
```

## 🔧 Data Processing Pipeline

### 1. Source Data Collection
- **PayPal Personal**: personal-6.CSV (4,818 transactions)
- **PayPal Business**: Download-6.CSV (4,334 transactions)
- **Cash App**: 2 report files (2,253 transactions combined)

### 2. Data Cleaning
- Remove authorization holds (keep settlements only)
- Exclude pending/denied/failed/reversed transactions
- Deduplicate exact matches
- Filter out non-spending (refunds, deposits, money in)
- Exclude transfers (P2P, ATM, Apple Cash, rent payments)

### 3. Categorization
Uses comprehensive keyword matching for:
- **Groceries**: Supermarkets, delis, convenience stores
- **Dining & Cafes**: Restaurants, fast food, coffee shops, delivery
- **Transportation**: Rideshare, car rental, transit, gas, parking
- **Subscriptions**: Apple Services, streaming, software, memberships
- **Bills & Housing**: Phone, utilities, insurance, laundry
- **Shopping**: Clothing, electronics, retail
- **Travel**: Hotels, flights, travel expenses
- **Services**: BNPL (Affirm, Klarna), fees, professional services
- **Health & Wellness**: Pharmacy, medical, fitness

### 4. Dashboard Generation
- Embed categorized data as JSON
- Generate 8 interactive visualizations
- Optimize for mobile Safari
- Self-contained, works offline

## 🌿 Branch Management

**Current Branch**: `claude/enhance-docs-review-u03EV` (clean, organized, latest)

**To make this the default branch:**
1. Go to GitHub.com → Settings → Branches
2. Change default branch to `claude/enhance-docs-review-u03EV`

**To sync with GitHub Desktop:**
1. Fetch origin (check for updates)
2. Pull origin (download updates)
3. Work on files
4. Commit changes
5. Push origin (upload changes)

See `GITHUB_WORKFLOW_GUIDE.md` for complete instructions.

## 🗄️ Automatic Archiving

**Archive old file versions automatically:**
```bash
./archive_old_versions.sh
```

This moves files matching patterns like `*_old.py`, `*_backup.csv`, `*_output.txt` to organized archive subdirectories.

**Enable automatic archiving before every commit:**
```bash
cp .git/hooks/pre-commit-archive-example .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

See archive/README.md for retention policy and archive structure.

## 📚 Documentation

- **SPENDING_DASHBOARD_GUIDE.md** - Dashboard features, insights, and mobile usage
- **GITHUB_WORKFLOW_GUIDE.md** - Branch management and GitHub Desktop workflow
- **DASHBOARD_INSTRUCTIONS.md** - Dashboard viewing and interpretation
- **AUDIT_CLEANING_LOGIC.md** - Data cleaning and categorization methodology
- **archive/README.md** - Archive structure and retention policy

## ❓ Questions or Issues?

**Dashboard not loading?**
- Ensure JavaScript enabled in browser
- Check browser console for errors (F12)
- Try Safari or Chrome
- See SPENDING_DASHBOARD_GUIDE.md troubleshooting section

**Data looks wrong?**
- Verify source files are correct
- Check date range (currently July-Dec 2025)
- Review categorization logic in prepare_dashboard_data.py
- Excluded transfers won't appear (P2P, ATM, Apple Cash)

**Sync issues with GitHub?**
- Always fetch before pulling
- Commit changes before switching branches
- See GITHUB_WORKFLOW_GUIDE.md for complete workflow

---

## ✅ Completed Features

✅ 99.98% audit accuracy verification
✅ Comprehensive data cleaning and deduplication
✅ 90.2% automatic transaction categorization
✅ Self-contained interactive dashboard (no upload needed)
✅ Mobile Safari optimization
✅ Organized archive with historical files
✅ Automatic archiving script
✅ Complete documentation and workflow guides

**Ready to use!** Just open `spending-dashboard.html` 📊