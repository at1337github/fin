#!/usr/bin/env python3
"""
Enhanced Categorization Script

Re-categorizes transactions with improved merchant recognition patterns.
"""

import pandas as pd
import re


def enhanced_categorize(row):
    """Enhanced categorization with more specific merchant patterns."""
    if row['Analysis_Status'] == 'Excluded':
        return 'Excluded'

    name = str(row['Name']).lower() if pd.notna(row['Name']) else ''
    original_name = str(row['Name']) if pd.notna(row['Name']) else ''

    # Check for P2P transfers that should be excluded (person names, not merchants)
    # These are likely internal transfers or payments to people
    p2p_patterns = [
        r'^aizihaer',  # Specific person name appearing 308 times
        r'cash app\*aizihaer',  # Cash App P2P
    ]
    for pattern in p2p_patterns:
        if re.search(pattern, name):
            return 'TRANSFER_TO_REVIEW'  # Flag for manual review

    # Financial Services / Banking
    financial_keywords = [
        'chime', 'cleo ai', 'paypal inc', 'one\*finance', 'reb nyc',
        'allianz insurance', 'vanguard', 'fidelity', 'bank',
        'credit card', 'loan', 'insurance'
    ]
    if any(keyword in name for keyword in financial_keywords):
        return 'Financial Services'

    # Phone / Utilities
    phone_keywords = [
        'at&t', 'verizon', 't-mobile', 'sprint', 'us mobile', 'vesta',
        'prepaid', 'mobile', 'phone', 'internet', 'wifi', 'electric',
        'gas', 'water', 'utility'
    ]
    if any(keyword in name for keyword in phone_keywords):
        return 'Phone/Utilities'

    # Tech & Subscriptions (enhanced)
    tech_keywords = [
        'apple', 'google', 'microsoft', 'netflix', 'spotify', 'amazon prime',
        'hulu', 'disney', 'adobe', 'dropbox', 'icloud', 'github',
        'patreon', 'twitch', 'youtube', 'soundcloud', 'audible'
    ]
    if any(keyword in name for keyword in tech_keywords):
        return 'Tech & Subs'

    # Transportation (enhanced)
    transport_keywords = [
        'uber', 'lyft', 'taxi', 'mta', 'transit', 'metrocard', 'parking',
        'citibik', 'citi bike', 'bike', 'curb mobility', 'via',
        'juno', 'car rental', 'joulez', 'hertz', 'enterprise', 'avis'
    ]
    if any(keyword in name for keyword in transport_keywords):
        return 'Transportation'

    # Gas Stations
    gas_keywords = ['shell', 'exxon', 'chevron', 'bp', 'mobil', 'conoco',
                   'sunoco', 'gulf', 'arco', 'marathon', 'speedway']
    if any(keyword in name for keyword in gas_keywords):
        return 'Transportation'

    # Grocery / Supermarkets (enhanced)
    grocery_keywords = [
        'grocery', 'market', 'supermarket', 'trader joe', 'whole foods',
        'target', 'walmart', 'costco', 'cvs', 'walgreens', 'duane reade',
        'rite aid', 'food town', 'key food', 'fairway', 'shoprite',
        'stop & shop', 'kroger', 'safeway', 'albertsons'
    ]
    if any(keyword in name for keyword in grocery_keywords):
        return 'Grocery/Daily'

    # Delis / Convenience Stores
    deli_keywords = [
        'deli', 'bodega', '7-eleven', 'convenience', 'corner store',
        'smoke shop', 'smoke loft', 'dm 561', 'gourmet'
    ]
    # Also check for patterns like "XXX DELI", "DELI XXX"
    if any(keyword in name for keyword in deli_keywords) or re.search(r'deli|bodega', name):
        return 'Grocery/Daily'

    # Fast Food
    fastfood_keywords = [
        'mcdonald', 'burger king', 'wendy', 'taco bell', 'kfc',
        'subway', 'chick-fil-a', 'chick fil a', 'popeyes', 'five guys',
        'shake shack', 'chipotle', 'panda express', 'arby', 'sonic',
        'jack in the box', 'carl\'s jr', 'hardee', 'white castle'
    ]
    if any(keyword in name for keyword in fastfood_keywords):
        return 'Fast Food'

    # Restaurants / Dining (look for TST* prefix and common restaurant patterns)
    restaurant_patterns = [
        r'^tst\*',  # Toast POS system prefix
        r'^sq \*',  # Square POS prefix
        r'restaurant', r'cafe', r'pizza', r'sushi', r'grill',
        r'bistro', r'kitchen', r'eatery', r'steakhouse', r'bar & grill'
    ]
    restaurant_keywords = [
        'mama pho', 'pho', 'falafel', 'yia yias', 'wonder',
        'dining', 'cuisine', 'noodle', 'ramen', 'thai', 'chinese',
        'mexican', 'italian', 'japanese', 'korean', 'indian',
        'mediterranean', 'vietnamese', 'greek'
    ]
    if any(re.search(pattern, name) for pattern in restaurant_patterns):
        return 'Dining/Restaurants'
    if any(keyword in name for keyword in restaurant_keywords):
        return 'Dining/Restaurants'

    # Food Delivery (enhanced)
    delivery_keywords = [
        'doordash', 'ubereats', 'uber eats', 'grubhub', 'seamless',
        'postmates', 'instacart', 'delivery', 'caviar', 'gopuff'
    ]
    if any(keyword in name for keyword in delivery_keywords):
        return 'Delivery'

    # Services / Laundry
    service_keywords = [
        'laundry', 'dry clean', 'wash', 'salon', 'barber', 'gym',
        'fitness', 'spa', 'massage', 'nail', 'hair', 'cleaners',
        'fedex', 'ups', 'usps', 'post office', 'shipping'
    ]
    if any(keyword in name for keyword in service_keywords):
        return 'Services/Laundry'

    # Entertainment
    entertainment_keywords = [
        'movie', 'cinema', 'theater', 'concert', 'tickets', 'entertainment',
        'bar', 'club', 'lounge', 'amc', 'regal', 'cinemark', 'imax',
        'ticketmaster', 'stubhub', 'eventbrite', 'museum', 'zoo', 'aquarium'
    ]
    if any(keyword in name for keyword in entertainment_keywords):
        return 'Entertainment'

    # Retail / Shopping
    retail_keywords = [
        'kohl', 'macy', 'nordstrom', 'jcpenney', 'sears', 'dillard',
        'bloomingdale', 'h&m', 'zara', 'gap', 'old navy', 'forever 21',
        'tj maxx', 'marshall', 'ross', 'burlington', 'outlet',
        'clothing', 'apparel', 'fashion'
    ]
    if any(keyword in name for keyword in retail_keywords):
        return 'Retail/Shopping'

    # Buy Now Pay Later / Payment Services
    bnpl_keywords = [
        'afterpay', 'klarna', 'affirm', 'sezzle', 'quadpay', 'splitit',
        'paywithfour', 'pay later', 'zip*', 'tulu'
    ]
    if any(keyword in name for keyword in bnpl_keywords):
        return 'Financial Services'

    # ATM Withdrawals
    if 'atm' in name:
        return 'ATM/Cash'

    # Healthcare / Pharmacy
    health_keywords = [
        'pharmacy', 'drug', 'medical', 'doctor', 'dentist', 'hospital',
        'clinic', 'urgent care', 'health', 'prescription', 'rx'
    ]
    if any(keyword in name for keyword in health_keywords):
        return 'Healthcare'

    # Home / Hardware
    home_keywords = [
        'home depot', 'lowe', 'ace hardware', 'hardware', 'furniture',
        'ikea', 'bed bath', 'container store', 'home goods'
    ]
    if any(keyword in name for keyword in home_keywords):
        return 'Home/Hardware'

    return 'Other/Uncategorized'


