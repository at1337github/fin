#!/usr/bin/env python3
"""
Final Audit Creation - With P2P Transfer Detection

Creates the final audit with proper P2P transfer exclusion and enhanced categorization.
"""

import pandas as pd
import re


def is_p2p_transfer(row):
    """Detect if a transaction is a P2P transfer (not merchant spending)."""
    name = str(row['Name']).lower() if pd.notna(row['Name']) else ''

    # Specific person names (these are transfers to individuals, not businesses)
    p2p_names = [
        'aizihaer tuerxuntuoheti',  # Specific person receiving transfers
        'cash app*aizihaer',         # Cash App transfers to same person
    ]

    if any(p2p_name in name for p2p_name in p2p_names):
        return True

    # Check transaction type - P2P transfers
    trans_type = str(row['Type']).lower()
    if 'p2p' in trans_type and row['Source'] == 'Cash App':
        return True

    return False


def enhanced_categorize(row):
    """Enhanced categorization with comprehensive merchant patterns."""
    if row['Analysis_Status'] == 'Excluded':
        return 'Excluded'

    name = str(row['Name']).lower() if pd.notna(row['Name']) else ''

    # Financial Services / Banking
    financial_keywords = [
        'chime', 'cleo ai', 'paypal inc', 'one\*finance', 'reb nyc',
        'allianz insurance', 'vanguard', 'fidelity', 'bank',
        'credit card', 'loan', 'insurance', 'affirm', 'afterpay',
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

    # Tech & Subscriptions
    tech_keywords = [
        'apple', 'google', 'microsoft', 'netflix', 'spotify', 'amazon prime',
        'hulu', 'disney', 'adobe', 'dropbox', 'icloud', 'github',
        'patreon', 'twitch', 'youtube', 'soundcloud', 'audible',
        'nektony', 'spokeo', 'truthfinder', 'epoch'
    ]
    if any(keyword in name for keyword in tech_keywords):
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

    # Grocery / Supermarkets / Delis
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
        'tj maxx', 'marshall', 'ross', 'burlington'
    ]
    if any(keyword in name for keyword in retail_keywords):
        return 'Retail/Shopping'

    # ATM
    if 'atm' in name or 'pai atm' in name or 'pai iso' in name:
        return 'ATM/Cash'

    # Vending Machines
    if 'vending' in name or 'canteen' in name:
        return 'Vending/Snacks'

    # Healthcare / Pharmacy
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
    print("FINAL AUDIT CREATION")
    print("="*60)

    # Load the complete audit
    df = pd.read_csv('Complete_Audit_PayPal_CashApp.csv')

    print(f"\nInitial stats:")
    print(f"  Total transactions: {len(df)}")
    print(f"  Included: {len(df[df['Analysis_Status'] == 'Included (True Spend)'])}")
    print(f"  Excluded: {len(df[df['Analysis_Status'] == 'Excluded'])}")

    # Identify P2P transfers
    print("\nDetecting P2P transfers...")
    p2p_mask = df.apply(is_p2p_transfer, axis=1) & (df['Analysis_Status'] == 'Included (True Spend)')
    p2p_count = p2p_mask.sum()
    p2p_amount = df[p2p_mask]['Amount'].sum()

    print(f"  Found {p2p_count} P2P transfers")
    print(f"  Total P2P amount: ${p2p_amount:,.2f}")

    # Move P2P transfers to excluded
    df.loc[p2p_mask, 'Analysis_Status'] = 'Excluded'
    df.loc[p2p_mask, 'Exclusion_Reason'] = 'Transfer / Noise'
    df.loc[p2p_mask, 'Category'] = 'Excluded'

    # Apply enhanced categorization to remaining included transactions
    print("\nApplying enhanced categorization...")
    df['Category'] = df.apply(enhanced_categorize, axis=1)

    # Final statistics
    print("\n" + "="*60)
    print("FINAL AUDIT STATISTICS")
    print("="*60)

    included = df[df['Analysis_Status'] == 'Included (True Spend)']
    excluded = df[df['Analysis_Status'] == 'Excluded']

    print(f"\nTotal transactions: {len(df)}")
    print(f"Included (True Spend): {len(included)}")
    print(f"Excluded: {len(excluded)}")

    true_spend = included['Amount'].sum()
    print(f"\n💰 Total True Spend: ${true_spend:,.2f}")

    print(f"\nExclusion Breakdown:")
    print(excluded['Exclusion_Reason'].value_counts())

    print(f"\nCategory Breakdown (Included only):")
    category_counts = included['Category'].value_counts()
    print(category_counts)

    uncategorized = category_counts.get('Other/Uncategorized', 0)
    categorization_pct = ((len(included) - uncategorized) / len(included) * 100)
    print(f"\nCategorization Coverage: {categorization_pct:.1f}%")

    # Save final audit
    output_file = 'Final_Audit_PayPal_CashApp.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✓ Final audit saved to: {output_file}")

    # Generate spending summary by category
    print("\n" + "="*60)
    print("SPENDING BY CATEGORY")
    print("="*60)

    for category in sorted(category_counts.index):
        if category != 'Other/Uncategorized':
            count = category_counts[category]
            amount = included[included['Category'] == category]['Amount'].sum()
            avg = amount / count
            pct = (count / len(included) * 100)
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


if __name__ == "__main__":
    main()
