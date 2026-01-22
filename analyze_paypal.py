#!/usr/bin/env python3
"""
PayPal Audit Analysis Script

This script analyzes the relationship between PayPal source files and the audit file.
It performs the following tasks:
- Loads and compares the audit file with source transaction files
- Identifies transaction matches and discrepancies
- Detects potential additional data sources
- Generates a comprehensive analysis report
"""

import pandas as pd
import sys
from datetime import datetime
from collections import defaultdict


def load_csv_safely(filepath, encoding='utf-8'):
    """Load CSV file with fallback encoding handling."""
    try:
        return pd.read_csv(filepath, encoding=encoding)
    except UnicodeDecodeError:
        try:
            return pd.read_csv(filepath, encoding='utf-8-sig')
        except:
            return pd.read_csv(filepath, encoding='latin-1')
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def analyze_data_structure(df, name):
    """Analyze and print data structure information."""
    print(f"\n{'='*60}")
    print(f"STRUCTURE: {name}")
    print(f"{'='*60}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nColumn Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")

    print(f"\nData Types:")
    print(df.dtypes)

    print(f"\nFirst 3 rows:")
    print(df.head(3).to_string())

    return df


def compare_transactions(audit_df, personal_df):
    """Compare audit file with personal transactions."""
    print(f"\n{'='*60}")
    print("TRANSACTION COMPARISON ANALYSIS")
    print(f"{'='*60}")

    # Clean and prepare data
    audit_df['Date_Clean'] = pd.to_datetime(audit_df['Date'], errors='coerce')
    personal_df['Date_Clean'] = pd.to_datetime(personal_df['Date'], errors='coerce')

    # Convert amounts to float for comparison
    audit_df['Amount_Float'] = pd.to_numeric(audit_df['Amount'], errors='coerce')
    personal_df['Total_Float'] = pd.to_numeric(personal_df['Total'], errors='coerce')

    print(f"\nAudit File Stats:")
    print(f"  Total Transactions: {len(audit_df)}")
    print(f"  Date Range: {audit_df['Date_Clean'].min()} to {audit_df['Date_Clean'].max()}")
    print(f"  Total Amount: ${audit_df['Amount_Float'].sum():,.2f}")

    print(f"\nPersonal File Stats:")
    print(f"  Total Transactions: {len(personal_df)}")
    print(f"  Date Range: {personal_df['Date_Clean'].min()} to {personal_df['Date_Clean'].max()}")
    print(f"  Total Amount: ${personal_df['Total_Float'].sum():,.2f}")

    # Analysis Status breakdown
    print(f"\n{'='*60}")
    print("AUDIT STATUS BREAKDOWN")
    print(f"{'='*60}")
    if 'Analysis_Status' in audit_df.columns:
        status_counts = audit_df['Analysis_Status'].value_counts()
        print(status_counts)

        print(f"\nExclusion Reasons:")
        if 'Exclusion_Reason' in audit_df.columns:
            exclusion_counts = audit_df['Exclusion_Reason'].value_counts()
            print(exclusion_counts)

    # Category breakdown
    if 'Category' in audit_df.columns:
        print(f"\n{'='*60}")
        print("CATEGORY BREAKDOWN")
        print(f"{'='*60}")
        category_counts = audit_df['Category'].value_counts()
        print(category_counts)

    # Source breakdown
    if 'Source' in audit_df.columns:
        print(f"\n{'='*60}")
        print("SOURCE BREAKDOWN")
        print(f"{'='*60}")
        source_counts = audit_df['Source'].value_counts()
        print(source_counts)

    # Transaction matching analysis
    print(f"\n{'='*60}")
    print("TRANSACTION MATCHING ANALYSIS")
    print(f"{'='*60}")

    # Try to match transactions by date and amount
    matched = 0
    unmatched_audit = []

    for idx, audit_row in audit_df.iterrows():
        audit_date = audit_row['Date_Clean']
        audit_amount = audit_row['Amount_Float']

        # Look for matching transaction in personal file
        matches = personal_df[
            (personal_df['Date_Clean'] == audit_date) &
            (personal_df['Total_Float'] == audit_amount)
        ]

        if len(matches) > 0:
            matched += 1
        else:
            unmatched_audit.append(audit_row)

    print(f"Matched Transactions: {matched} ({matched/len(audit_df)*100:.2f}%)")
    print(f"Unmatched in Audit: {len(unmatched_audit)} ({len(unmatched_audit)/len(audit_df)*100:.2f}%)")

    # Check for transactions in personal not in audit
    unmatched_personal = 0
    for idx, personal_row in personal_df.iterrows():
        pers_date = personal_row['Date_Clean']
        pers_amount = personal_row['Total_Float']

        matches = audit_df[
            (audit_df['Date_Clean'] == pers_date) &
            (audit_df['Amount_Float'] == pers_amount)
        ]

        if len(matches) == 0:
            unmatched_personal += 1

    print(f"Transactions in Personal not in Audit: {unmatched_personal}")

    # Additional data sources analysis
    print(f"\n{'='*60}")
    print("ADDITIONAL DATA SOURCES ANALYSIS")
    print(f"{'='*60}")

    if len(unmatched_audit) > 0:
        print(f"\nFound {len(unmatched_audit)} transactions in audit that don't match personal file.")
        print(f"This suggests there may be additional data sources.")

        # Check if these are from business source
        if 'Source' in audit_df.columns:
            unmatched_df = pd.DataFrame(unmatched_audit)
            if 'Source' in unmatched_df.columns:
                unmatched_sources = unmatched_df['Source'].value_counts()
                print(f"\nSources of unmatched transactions:")
                print(unmatched_sources)

    return matched, len(unmatched_audit), unmatched_personal


