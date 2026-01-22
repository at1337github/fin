# Fin - PayPal Transaction Audit Analysis

## Overview
This project analyzes the relationship between PayPal transaction audit files and their source data files. The primary goal is to understand data lineage, identify additional data sources, verify audit accuracy, and ensure data consistency across all PayPal transaction records.

## Project Purpose
The analysis helps answer critical questions:
- How does the audit file relate to source transaction files?
- Are there additional, undocumented data sources contributing to the audit?
- Is the audit process accurate and complete?
- What transactions are included, excluded, or missing?

## Files in Repository

### Data Files
- **PayPal_True_Spend_Audit.csv** (9,151 rows) - Processed audit file with analysis status, exclusions, and categorization
- **personal-6.CSV** (4,818 rows) - Raw personal PayPal transaction export
- **business_paypal-6.CSV** (0 bytes) - Empty business account file (potential missing data source)

### Analysis Scripts
- **analyze_paypal.py** - Comprehensive Python analysis script that:
  - Loads and compares audit and source files
  - Identifies transaction matches and discrepancies
  - Detects additional data sources
  - Analyzes data quality and consistency
  - Generates detailed reports

## Data Structure

### Audit File Columns
- Date, Name, Amount
- Analysis_Status (Excluded, Included, etc.)
- Exclusion_Reason (Transfer/Noise, Money In/Refund, etc.)
- Category (Excluded, Spending, etc.)
- Source (Business/Main, Personal, etc.)
- Type (Mobile Payment, Card Deposit, etc.)
- Status (Completed, Denied, etc.)

### Personal Transaction File Columns
- Date, Time, TimeZone
- Name, Type, Status
- Currency, Gross, Fees, Total
- Exchange Rate, Receipt ID, Balance
- Transaction ID, Item Title

## How to Run Analysis

### Prerequisites
```bash
# Install Python 3.x and pandas
pip install pandas
```

### Execute Analysis
```bash
# Run the analysis script
python3 analyze_paypal.py

# Or make it executable and run
chmod +x analyze_paypal.py
./analyze_paypal.py
```

### Output
The script generates:
- Detailed console output with transaction comparisons
- Structure analysis of both files
- Data quality assessment
- **ANALYSIS_REPORT.txt** - Summary report file

## Key Analysis Tasks

### 1. Data Relationship Analysis
- Compare audit file transactions with source files
- Match transactions by date and amount
- Identify which source file each audit entry comes from

### 2. Additional Data Source Detection
- Find transactions in audit not present in source files
- Identify potential missing business account data
- Analyze source attribution in audit file

### 3. Audit Accuracy Verification
- Check for missing transactions
- Validate categorization and exclusions
- Ensure data consistency

### 4. Data Quality Assessment
- Detect missing values
- Identify duplicates
- Validate data types and formats

## Known Issues & Observations

1. **Empty Business File**: `business_paypal-6.CSV` is empty (0 bytes), which may indicate:
   - Business transactions are included in the audit but source file is missing
   - Business account data needs to be exported separately
   - This could be a source of unmatched transactions

2. **Transaction Count Discrepancy**: Audit file (9,151 rows) has significantly more entries than personal file (4,818 rows), suggesting:
   - Multiple data sources are combined in the audit
   - Transactions may be duplicated for analysis purposes
   - Business account data is included in audit

## Future Enhancements
- Automate data validation and reconciliation
- Create visualization dashboards for transaction analysis
- Implement automated alerting for data inconsistencies
- Document standard operating procedures for recurring audits
- Add support for multiple business account files
- Generate detailed mismatch reports with specific transaction details

## Results & Findings
After running the analysis, check `ANALYSIS_REPORT.txt` for:
- Total transaction counts
- Match percentage between files
- Unmatched transaction details
- Data quality metrics
- Recommendations for data reconciliation

## Questions or Issues?
If the analysis reveals unexpected discrepancies, verify:
1. All source files are exported for the same date range
2. Business PayPal account data is included
3. Transaction export settings are consistent
4. No manual modifications were made to source files