#!/usr/bin/env python3
"""
Corrected Audit - After June 2025

Corrections:
1. Filter to transactions after June 2025
2. Exclude Apple Cash transfers (APPLE CASH BALANCE ADD, APPLE CASH SENT MONEY)
3. Review REB NYC as potential transfers
4. Re-categorize with corrections
"""

import pandas as pd
import re
from datetime import datetime


def is_transfer(row):
    """Detect if a transaction is actually a transfer (not spending)."""
    name = str(row['Name']).lower() if pd.notna(row['Name']) else ''

    # Apple Cash transfers (adding to balance or sending to people)
    apple_cash_transfers = [
        'apple cash balance add',
        'apple cash sent money',
        'apple cash inst xfer',  # Instant transfer
    ]

    if any(transfer in name for transfer in apple_cash_transfers):
        return True

    # REB NYC (appears to be rent or large recurring transfers)
    if 'reb nyc' in name:
        return True

    # Previously identified P2P transfers
    if 'aizihaer' in name or 'cash app*aizihaer' in name:
        return True

    return False


def enhanced_categorize(row):
    """Enhanced categorization excluding transfers."""
    if row['Analysis_Status'] == 'Excluded':
        return 'Excluded'

    name = str(row['Name']).lower() if pd.notna(row['Name']) else ''

    # Financial Services (cleaned - no REB NYC)
    financial_keywords = [
        'chime', 'cleo ai', 'paypal inc', 'one\*finance',
        'allianz insurance', 'insurance', 'affirm', 'afterpay',
        'klarna', 'sezzle', 'paywithfour', 'zip*', 'tulu'
    ]
    if any(keyword in name for keyword in financial_keywords):
        return 'Financial Services'

    # Phone / Utilities
    phone_keywords = [
        'at&t', 'verizon', 't-mobile', 'sprint', 'us mobile', 'vesta',
        'prepaid', 'mobile phone', 'internet', 'wifi', 'electric',
        'gas', 'water', 'utility', 'godaddy'
    ]
    if any(keyword in name for keyword in phone_keywords):
        return 'Phone/Utilities'

    # Tech & Subs (cleaned - no Apple Cash transfers)
    # Only include actual Apple services/products, not Apple Cash
    tech_keywords = [
        'apple services', 'apple.com/bill', 'apple store', 'apple com bill',
        'google', 'microsoft', 'netflix', 'spotify', 'amazon prime',
        'hulu', 'disney', 'adobe', 'dropbox', 'icloud', 'github',
        'patreon', 'twitch', 'youtube', 'soundcloud', 'audible',
        'nektony', 'spokeo', 'truthfinder', 'epoch'
    ]
    # Exclude Apple Cash
    if 'apple cash' not in name and any(keyword in name for keyword in tech_keywords):
        return 'Tech & Subs'

    # Transportation
    transport_keywords = [
        'uber', 'lyft', 'taxi', 'mta', 'transit', 'metrocard', 'parking',
        'citibik', 'citi bike', 'bike', 'curb mobility', 'via',
        'juno', 'car rental', 'joulez', 'hertz', 'enterprise', 'avis',
        'revel', 'shell', 'exxon', 'chevron', 'bp', 'mobil', 'conoco',
        'sunoco', 'gulf', 'arco', 'marathon', 'speedway'
    ]
    if any(keyword in name for keyword in transport_keywords):
        return 'Transportation'

    # Grocery / Delis
    grocery_keywords = [
        'grocery', 'market', 'supermarket', 'trader joe', 'whole foods',
        'target', 'walmart', 'costco', 'cvs', 'walgreens', 'duane reade',
        'rite aid', 'food town', 'key food', 'fairway', 'shoprite',
        'stop & shop', 'kroger', 'safeway', 'albertsons', 'wawa'
    ]
    deli_keywords = ['deli', 'bodega', '7-eleven', 'convenience', 'smoke shop']

    if any(keyword in name for keyword in grocery_keywords):
        return 'Grocery/Daily'
    if any(keyword in name for keyword in deli_keywords) or re.search(r'deli|bodega', name):
        return 'Grocery/Daily'

    # Fast Food
    fastfood_keywords = [
        'mcdonald', 'burger king', 'wendy', 'taco bell', 'kfc',
        'subway', 'chick-fil-a', 'chick fil a', 'popeyes', 'five guys',
        'shake shack', 'chipotle', 'panda express'
    ]
    if any(keyword in name for keyword in fastfood_keywords):
        return 'Fast Food'

    # Restaurants / Dining
    restaurant_patterns = [
        r'^tst\*',  # Toast POS
        r'^sq \*',  # Square POS
        r'restaurant', r'cafe', r'pizza', r'sushi', r'grill',
        r'bistro', r'kitchen', r'eatery'
    ]
    restaurant_keywords = [
        'mama pho', 'pho', 'falafel', 'yia yias', 'wonder',
        'dining', 'noodle', 'ramen'
    ]
    if any(re.search(pattern, name) for pattern in restaurant_patterns):
        return 'Dining/Restaurants'
    if any(keyword in name for keyword in restaurant_keywords):
        return 'Dining/Restaurants'

    # Food Delivery
    delivery_keywords = [
        'doordash', 'ubereats', 'uber eats', 'grubhub', 'seamless',
        'postmates', 'instacart', 'caviar', 'gopuff'
    ]
    if any(keyword in name for keyword in delivery_keywords):
        return 'Delivery'

    # Services
    service_keywords = [
        'laundry', 'dry clean', 'salon', 'barber', 'gym', 'fitness',
        'fedex', 'ups', 'usps', 'shipping', 'hercules corp'
    ]
    if any(keyword in name for keyword in service_keywords):
        return 'Services/Laundry'

    # Entertainment
    entertainment_keywords = [
        'movie', 'cinema', 'theater', 'concert', 'tickets',
        'amc', 'regal', 'ticketmaster'
    ]
    if any(keyword in name for keyword in entertainment_keywords):
        return 'Entertainment'

    # Retail / Shopping
    retail_keywords = [
        'kohl', 'macy', 'nordstrom', 'h&m', 'zara', 'gap',
        'tj maxx', 'marshall', 'ross', 'burlington', 'nike'
    ]
    if any(keyword in name for keyword in retail_keywords):
        return 'Retail/Shopping'

    # ATM
    if 'atm' in name or 'pai atm' in name or 'pai iso' in name:
        return 'ATM/Cash'

    # Vending Machines
    if 'vending' in name or 'canteen' in name:
        return 'Vending/Snacks'

    # Healthcare
    health_keywords = [
        'pharmacy', 'medical', 'doctor', 'dentist', 'health'
    ]
    if any(keyword in name for keyword in health_keywords):
        return 'Healthcare'

    # Home / Hardware
    home_keywords = [
        'home depot', 'lowe', 'hardware', 'ikea'
    ]
    if any(keyword in name for keyword in home_keywords):
        return 'Home/Hardware'

    return 'Other/Uncategorized'


