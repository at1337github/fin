#!/usr/bin/env python3
"""
Final Corrected Audit - July to December 2025
With Updated Categorizations: CLEO AI (rental car) and Insurance under Transportation
"""

import pandas as pd
import re
from datetime import datetime


def is_transfer(row):
    """Detect if a transaction is actually a transfer (not spending)."""
    name = str(row['Name']).lower() if pd.notna(row['Name']) else ''

    # Apple Cash transfers
    apple_cash_transfers = [
        'apple cash balance add',
        'apple cash sent money',
        'apple cash inst xfer',
    ]
    if any(transfer in name for transfer in apple_cash_transfers):
        return True

    # REB NYC (rent/recurring transfers)
    if 'reb nyc' in name:
        return True

    # P2P transfers
    if 'aizihaer' in name or 'cash app*aizihaer' in name:
        return True

    return False


def categorize_transaction(row):
    """Categorize transactions with updated rules."""
    if row['Analysis_Status'] == 'Excluded':
        return 'Excluded'

    name = str(row['Name']).lower() if pd.notna(row['Name']) else ''

    # Transportation (UPDATED - includes CLEO AI and Insurance)
    transport_keywords = [
        'uber', 'lyft', 'taxi', 'mta', 'transit', 'metrocard', 'parking',
        'citibik', 'citi bike', 'bike', 'curb mobility', 'via',
        'juno', 'car rental', 'joulez', 'hertz', 'enterprise', 'avis',
        'revel', 'shell', 'exxon', 'chevron', 'bp', 'mobil', 'conoco',
        'sunoco', 'gulf', 'arco', 'marathon', 'speedway',
        'cleo ai',  # NEW: Rental car service
        'insurance', 'allianz'  # NEW: Transportation insurance
    ]
    if any(keyword in name for keyword in transport_keywords):
        return 'Transportation'

    # Financial Services (removed CLEO AI and Insurance)
    financial_keywords = [
        'chime', 'paypal inc', 'one\*finance',
        'affirm', 'afterpay', 'klarna', 'sezzle',
        'paywithfour', 'zip*', 'tulu'
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

    # Tech & Subs (clean - no Apple Cash)
    tech_keywords = [
        'apple services', 'apple.com/bill', 'apple store', 'apple com bill',
        'google', 'microsoft', 'netflix', 'spotify', 'amazon prime',
        'hulu', 'disney', 'adobe', 'dropbox', 'icloud', 'github',
        'patreon', 'twitch', 'youtube', 'soundcloud', 'audible',
        'nektony', 'spokeo', 'truthfinder', 'epoch'
    ]
    if 'apple cash' not in name and any(keyword in name for keyword in tech_keywords):
        return 'Tech & Subs'

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
        r'^tst\*', r'^sq \*',
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

    # Vending
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
    print("FINAL AUDIT - JULY TO DECEMBER 2025")
    print("Updated: CLEO AI → Transportation, Insurance → Transportation")
    print("="*60)

    # Load the complete audit
    df = pd.read_csv('Complete_Audit_PayPal_CashApp.csv')

    # Parse dates
    df['Date_parsed'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')

    # Filter to July-Dec 2025 FIRST for efficiency
    june_2025_end = pd.Timestamp('2025-06-30')
    df = df[df['Date_parsed'] > june_2025_end].copy()

    print(f"\nFiltered to July-Dec 2025: {len(df)} transactions")

    # Identify and exclude transfers
    transfer_mask = df.apply(is_transfer, axis=1) & (df['Analysis_Status'] == 'Included (True Spend)')
    transfer_count = transfer_mask.sum()

    if transfer_count > 0:
        print(f"Excluding {transfer_count} transfers")
        df.loc[transfer_mask, 'Analysis_Status'] = 'Excluded'
        df.loc[transfer_mask, 'Exclusion_Reason'] = 'Transfer / Noise'
        df.loc[transfer_mask, 'Category'] = 'Excluded'

    # Apply updated categorization
    print("Applying updated categorization...")
    df['Category'] = df.apply(categorize_transaction, axis=1)

    # Add month column for analysis
    df['Month'] = df['Date_parsed'].dt.to_period('M')
    df['MonthName'] = df['Date_parsed'].dt.strftime('%B')
    df['MonthNum'] = df['Date_parsed'].dt.month

    # Final statistics
    print("\n" + "="*60)
    print("FINAL AUDIT STATISTICS (JULY-DEC 2025)")
    print("="*60)

    included = df[df['Analysis_Status'] == 'Included (True Spend)']
    excluded = df[df['Analysis_Status'] == 'Excluded']

    print(f"\nTotal transactions: {len(df)}")
    print(f"Included (True Spend): {len(included)}")
    print(f"Excluded: {len(excluded)}")

    true_spend = included['Amount'].sum()
    print(f"\n💰 Total True Spend (July-Dec 2025): ${true_spend:,.2f}")
    print(f"📊 Monthly Average: ${true_spend/6:,.2f}")

    # Category breakdown
    print(f"\nCategory Breakdown:")
    category_counts = included['Category'].value_counts()
    print(category_counts)

    # Save final audit
    output_file = 'July_December_2025_Audit.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✓ Final audit saved to: {output_file}")

    # Category summary with amounts
    print("\n" + "="*60)
    print("SPENDING BY CATEGORY")
    print("="*60)

    category_summary = []
    for category in sorted(category_counts.index):
        if category != 'Other/Uncategorized':
            count = category_counts[category]
            amount = included[included['Category'] == category]['Amount'].sum()
            avg = amount / count if count > 0 else 0
            pct = (abs(amount) / abs(true_spend) * 100) if true_spend != 0 else 0

            category_summary.append({
                'Category': category,
                'Transactions': count,
                'Total': amount,
                'Average': avg,
                'Percent': pct
            })

            print(f"\n{category}")
            print(f"  Transactions: {count}")
            print(f"  Total: ${amount:,.2f}")
            print(f"  Average: ${avg:,.2f}")
            print(f"  Percent of spend: {pct:.1f}%")

    # Monthly breakdown
    print("\n" + "="*60)
    print("MONTHLY SPENDING BREAKDOWN")
    print("="*60)

    monthly = included.groupby('Month')['Amount'].sum().sort_index()
    for month, amount in monthly.items():
        print(f"{month}: ${amount:,.2f}")

    print("\n✓ Data ready for visualization!")

    return df, included


if __name__ == "__main__":
    df, included = main()
