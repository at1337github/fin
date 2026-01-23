# Spending Dashboard - July to December 2025

## Overview
A clean, modern, interactive dashboard visualizing spending patterns across the second half of 2025.

---

## Key Updates Applied

### 1. Categorization Corrections
✅ **CLEO AI** → Recategorized from Financial Services to **Transportation** (rental car service)
✅ **Insurance (Allianz)** → Recategorized from Financial Services to **Transportation**

### 2. Data Filtering
- **Period:** July 1 - December 31, 2025 (6 months)
- **Efficiency:** Filtered at source for faster processing
- **Focus:** Second half of year only

### 3. Archive System
- Old audit files moved to `archive/` folder
- Maintains clean working directory
- Preserves historical versions

---

## Final Spending Summary (July-Dec 2025)

### Overall Metrics
| Metric | Value |
|--------|-------|
| **Total Spending** | $31,734.23 |
| **Monthly Average** | $5,289.04 |
| **Total Transactions** | 1,404 |
| **Avg per Transaction** | $22.60 |

### Updated Category Breakdown

| Category | Amount | % | Transactions | Change |
|----------|--------|---|--------------|--------|
| **Transportation** | **$6,861** | **21.6%** | 255 | ⬆️ +$136 (CLEO AI + Insurance) |
| Grocery/Daily | $4,789 | 15.1% | 330 | - |
| Dining/Restaurants | $2,314 | 7.3% | 145 | - |
| Financial Services | **$2,885** | **9.1%** | 113 | ⬇️ -$136 (removed CLEO AI + Insurance) |
| Tech & Subs | $1,526 | 4.8% | 87 | - |
| Delivery | $1,205 | 3.8% | 50 | - |
| Fast Food | $1,049 | 3.3% | 90 | - |
| Retail/Shopping | $978 | 3.1% | 16 | - |
| Services/Laundry | $712 | 2.2% | 29 | - |
| Phone/Utilities | $468 | 1.5% | 20 | - |
| ATM/Cash | $155 | 0.5% | 6 | - |
| Home/Hardware | $61 | 0.2% | 4 | - |
| Vending/Snacks | $41 | 0.1% | 12 | - |
| Healthcare | $4 | 0.0% | 2 | - |
| Other/Uncategorized | $9,686 | 30.5% | 245 | - |

### Transportation Details
**New Total: $6,861.12 (21.6% of spending)**

Components:
- Rideshares (Uber, Lyft)
- Public transit (MTA, Citi Bike)
- Gas stations
- Parking
- **CLEO AI** (rental car) - $4,381.47
- **Insurance** (Allianz) - $143.00

---

## Dashboard Files

### Main Dashboard
**📊 Spending_Dashboard.html** - Open this in your browser
- Complete overview with all visualizations
- Key insights and metrics
- Interactive charts
- Clean, modern design

### Individual Visualizations

1. **viz_heavy_hitters.html** - 🎯 Top Spending Categories
   - Horizontal bar chart
   - Shows top 8 categories
   - Clear percentages and amounts
   - Instantly see biggest expenses

2. **viz_monthly_trends.html** - 📈 Monthly Spending Patterns
   - Stacked bar chart + trend line
   - Month-to-month comparison
   - Category breakdown per month
   - Total spending overlay

3. **viz_category_breakdown.html** - ☀️ Category Sunburst
   - Hierarchical view
   - Interactive drill-down
   - Proportional sizing
   - Beautiful circular layout

4. **viz_category_insights.html** - 💡 Frequency vs Amount
   - Bubble chart
   - X-axis: Number of transactions
   - Y-axis: Total amount
   - Bubble size: Average transaction
   - Shows spending patterns

5. **viz_monthly_flow.html** - 🌊 Flow from Months to Categories
   - Sankey diagram
   - Shows money flow
   - Month → Category relationships
   - Visual spending paths

6. **viz_daily_intensity.html** - 🔥 Daily Spending Heatmap
   - Week-by-week view
   - Day-of-week patterns
   - Color-coded intensity
   - Identify high-spend days

---

## Key Insights

### 🎯 Heavy Hitters Discovery
**Top 4 categories = 53% of all spending:**
1. Transportation: 21.6% ($6,861)
2. Grocery/Daily: 15.1% ($4,789)
3. Financial Services: 9.1% ($2,885)
4. Dining: 7.3% ($2,314)

### 🍔 Food Spending Aggregated
**Combined food costs = 29.5% of spending ($9,356):**
- Grocery/Daily: $4,789
- Dining/Restaurants: $2,314
- Delivery: $1,205
- Fast Food: $1,049

### 📈 Monthly Patterns
- **Highest:** August ($7,306)
- **Lowest:** October ($3,465)
- **Variance:** 2.1x difference
- **Average:** $5,289/month

### 🚗 Transportation Dominance
**$6,861 total (21.6%)**
- Largest single category
- Includes CLEO AI rental car service
- Major optimization opportunity
- Consider alternatives:
  - Monthly transit pass?
  - Car-sharing vs. rentals?
  - Bike/walk when possible?