def main():
    print("="*60)
    print("ENHANCED CATEGORIZATION")
    print("="*60)

    # Load the complete audit
    df = pd.read_csv('Complete_Audit_PayPal_CashApp.csv')

    print(f"\nOriginal Category Breakdown:")
    print(df[df['Analysis_Status'] == 'Included (True Spend)']['Category'].value_counts())

    # Apply enhanced categorization
    print("\nApplying enhanced categorization...")
    df['Category'] = df.apply(enhanced_categorize, axis=1)

    # Show new breakdown
    print(f"\nEnhanced Category Breakdown:")
    included = df[df['Analysis_Status'] == 'Included (True Spend)']
    category_counts = included['Category'].value_counts()
    print(category_counts)

    # Show percentage improvement
    uncategorized_count = category_counts.get('Other/Uncategorized', 0)
    total_included = len(included)
    categorized_pct = ((total_included - uncategorized_count) / total_included * 100)
    print(f"\nCategorization Coverage: {categorized_pct:.1f}%")
    print(f"Still Uncategorized: {uncategorized_count} ({100-categorized_pct:.1f}%)")

    # Check for transfers flagged for review
    transfers_to_review = df[df['Category'] == 'TRANSFER_TO_REVIEW']
    if len(transfers_to_review) > 0:
        print(f"\n⚠ Found {len(transfers_to_review)} potential P2P transfers flagged for review")
        print("\nTop flagged transactions:")
        print(transfers_to_review.groupby('Name').size().sort_values(ascending=False).head(10))

    # Save enhanced audit
    output_file = 'Complete_Audit_Enhanced.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✓ Enhanced audit saved to: {output_file}")

    # Generate categorization report
    print("\n" + "="*60)
    print("CATEGORY SUMMARY")
    print("="*60)

    for category in sorted(category_counts.index):
        if category != 'Other/Uncategorized':
            count = category_counts[category]
            pct = (count / total_included * 100)
            amount = included[included['Category'] == category]['Amount'].sum()
            print(f"\n{category}: {count} transactions ({pct:.1f}%)")
            print(f"  Total: ${amount:,.2f}")
            print(f"  Avg: ${amount/count:,.2f}")

    # Show top remaining uncategorized
    if uncategorized_count > 0:
        print("\n" + "="*60)
        print("TOP 20 REMAINING UNCATEGORIZED MERCHANTS")
        print("="*60)
        uncategorized_df = included[included['Category'] == 'Other/Uncategorized']
        top_uncategorized = uncategorized_df['Name'].value_counts().head(20)
        for merchant, count in top_uncategorized.items():
            print(f"{count:4d}  {merchant}")


if __name__ == "__main__":
    main()
