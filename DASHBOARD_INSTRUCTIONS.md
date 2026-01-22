# How to Use the Unified Dashboard

## Quick Start (3 steps)

1. **Open the dashboard**
   - Double-click: `unified-dashboard-ultimate.html`
   - Or right-click → Open With → Browser

2. **Upload your data**
   - Click "Choose CSV File" button (top right)
   - Select: `dashboard_data.csv`

3. **Explore!**
   - Dashboard loads automatically with all visualizations

---

## What You'll See

### 📊 Key Metrics (Top Cards)
- **Total Spend:** $30,917 (July-Dec 2025)
- **Monthly Burn:** ~$5,153/month
- **Transaction Count:** 1,390
- **Income:** (if any)

### 🎯 Top Category Trends
Mini charts showing spending trends for:
- Groceries (16.1%)
- Rideshare (12.6%)
- Dining Out (12.0%)
- Services (9.3%)
- Shopping (6.8%)
- Food Delivery (5.7%)

### 📈 Multiple Visualizations
1. **Comparison Chart** - Current vs previous 3 months
2. **Stacked Area Chart** - Spending over time by category
3. **Category Drivers** - What's driving your spending
4. **Sankey Diagram** - Flow from groups to categories
5. **Pareto Chart** - 80/20 rule visualization
6. **Trend Analysis** - Monthly patterns

---

## Data Format

### What's Included
✅ July - December 2025 transactions
✅ 1,390 spending transactions
✅ 90.2% categorized
✅ Negative amounts (spending)

### What's Excluded
❌ P2P transfers (14 transactions)
❌ ATM withdrawals
❌ REB NYC (rent)
❌ CLEO AI marked as rental car
❌ Pending/Failed/Reversed transactions

### Categories Used
**Main Groups:**
- Groceries (16.1%)
- Rideshare - Uber (12.6%)
- Dining Out (12.0%)
- Services (9.3%)
- Shopping (6.8%)
- Food Delivery (5.7%)
- Subscriptions (4.7%)
- Bills & Housing (4.1%)
- Transportation (4.1%)
- Travel (3.4%)
- Car Rental (3.4%)
- Other (9.8%)

---

## Key Insights to Look For

### 🚗 Transportation
- **Rideshare:** $3,901 (12.6%) - Uber/Lyft dominating
- **Car Rental:** $1,047 (3.4%) - CLEO AI rental car
- **Transit:** Included in Transportation group
- **Total transport:** ~20% of spending

### 🍔 Food Spending
- **Groceries:** $4,988 (16.1%)
- **Dining Out:** $3,710 (12.0%)
- **Food Delivery:** $1,753 (5.7%)
- **Total food:** 33.8% of spending

### 💳 Services & Fees
- **Services:** $2,885 (9.3%)
- Includes BNPL, PayPal fees, financial services
- Consider reducing BNPL usage

### 🛍️ Shopping
- **Shopping:** $2,098 (6.8%)
- Clothing, electronics, general retail
- Check if necessary vs. discretionary

---

## Interactive Features

### Hover
- Move mouse over any chart element
- See exact amounts and details
- View percentages and trends

### Click
- Click legend items to show/hide categories
- Click chart elements to drill down
- Double-click to reset zoom

### Comparison
- Dashboard automatically compares recent 3 months vs previous 3 months
- Shows increase/decrease with percentages
- Identifies spending changes

---

## Troubleshooting

### Dashboard won't load?
1. Make sure you have internet connection (needs CDN libraries)
2. Use a modern browser (Chrome, Firefox, Safari, Edge)
3. Enable JavaScript if disabled

### Data won't upload?
1. Make sure you're selecting `dashboard_data.csv`
2. File should be in same folder as HTML
3. Check browser console for errors (F12)

### Numbers look wrong?
- All amounts are absolute values (no negative signs in charts)
- Spending shown as positive numbers
- Income shown separately

### Want different date range?
Edit `prepare_dashboard_data.py`:
- Modify date filter
- Re-run: `python3 prepare_dashboard_data.py`
- Upload new `dashboard_data.csv`

---

## Files Explanation

### unified-dashboard-ultimate.html
- The polished dashboard (provided by you)
- Self-contained with all visualizations
- Uses Chart.js and D3.js
- Modern, clean design

### dashboard_data.csv
- Your spending data (July-Dec 2025)
- Properly formatted and categorized
- Ready to upload to dashboard
- 1,390 transactions

### prepare_dashboard_data.py
- Script that creates dashboard_data.csv
- Comprehensive categorization logic
- Filters out transfers and ATM
- Run again for updated data

---

## What Changed from Before

### Better Categorization
✅ **90.2% categorized** (vs 70% uncategorized before)
- Groceries properly identified
- Hotels categorized as Travel
- Clothing items as Shopping
- Gas stations as Transportation
- Laundry, moving, shipping as Services

### Proper Format
✅ **Matches dashboard expectations:**
- Date, Description, Amount, Group, Category columns
- Negative amounts for spending
- Hierarchical categories (Group → Category)
- Last 6 months of data

### Clean Data
✅ **Excluded noise:**
- P2P transfers removed
- ATM withdrawals removed
- Only true merchant spending
- $30,917 total (down from $31,734 after exclusions)

---

## Recommendations Based on Data

### 🎯 Focus Areas

**1. Transportation (20% of spending)**
- Rideshare: $3,901 - Can trips be combined?
- Car Rental: $1,047 - Is CLEO AI necessary?
- Consider: monthly transit pass, car-sharing alternatives

**2. Food (34% of spending)**
- Groceries: $4,988 - Reasonable baseline
- Dining Out: $3,710 - Opportunity to reduce?
- Delivery: $1,753 - Expensive convenience
- **Action:** Meal prep, reduce delivery frequency

**3. Services/Fees (9.3%)**
- BNPL and fees: $2,885
- **Action:** Build emergency fund, reduce BNPL reliance

---

## Next Steps

1. ✅ **Open dashboard** - Load unified-dashboard-ultimate.html
2. ✅ **Upload data** - Select dashboard_data.csv
3. 📊 **Analyze patterns** - Study the visualizations
4. 🎯 **Identify opportunities** - Where to optimize?
5. 💰 **Set budgets** - Based on insights
6. 📈 **Track progress** - Re-run monthly

---

## Support

If something doesn't work:
1. Check browser console (F12 → Console tab)
2. Verify CSV format (open in Excel/text editor)
3. Ensure internet connection for CDN libraries
4. Try different browser

The dashboard is designed to load your data automatically and provide immediate insights. Enjoy exploring your spending patterns! 📊💰
