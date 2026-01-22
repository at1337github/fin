#!/usr/bin/env python3
"""
Complete Audit Creation Script

This script combines PayPal and Cash App transaction data into a single
deduplicated, cleaned audit file following the documented cleaning logic.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import re


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
        print(f"Warning: Could not load {filepath}: {e}")
        return None


def normalize_paypal_data(df, source_name):
    """Normalize PayPal data to common format."""
    print(f"\nProcessing {source_name}...")
    print(f"  Initial transactions: {len(df)}")

    # Determine amount column (Personal uses 'Total', Business uses 'Net')
    amount_col = 'Net' if 'Net' in df.columns else 'Total'

    # Create normalized dataframe
    normalized = pd.DataFrame()
    normalized['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    normalized['Name'] = df['Name']
    normalized['Amount'] = pd.to_numeric(df[amount_col], errors='coerce')
    normalized['Type'] = df['Type']
    normalized['Status'] = df['Status']
    normalized['Source'] = source_name
    normalized['Transaction_ID'] = df.get('Transaction ID', '')

    # Apply exclusion logic
    normalized['Analysis_Status'] = 'Included (True Spend)'
    normalized['Exclusion_Reason'] = ''
    normalized['Category'] = 'Other/Uncategorized'

    # Exclude non-finalized transactions
    failed_statuses = ['Denied', 'Pending', 'Reversed', 'Canceled', 'Removed', 'Refunded']
    for status in failed_statuses:
        mask = normalized['Status'] == status
        normalized.loc[mask, 'Analysis_Status'] = 'Excluded'
        normalized.loc[mask, 'Exclusion_Reason'] = f'Non-Finalized (Status: {status})'
        normalized.loc[mask, 'Category'] = 'Excluded'

    # Exclude money in / refunds (positive amounts)
    money_in_mask = (normalized['Amount'] > 0) & (normalized['Analysis_Status'] == 'Included (True Spend)')
    normalized.loc[money_in_mask, 'Analysis_Status'] = 'Excluded'
    normalized.loc[money_in_mask, 'Exclusion_Reason'] = 'Money In / Refund'
    normalized.loc[money_in_mask, 'Category'] = 'Excluded'

    # Exclude transfers/noise (specific types)
    transfer_types = ['General Payment', 'Mobile Payment']  # When both positive and negative amounts for same person
    # More sophisticated logic: transfers between same parties on same day

    print(f"  After exclusions: {len(normalized[normalized['Analysis_Status'] == 'Included (True Spend)'])} included")

    return normalized


def normalize_cashapp_data(df, source_name):
    """Normalize Cash App data to common format."""
    print(f"\nProcessing {source_name}...")
    print(f"  Initial transactions: {len(df)}")

    # Create normalized dataframe
    normalized = pd.DataFrame()

    # Parse date (Cash App format: "YYYY-MM-DD HH:MM:SS TZ")
    normalized['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Clean amount fields (remove $ and convert to float)
    def clean_amount(val):
        if pd.isna(val) or val == '':
            return 0.0
        return float(str(val).replace('$', '').replace(',', ''))

    normalized['Amount'] = df['Net Amount'].apply(clean_amount)
    normalized['Name'] = df['Notes']  # Merchant/recipient is in Notes
    normalized['Type'] = df['Transaction Type']
    normalized['Status'] = df['Status']
    normalized['Source'] = source_name
    normalized['Transaction_ID'] = df.get('Transaction ID', '')

    # Apply exclusion logic
    normalized['Analysis_Status'] = 'Included (True Spend)'
    normalized['Exclusion_Reason'] = ''
    normalized['Category'] = 'Other/Uncategorized'

    # Exclude non-finalized transactions
    failed_statuses = ['FAILED', 'WAITING_ON_RECIPIENT', 'REFUNDED', 'CANCELED']
    for status in failed_statuses:
        mask = normalized['Status'] == status
        normalized.loc[mask, 'Analysis_Status'] = 'Excluded'
        normalized.loc[mask, 'Exclusion_Reason'] = f'Non-Finalized (Status: {status})'
        normalized.loc[mask, 'Category'] = 'Excluded'

    # Exclude money in / refunds (positive amounts)
    money_in_mask = (normalized['Amount'] > 0) & (normalized['Analysis_Status'] == 'Included (True Spend)')
    normalized.loc[money_in_mask, 'Analysis_Status'] = 'Excluded'
    normalized.loc[money_in_mask, 'Exclusion_Reason'] = 'Money In / Refund'
    normalized.loc[money_in_mask, 'Category'] = 'Excluded'

    # Exclude transfers/noise
    noise_types = ['Account Notifications', 'Deposits', 'Withdrawal']
    noise_mask = normalized['Type'].isin(noise_types) & (normalized['Analysis_Status'] == 'Included (True Spend)')
    normalized.loc[noise_mask, 'Analysis_Status'] = 'Excluded'
    normalized.loc[noise_mask, 'Exclusion_Reason'] = 'Transfer / Noise'
    normalized.loc[noise_mask, 'Category'] = 'Excluded'

    # Exclude P2P transfers (peer-to-peer, not merchant spending)
    p2p_mask = (normalized['Type'] == 'P2P') & (normalized['Analysis_Status'] == 'Included (True Spend)')
    normalized.loc[p2p_mask, 'Analysis_Status'] = 'Excluded'
    normalized.loc[p2p_mask, 'Exclusion_Reason'] = 'Transfer / Noise'
    normalized.loc[p2p_mask, 'Category'] = 'Excluded'

    print(f"  After exclusions: {len(normalized[normalized['Analysis_Status'] == 'Included (True Spend)'])} included")

    return normalized


def categorize_transaction(row):
    """Categorize transaction based on merchant name and type."""
    if row['Analysis_Status'] == 'Excluded':
        return 'Excluded'

    name = str(row['Name']).lower() if pd.notna(row['Name']) else ''

    # Tech & Subscriptions
    tech_keywords = ['apple', 'google', 'microsoft', 'netflix', 'spotify', 'amazon prime',
                     'hulu', 'disney', 'adobe', 'dropbox', 'icloud', 'github']
    if any(keyword in name for keyword in tech_keywords):
        return 'Tech & Subs'

    # Grocery / Daily
    grocery_keywords = ['grocery', 'market', 'food', 'supermarket', 'trader joe', 'whole foods',
                       'target', 'walmart', 'costco', 'cvs', 'walgreens', 'duane reade']
    if any(keyword in name for keyword in grocery_keywords):
        return 'Grocery/Daily'

    # Transportation
    transport_keywords = ['uber', 'lyft', 'taxi', 'mta', 'transit', 'metrocard', 'parking',
                         'gas', 'shell', 'exxon', 'chevron', 'bp']
    if any(keyword in name for keyword in transport_keywords):
        return 'Transportation'

    # Delivery
    delivery_keywords = ['doordash', 'ubereats', 'grubhub', 'seamless', 'postmates', 'instacart']
    if any(keyword in name for keyword in delivery_keywords):
        return 'Delivery'

    # Services / Laundry
    service_keywords = ['laundry', 'dry clean', 'wash', 'salon', 'barber', 'gym', 'fitness']
    if any(keyword in name for keyword in service_keywords):
        return 'Services/Laundry'

    # Entertainment
    entertainment_keywords = ['movie', 'cinema', 'theater', 'concert', 'tickets', 'entertainment',
                             'bar', 'club', 'lounge']
    if any(keyword in name for keyword in entertainment_keywords):
        return 'Entertainment'

    return 'Other/Uncategorized'


def deduplicate_transactions(df):
    """Remove duplicate transactions."""
    print("\nDeduplicating transactions...")
    initial_count = len(df)

    # Sort by date and amount for better duplicate detection
    df = df.sort_values(['Date', 'Amount', 'Name'])

    # Remove exact duplicates (same date, amount, name, type)
    df = df.drop_duplicates(subset=['Date', 'Amount', 'Name', 'Type'], keep='first')

    # Identify authorization + settlement pairs
    # Keep settlement (PreApproved Payment), remove authorization (General Authorization)
    df['is_authorization'] = df['Type'].str.contains('Authorization', case=False, na=False)
    df['is_settlement'] = df['Type'].str.contains('PreApproved|Bill', case=False, na=False)

    # For each date+amount+name combination, if both auth and settlement exist, remove auth
    duplicates_to_remove = []
    for (date, amount, name), group in df.groupby(['Date', 'Amount', 'Name']):
        if len(group) > 1:
            has_auth = group['is_authorization'].any()
            has_settlement = group['is_settlement'].any()
            if has_auth and has_settlement:
                # Remove authorization, keep settlement
                auth_indices = group[group['is_authorization']].index
                duplicates_to_remove.extend(auth_indices)

    if duplicates_to_remove:
        df = df.drop(duplicates_to_remove)

    df = df.drop(['is_authorization', 'is_settlement'], axis=1)

    removed_count = initial_count - len(df)
    print(f"  Removed {removed_count} duplicates")
    print(f"  Remaining transactions: {len(df)}")

    return df


def main():
    """Main audit creation function."""
    print("="*60)
    print("COMPLETE AUDIT CREATION")
    print("="*60)
    print(f"Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Load all source files
    print("\n" + "="*60)
    print("LOADING SOURCE FILES")
    print("="*60)

    personal_df = load_csv_safely('personal-6.CSV')
    business_df = load_csv_safely('business_paypal-6.CSV')
    cashapp1_df = load_csv_safely('cash_app_report_1741759362166.csv')
    cashapp2_df = load_csv_safely('cash_app_report_1746328330627.csv')

    if personal_df is None or business_df is None:
        print("Error: Could not load required PayPal files")
        sys.exit(1)

    # Normalize all sources
    print("\n" + "="*60)
    print("NORMALIZING AND CLEANING DATA")
    print("="*60)

    all_transactions = []

    # Process PayPal Personal
    if personal_df is not None:
        personal_normalized = normalize_paypal_data(personal_df, 'Personal')
        all_transactions.append(personal_normalized)

    # Process PayPal Business
    if business_df is not None:
        business_normalized = normalize_paypal_data(business_df, 'Business/Main')
        all_transactions.append(business_normalized)

    # Process Cash App files
    if cashapp1_df is not None:
        cashapp1_normalized = normalize_cashapp_data(cashapp1_df, 'Cash App')
        all_transactions.append(cashapp1_normalized)

    if cashapp2_df is not None:
        cashapp2_normalized = normalize_cashapp_data(cashapp2_df, 'Cash App')
        all_transactions.append(cashapp2_normalized)

    # Combine all transactions
    print("\n" + "="*60)
    print("COMBINING ALL SOURCES")
    print("="*60)

    combined_df = pd.concat(all_transactions, ignore_index=True)
    print(f"Total combined transactions: {len(combined_df)}")
    print(f"  Included: {len(combined_df[combined_df['Analysis_Status'] == 'Included (True Spend)'])}")
    print(f"  Excluded: {len(combined_df[combined_df['Analysis_Status'] == 'Excluded'])}")

    # Deduplicate
    combined_df = deduplicate_transactions(combined_df)

    # Apply categorization to included transactions
    print("\n" + "="*60)
    print("CATEGORIZING TRANSACTIONS")
    print("="*60)

    combined_df['Category'] = combined_df.apply(categorize_transaction, axis=1)

    # Show category breakdown
    print("\nCategory Breakdown (Included only):")
    included_df = combined_df[combined_df['Analysis_Status'] == 'Included (True Spend)']
    print(included_df['Category'].value_counts())

    # Format date for output (MM/DD/YYYY)
    combined_df['Date'] = combined_df['Date'].dt.strftime('%m/%d/%Y')

    # Prepare final output columns
    output_df = combined_df[['Date', 'Name', 'Amount', 'Analysis_Status', 'Exclusion_Reason',
                             'Category', 'Source', 'Type', 'Status']]

    # Sort by date (most recent first)
    output_df = output_df.sort_values('Date', ascending=False)

    # Save complete audit
    output_file = 'Complete_Audit_PayPal_CashApp.csv'
    output_df.to_csv(output_file, index=False)

    # Summary statistics
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)

    print(f"\n✓ Total transactions processed: {len(output_df)}")
    print(f"✓ Included (True Spend): {len(output_df[output_df['Analysis_Status'] == 'Included (True Spend)'])}")
    print(f"✓ Excluded: {len(output_df[output_df['Analysis_Status'] == 'Excluded'])}")

    print(f"\nSource Breakdown:")
    print(output_df['Source'].value_counts())

    print(f"\nExclusion Reasons:")
    excluded_df = output_df[output_df['Analysis_Status'] == 'Excluded']
    print(excluded_df['Exclusion_Reason'].value_counts())

    # Calculate total spending
    true_spend = output_df[output_df['Analysis_Status'] == 'Included (True Spend)']['Amount'].sum()
    print(f"\n💰 Total True Spend: ${true_spend:,.2f}")

    print(f"\n✓ Complete audit saved to: {output_file}")
    print("✓ Analysis complete!")


if __name__ == "__main__":
    main()