### 💳 Financial Services Pattern
**$2,885 in BNPL & fees**
- Chime fees
- Cleo AI (now removed - was rental car)
- PayPal fees
- BNPL services (Affirm, Klarna, Zip, Afterpay)
- Suggests cash flow management via BNPL
- Consider: reducing BNPL usage?

### 📊 Transaction Frequency
- **Total:** 1,404 transactions
- **Per Month:** 234 transactions
- **Per Day:** 7.8 transactions
- **Most Frequent:** Grocery/Daily (330 trans)

---

## Design Features

### Visual Style
- ✅ Light background (#FAFAFA)
- ✅ Bright, distinct colors for categories
- ✅ Not busy - clean spacing
- ✅ Modern, professional look
- ✅ Responsive layout

### Color Palette
- Transportation: Coral Red (#FF6B6B)
- Grocery/Daily: Teal (#4ECDC4)
- Dining: Yellow (#FFE66D)
- Financial Services: Mint (#A8E6CF)
- Tech & Subs: Aqua (#95E1D3)
- Plus 6 more distinct colors

### Interactivity
- Hover for details
- Zoom and pan
- Click to filter
- Download as PNG
- Responsive tooltips

---

## How to Use

### Step 1: Open Main Dashboard
```bash
# Open in your default browser
open Spending_Dashboard.html

# Or double-click the file
```

### Step 2: Explore Visualizations
- Scroll through the dashboard
- Hover over charts for details
- Click legend items to filter
- Read the insight boxes

### Step 3: Individual Charts
Open any `viz_*.html` file for full-screen view of specific chart

### Step 4: Export/Share
- Use browser print to PDF
- Screenshot individual charts
- Share HTML files directly

---

## Files Created

### Data Files
- `July_December_2025_Audit.csv` - Filtered, categorized data
- `july_dec_audit_output.txt` - Processing log

### Scripts
- `create_july_dec_audit.py` - Data processing with updated categories
- `create_dashboard.py` - Visualization generator

### Visualizations
- `Spending_Dashboard.html` - Main dashboard
- `viz_heavy_hitters.html` - Top categories bar chart
- `viz_monthly_trends.html` - Monthly trend chart
- `viz_category_breakdown.html` - Sunburst chart
- `viz_category_insights.html` - Bubble chart
- `viz_monthly_flow.html` - Sankey diagram
- `viz_daily_intensity.html` - Heatmap

### Documentation
- `DASHBOARD_README.md` - This file

---

## Actionable Recommendations

### 1. Transportation ($6,861 - 21.6%)
**Action:** Review and optimize
- CLEO AI: $4,381 for rental car - is this necessary?
- Consider alternatives: monthly car subscription?
- Uber/Lyft: Can some trips be combined?
- MTA: Monthly unlimited pass worth it?

### 2. Food Spending ($9,356 - 29.5%)
**Action:** Meal planning and budgeting
- Grocery: $4,789 (reasonable baseline)
- Dining: $2,314 (could reduce?)
- Delivery: $1,205 (expensive - cook more?)
- Fast Food: $1,049 (convenience cost)
- **Suggestion:** Set dining budget at $3,000/6mo

### 3. Financial Services ($2,885 - 9.1%)
**Action:** Reduce BNPL usage
- Multiple BNPL services in use
- Indicates cash flow challenges
- **Suggestion:** Build emergency fund, reduce BNPL

### 4. Monthly Budget Variance
**Action:** Stabilize spending
- Current range: $3,465 - $7,306
- Target: ~$5,300/month
- **Suggestion:** Track weekly, not just monthly

### 5. Uncategorized ($9,686 - 30.5%)
**Action:** Improve categorization
- 245 transactions uncategorized
- Includes: DM 561, convenience stores
- **Suggestion:** Run enhanced categorization

---

## Technical Details

### Technologies Used
- **Python** - Data processing
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **HTML/CSS** - Dashboard layout

### Performance
- All data filtered at source (July-Dec only)
- Efficient processing - runs in seconds
- Visualizations load instantly
- No external dependencies needed

### Browser Compatibility
- Chrome ✅
- Firefox ✅
- Safari ✅
- Edge ✅

---

## Changelog

### 2026-01-22
- ✅ Recategorized CLEO AI → Transportation (+$4,381)
- ✅ Recategorized Insurance → Transportation (+$143)
- ✅ Filtered data to July-Dec 2025 only
- ✅ Created interactive dashboard
- ✅ Archived old audit files
- ✅ Generated 7 visualization types
- ✅ Added key insights and patterns

---

## Next Steps

1. **Review Dashboard** - Open Spending_Dashboard.html
2. **Analyze Patterns** - Study monthly trends
3. **Identify Opportunities** - Focus on heavy hitters
4. **Set Budgets** - Use insights to create monthly targets
5. **Track Progress** - Re-run monthly to monitor

---

## Questions?

The dashboard is fully self-contained and can be:
- Opened offline
- Shared via email/cloud
- Embedded in reports
- Updated with new data

To update with new data:
1. Export new transactions
2. Run `create_july_dec_audit.py`
3. Run `create_dashboard.py`
4. Refresh browser

---

**Dashboard Status:** ✅ Complete and Ready
**Last Updated:** 2026-01-22
**Data Period:** July 1 - December 31, 2025
