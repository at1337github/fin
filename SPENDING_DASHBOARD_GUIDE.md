# Spending Dashboard Guide

## Quick Start - Just Open the File!

**Simply open this file in any browser:**
```
spending-dashboard.html
```

✅ **No file upload needed** - Data is embedded directly
✅ **Works offline** - No internet required after first load
✅ **Mobile Safari compatible** - Optimized for iPhone/iPad
✅ **Auto-loads** - Dashboard appears immediately

---

## What's Inside

### 📊 Your Data
- **Time Period:** July - December 2025 (6 months)
- **Transactions:** 1,390 spending transactions
- **Total Amount:** $30,917
- **Categorization:** 90.2% categorized (9.8% uncategorized)

### 🎯 Key Metrics (Top Cards)
The dashboard shows 5 key performance indicators:
- **Total Spend:** All spending for the 6-month period
- **Total Income:** Any income/refunds received
- **Monthly Burn:** Average spending per month
- **Net Cash Flow:** Income minus spending
- **Transaction Count:** Total number of transactions

### 📈 Visualizations

#### 1. **Category Trend Cards** (Recent vs Previous 3 Months)
Mini sparkline charts showing top categories:
- Groceries (16.1%)
- Rideshare - Uber (12.6%)
- Dining Out (12.0%)
- Services (9.3%)
- Shopping (6.8%)
- Food Delivery (5.7%)

Each card shows:
- Recent 3-month spending vs previous 3 months
- Percentage change (↑ increase / ↓ decrease)
- Visual trend line

#### 2. **Comparison Chart** (Current vs Previous Period)
Side-by-side bar chart comparing:
- Recent 3 months (Oct-Dec 2025)
- Previous 3 months (Jul-Sep 2025)
- Shows which categories increased/decreased

#### 3. **Stacked Area Chart** (Spending Over Time)
Shows how spending flows across months:
- Each color = different category
- Height = total spending that month
- See spending patterns and trends

#### 4. **Category Drivers** (What's Driving Your Spending)
Cards showing top 6 spending categories with:
- Total amount and percentage
- Number of transactions
- Average per transaction
- Top merchants in that category

#### 5. **Sankey Diagram** (Expenditure Flow)
Visual flow showing:
- Total Spend → Category Groups → Specific Categories
- Width of lines = amount of money
- See how money flows through categories

#### 6. **Pareto Chart** (80/20 Rule)
Shows cumulative spending:
- Which categories contribute most
- Typically 20% of categories = 80% of spending
- Identifies where to focus optimization

#### 7. **Monthly Trend Analysis**
Line chart showing:
- Monthly spending totals
- Monthly income
- Month-to-month patterns

---

## Top Spending Categories

Based on your July-December 2025 data:

1. **Groceries** - $4,988 (16.1%)
   - Supermarkets, delis, convenience stores
   - Essential spending baseline

2. **Rideshare - Uber** - $3,901 (12.6%)
   - Uber/Lyft rides
   - Major transportation expense

3. **Dining Out** - $3,710 (12.0%)
   - Restaurants, fast food, cafes
   - Opportunity to reduce with meal planning

4. **Services** - $2,885 (9.3%)
   - BNPL payments, PayPal fees, financial services
   - Consider reducing BNPL usage

5. **Shopping** - $2,098 (6.8%)
   - Clothing, electronics, retail
   - Check if necessary vs discretionary

6. **Food Delivery** - $1,753 (5.7%)
   - DoorDash, Uber Eats, etc.
   - Expensive convenience premium

7. **Subscriptions** - $1,467 (4.7%)
   - Apple Services, streaming, software
   - Review and cancel unused subscriptions

8. **Bills & Housing** - $1,266 (4.1%)
   - Phone, utilities, insurance, laundry

9. **Transportation** - $1,265 (4.1%)
   - Transit, gas, parking (excluding rideshare)

10. **Travel** - $1,047 (3.4%)
    - Hotels, travel expenses

11. **Car Rental** - $1,047 (3.4%)
    - CLEO AI rental car service

**Combined Transportation = 20.1%** (Rideshare + Car Rental + Transit)
**Combined Food = 33.8%** (Groceries + Dining + Delivery)

---

## Interactive Features

### Hover
- Move mouse over any chart element
- See exact amounts, percentages, details
- Tooltips show additional context

### Click
- Click legend items to show/hide categories
- Focus on specific categories
- Double-click to reset

### Mobile Touch
- Tap any chart element for details
- Swipe to scroll through data
- Pinch to zoom (where applicable)

---

## Insights & Recommendations

### 🚗 Transportation (20.1% - $6,195)
**Issue:** Single largest spending area
- Rideshare: $3,901
- Car Rental (CLEO AI): $1,047
- Transit/Gas: $1,265

**Actions:**
- Can Uber/Lyft trips be combined or reduced?
- Is CLEO AI rental car necessary vs alternatives?
- Consider monthly transit pass vs per-trip

### 🍔 Food (33.8% - $10,451)
**Issue:** Over 1/3 of all spending
- Groceries: $4,988 (reasonable baseline)
- Dining Out: $3,710 (opportunity)
- Delivery: $1,753 (expensive convenience)