def analyze_data_consistency(audit_df):
    """Analyze data consistency and quality."""
    print(f"\n{'='*60}")
    print("DATA QUALITY ANALYSIS")
    print(f"{'='*60}")

    # Missing values
    print("\nMissing Values:")
    missing = audit_df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            print(f"  {col}: {count} ({count/len(audit_df)*100:.2f}%)")

    # Duplicate check
    duplicates = audit_df.duplicated().sum()
    print(f"\nDuplicate Rows: {duplicates}")

    # Empty names
    if 'Name' in audit_df.columns:
        empty_names = audit_df['Name'].isna().sum() + (audit_df['Name'] == '').sum()
        print(f"Transactions with empty names: {empty_names}")

    return True


def main():
    """Main analysis function."""
    print("="*60)
    print("PAYPAL AUDIT ANALYSIS")
    print("="*60)
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Load files
    print("\nLoading data files...")

    audit_df = load_csv_safely('PayPal_True_Spend_Audit.csv')
    personal_df = load_csv_safely('personal-6.CSV')

    if audit_df is None or personal_df is None:
        print("Error: Could not load required files")
        sys.exit(1)

    # Analyze structures
    audit_df = analyze_data_structure(audit_df, "PayPal True Spend Audit")
    personal_df = analyze_data_structure(personal_df, "Personal PayPal Transactions")

    # Compare transactions
    matched, unmatched_audit, unmatched_personal = compare_transactions(audit_df, personal_df)

    # Analyze data quality
    analyze_data_consistency(audit_df)

    # Final Summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"\n✓ Audit file contains {len(audit_df)} total transactions")
    print(f"✓ Personal file contains {len(personal_df)} total transactions")
    print(f"✓ {matched} transactions matched between files")
    print(f"✓ {unmatched_audit} transactions in audit not found in personal file")
    print(f"✓ {unmatched_personal} transactions in personal not found in audit file")

    print(f"\n{'='*60}")
    print("CONCLUSIONS")
    print(f"{'='*60}")

    if unmatched_audit > 0:
        print(f"\n⚠ The audit file contains transactions not present in the personal file.")
        print(f"  This indicates additional data sources are being used.")
        print(f"  Note: business_paypal-6.CSV file is empty (0 bytes)")
        print(f"  Recommendation: Verify if there's a business PayPal account file that should be included.")

    if len(audit_df) > len(personal_df):
        print(f"\n⚠ Audit file has MORE transactions than the personal file.")
        print(f"  Difference: {len(audit_df) - len(personal_df)} transactions")

    print(f"\n✓ Analysis complete!")

    # Save summary to file
    with open('ANALYSIS_REPORT.txt', 'w') as f:
        f.write("="*60 + "\n")
        f.write("PAYPAL AUDIT ANALYSIS REPORT\n")
        f.write("="*60 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Audit Transactions: {len(audit_df)}\n")
        f.write(f"Personal Transactions: {len(personal_df)}\n")
        f.write(f"Matched: {matched}\n")
        f.write(f"Unmatched in Audit: {unmatched_audit}\n")
        f.write(f"Unmatched in Personal: {unmatched_personal}\n")
        f.write("\nConclusion: See console output for detailed analysis.\n")

    print(f"\n📄 Report saved to: ANALYSIS_REPORT.txt")


if __name__ == "__main__":
    main()