def main():
    print("="*60)
    print("CORRECTED AUDIT - AFTER JUNE 2025")
    print("="*60)

    # Load the final audit
    df = pd.read_csv('Final_Audit_PayPal_CashApp.csv')

    # Parse dates
    df['Date_parsed'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')

    print(f"\nOriginal audit:")
    print(f"  Total transactions: {len(df)}")
    print(f"  Date range: {df['Date_parsed'].min().date()} to {df['Date_parsed'].max().date()}")

    # Filter to after June 2025
    june_2025_end = pd.Timestamp('2025-06-30')
    df_filtered = df[df['Date_parsed'] > june_2025_end].copy()

    print(f"\nAfter filtering to post-June 2025:")
    print(f"  Total transactions: {len(df_filtered)}")
    print(f"  Date range: {df_filtered['Date_parsed'].min().date()} to {df_filtered['Date_parsed'].max().date()}")

    # Identify additional transfers (Apple Cash, REB NYC)
    print("\n" + "="*60)
    print("DETECTING ADDITIONAL TRANSFERS")
    print("="*60)

    transfer_mask = df_filtered.apply(is_transfer, axis=1) & (df_filtered['Analysis_Status'] == 'Included (True Spend)')
    transfer_count = transfer_mask.sum()
    transfer_amount = df_filtered[transfer_mask]['Amount'].sum()

    print(f"\nFound {transfer_count} additional transfers:")
    if transfer_count > 0:
        transfer_breakdown = df_filtered[transfer_mask].groupby('Name')['Amount'].agg(['count', 'sum']).sort_values('sum')
        print(transfer_breakdown)
        print(f"\nTotal transfer amount: ${transfer_amount:,.2f}")

    # Move additional transfers to excluded
    df_filtered.loc[transfer_mask, 'Analysis_Status'] = 'Excluded'
    df_filtered.loc[transfer_mask, 'Exclusion_Reason'] = 'Transfer / Noise'
    df_filtered.loc[transfer_mask, 'Category'] = 'Excluded'

    # Re-categorize remaining included transactions
    print("\n" + "="*60)
    print("APPLYING CORRECTED CATEGORIZATION")
    print("="*60)

    df_filtered['Category'] = df_filtered.apply(enhanced_categorize, axis=1)

    # Final statistics
    print("\n" + "="*60)
    print("CORRECTED AUDIT STATISTICS (AFTER JUNE 2025)")
    print("="*60)

    included = df_filtered[df_filtered['Analysis_Status'] == 'Included (True Spend)']
    excluded = df_filtered[df_filtered['Analysis_Status'] == 'Excluded']

    print(f"\nTotal transactions: {len(df_filtered)}")
    print(f"Included (True Spend): {len(included)}")
    print(f"Excluded: {len(excluded)}")

    true_spend = included['Amount'].sum()
    print(f"\n💰 Total True Spend (July-Dec 2025): ${true_spend:,.2f}")

    print(f"\nExclusion Breakdown:")
    exclusion_counts = excluded['Exclusion_Reason'].value_counts()
    print(exclusion_counts)

    print(f"\nCategory Breakdown (Included only):")
    category_counts = included['Category'].value_counts()
    print(category_counts)

    uncategorized = category_counts.get('Other/Uncategorized', 0)
    categorization_pct = ((len(included) - uncategorized) / len(included) * 100) if len(included) > 0 else 0
    print(f"\nCategorization Coverage: {categorization_pct:.1f}%")

    # Save corrected audit
    output_file = 'Corrected_Audit_Post_June_2025.csv'

    # Reset index and drop helper columns
    df_output = df_filtered.drop('Date_parsed', axis=1)
    df_output.to_csv(output_file, index=False)

    print(f"\n✓ Corrected audit saved to: {output_file}")

    # Generate spending summary by category
    print("\n" + "="*60)
    print("SPENDING BY CATEGORY (JULY-DEC 2025)")
    print("="*60)

    for category in sorted(category_counts.index):
        if category != 'Other/Uncategorized':
            count = category_counts[category]
            amount = included[included['Category'] == category]['Amount'].sum()
            avg = amount / count if count > 0 else 0
            pct = (count / len(included) * 100) if len(included) > 0 else 0
            print(f"\n{category}")
            print(f"  Transactions: {count} ({pct:.1f}%)")
            print(f"  Total: ${amount:,.2f}")
            print(f"  Average: ${avg:,.2f}")

    # Remaining uncategorized
    if uncategorized > 0:
        print("\n" + "="*60)
        print(f"TOP 15 REMAINING UNCATEGORIZED ({uncategorized} total)")
        print("="*60)
        uncategorized_df = included[included['Category'] == 'Other/Uncategorized']
        top_uncategorized = uncategorized_df['Name'].value_counts().head(15)
        for merchant, count in top_uncategorized.items():
            amount = uncategorized_df[uncategorized_df['Name'] == merchant]['Amount'].sum()
            print(f"{count:4d}  ${amount:8,.2f}  {merchant}")

    # Summary comparison
    print("\n" + "="*60)
    print("COMPARISON: ORIGINAL vs CORRECTED")
    print("="*60)

    # Load original for comparison
    original = pd.read_csv('Final_Audit_PayPal_CashApp.csv')
    original['Date_parsed'] = pd.to_datetime(original['Date'], format='%m/%d/%Y', errors='coerce')
    original_filtered = original[original['Date_parsed'] > june_2025_end]
    original_included = original_filtered[original_filtered['Analysis_Status'] == 'Included (True Spend)']

    print(f"\nOriginal (post-June 2025):")
    print(f"  True Spend Transactions: {len(original_included)}")
    print(f"  True Spend Amount: ${original_included['Amount'].sum():,.2f}")

    print(f"\nCorrected (post-June 2025):")
    print(f"  True Spend Transactions: {len(included)}")
    print(f"  True Spend Amount: ${true_spend:,.2f}")

    print(f"\nDifference:")
    print(f"  Transactions: {len(included) - len(original_included)} ({(len(included) - len(original_included))/len(original_included)*100:.1f}%)")
    print(f"  Amount: ${true_spend - original_included['Amount'].sum():,.2f}")

    print(f"\n✓ Analysis complete!")


if __name__ == "__main__":
    main()