**Actions:**
- Meal prep to reduce dining out frequency
- Limit delivery to 1-2x per week
- Pack lunch/snacks to avoid impulse purchases

### 💳 Services/Fees (9.3% - $2,885)
**Issue:** BNPL and financial service fees
- Affirm, Klarna, PayPal fees

**Actions:**
- Build emergency fund to reduce BNPL reliance
- Pay upfront when possible to avoid fees
- Review all BNPL commitments

### 📦 Subscriptions (4.7% - $1,467)
**Issue:** Recurring charges add up
- Apple Services, streaming, software

**Actions:**
- Audit all subscriptions monthly
- Cancel services you don't actively use
- Share family plans where possible

---

## Mobile Safari Specific Features

### ✅ Optimizations Applied
- **Smooth scrolling** with -webkit-overflow-scrolling
- **No tap flash** - Disabled gray tap highlight
- **Safe area support** - Works with iPhone notch
- **Responsive charts** - Adapt to screen size
- **Touch-friendly** - Large tap targets

### 📱 Best Viewing Practices
1. **Orientation:** Landscape recommended for charts
2. **Zoom:** Pinch to zoom for details
3. **Full screen:** Add to home screen for app-like experience
4. **Connection:** Internet required only for first load (CDN libraries)

### 🔧 Troubleshooting on iOS

**Dashboard won't load?**
- Ensure internet connection (CDN libraries needed)
- Try Safari private mode
- Clear Safari cache (Settings → Safari → Clear History)
- Update to latest iOS version

**Charts not showing?**
- Refresh page (pull down)
- Check JavaScript is enabled (Settings → Safari → Advanced)
- Disable content blockers temporarily

**Performance slow?**
- Close other Safari tabs
- Restart Safari app
- Free up device memory

---

## Technical Details

### Data Format
```csv
Date,Description,Amount,Group,Category
12/31/2025,MTA*NYCT PAYGO,-2.9,Transportation,Transit - Subway/Bus
12/31/2025,Uber Technologies Inc,-24.93,Rideshare - Uber,Rideshare - Uber
```

### Data Exclusions
❌ P2P transfers (person-to-person payments)
❌ ATM withdrawals
❌ Apple Cash balance transfers
❌ REB NYC (rent payments)
❌ Pending/Failed/Reversed transactions

### Libraries Used
- **Chart.js 4.4.1** - Bar, line, area charts
- **D3.js v7** - Sankey diagram
- **PapaParse 5.4.1** - CSV parsing (not used, but included)
- **Google Fonts** - Inter & JetBrains Mono

### File Size
- **spending-dashboard.html:** ~265 KB
- Includes all 1,390 transactions embedded as JSON
- Self-contained, works offline after initial load

---

## Updates & Maintenance

### To Update Data
1. Run `python3 prepare_dashboard_data.py` with new CSV
2. Run `python3 create_embedded_dashboard.py`
3. New `spending-dashboard.html` will be generated

### To Modify Visualizations
- Edit `unified-dashboard-ultimate.html` template
- Re-run `create_embedded_dashboard.py`
- Changes will be applied to new dashboard

### To Change Date Range
- Edit date filter in `prepare_dashboard_data.py`
- Re-run preparation and embedding scripts

---

## Privacy & Security

✅ **Local-only** - No data sent to external servers
✅ **Offline-capable** - Works without internet after first load
✅ **No tracking** - No analytics or third-party scripts
✅ **Self-contained** - All data embedded in HTML file

**Share safely:**
- File contains your full transaction history
- Only share with trusted individuals
- Consider password-protecting if emailing

---

## Quick Actions

### Want to reduce spending?
1. **Focus on top 3 categories** (20% of categories = 80% of spending)
2. **Set category budgets** based on insights
3. **Track progress monthly** by re-running analysis

### Want different visualizations?
- Stacked area shows trends over time
- Sankey shows category relationships
- Pareto shows concentration
- Choose what resonates with you

### Want to compare periods?
- Comparison chart shows recent vs previous 3 months
- See if spending is increasing/decreasing
- Identify seasonal patterns

---

## Support

**Dashboard not working?**
1. Check browser console for errors (F12 → Console)
2. Verify all CDN libraries loaded
3. Ensure JavaScript enabled
4. Try different browser

**Need help interpreting data?**
- Focus on visualizations that resonate
- Start with "Category Drivers" card
- Look at Sankey for big picture
- Use Comparison chart to see changes

**Want custom analysis?**
- Raw data available in `dashboard_data.csv`
- Use Excel/Google Sheets for custom pivots
- Filter by merchant, date, or amount

---

## Version History

**v2.0 (Current)** - Embedded Data Version
- ✅ No file upload needed
- ✅ Data embedded directly
- ✅ Mobile Safari optimized
- ✅ Fixed date filtering bug
- ✅ Auto-loads on open

**v1.0** - File Upload Version
- ❌ Required CSV upload
- ❌ Mobile compatibility issues
- ❌ Extra user interaction needed

---

**Just open `spending-dashboard.html` and start exploring your spending! 📊💰**
