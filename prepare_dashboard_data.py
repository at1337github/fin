#!/usr/bin/env python3
"""
Prepare data for unified-dashboard-ultimate.html
Proper categorization and format matching
"""

import pandas as pd
import re


def comprehensive_categorize(row):
    """Comprehensive categorization matching dashboard expectations."""
    name = str(row['Name']).lower() if pd.notna(row['Name']) else ''

    # GROCERIES
    grocery_keywords = [
        'market', 'grocery', 'supermarket', 'trader joe', 'whole foods',
        'target', 'walmart', 'costco', 'key food', 'fairway', 'shoprite',
        'stop & shop', 'food town'
    ]
    deli_keywords = ['deli', 'bodega', 'convenience', 'dm 561', 'nostrand', 'bound brook']

    for kw in grocery_keywords:
        if kw in name:
            return 'Groceries', 'Supermarket'

    for kw in deli_keywords:
        if kw in name:
            return 'Groceries', 'Deli/Market'

    # DINING & CAFES
    fastfood_keywords = [
        'mcdonald', 'burger king', 'wendy', 'taco bell', 'kfc',
        'subway', 'chick-fil-a', 'popeyes', 'five guys', 'shake shack',
        'chipotle', 'panda express', 'panera'
    ]
    restaurant_keywords = [
        'tst*', 'sq *', 'restaurant', 'cafe', 'pizza', 'sushi', 'grill',
        'bistro', 'kitchen', 'pho', 'falafel', 'yia yias', 'wonder',
        'marble', 'draper'
    ]
    delivery_keywords = ['doordash', 'ubereats', 'uber eats', 'grubhub', 'seamless', 'postmates']

    for kw in fastfood_keywords:
        if kw in name:
            return 'Dining Out', 'Fast Food'

    for kw in restaurant_keywords:
        if kw in name or re.search(kw.replace('*', '.*'), name):
            return 'Dining Out', 'Restaurant'

    for kw in delivery_keywords:
        if kw in name:
            return 'Food Delivery', 'Delivery'

    # TRANSPORTATION
    rideshare_keywords = ['uber', 'lyft', 'taxi', 'curb mobility', 'via']
    transit_keywords = ['mta', 'omny', 'transit', 'metrocard', 'citibik', 'bike']
    gas_keywords = ['shell', 'exxon', 'chevron', 'bp', 'mobil', 'conoco', 'gas', 'speedway']
    rental_keywords = ['cleo ai', 'hertz', 'enterprise', 'avis', 'joulez', 'revel', 'car rental']

    for kw in rideshare_keywords:
        if kw in name:
            return 'Rideshare - Uber', 'Rideshare - Uber'

    for kw in transit_keywords:
        if kw in name:
            return 'Transportation', 'Transit - Subway/Bus'

    for kw in gas_keywords:
        if kw in name:
            return 'Transportation', 'Gas Station'

    for kw in rental_keywords:
        if kw in name:
            return 'Car Rental', 'Car Rental'

    if 'parking' in name:
        return 'Transportation', 'Parking'

    if 'insurance' in name or 'allianz' in name:
        return 'Bills & Housing', 'Insurance'

    # RETAIL & SHOPPING
    clothing_keywords = [
        'bloomingdale', 'macy', 'nordstrom', 'zara', 'h&m', 'gap',
        'tj maxx', 'marshall', 'ross', 'burlington', 'kohls',
        'snipes', 'nike', 'ulta', 'farfetch'
    ]
    sports_keywords = ['dick', 'sporting goods', 'sports', 'athletic']

    for kw in clothing_keywords:
        if kw in name:
            return 'Shopping', 'Clothing'

    for kw in sports_keywords:
        if kw in name:
            return 'Shopping', 'Electronics'

    # TRAVEL
    hotel_keywords = ['hilton', 'marriott', 'residence inn', 'ihg', 'crowne plaza', 'hotel']
    for kw in hotel_keywords:
        if kw in name:
            return 'Travel', 'Hotels'

    # SERVICES
    if 'moving' in name or 'piece of cake' in name:
        return 'Bills & Housing', 'Moving'

    if 'laundry' in name or 'dry clean' in name or 'hercules' in name:
        return 'Bills & Housing', 'Laundry'

    if 'fedex' in name or 'ups' in name or 'usps' in name:
        return 'Shipping', 'Shipping'

    # SUBSCRIPTIONS
    tech_keywords = [
        'apple services', 'apple.com', 'apple store', 'apple com bill',
        'netflix', 'spotify', 'hulu', 'disney', 'adobe', 'dropbox',
        'patreon', 'amazon prime'
    ]
    background_check_keywords = ['spokeo', 'truthfinder', 'beenverified']

    for kw in tech_keywords:
        if kw in name:
            return 'Subscriptions', 'Apple Services'

    for kw in background_check_keywords:
        if kw in name:
            return 'Subscriptions', 'Software'

    # BILLS & UTILITIES
    phone_keywords = ['us mobile', 'vesta', 'at&t', 'verizon', 't-mobile', 'mobile', 'phone']
    for kw in phone_keywords:
        if kw in name:
            return 'Bills & Housing', 'Phone/Internet'

    if 'godaddy' in name:
        return 'Subscriptions', 'Software'

    # FINANCIAL SERVICES
    bnpl_keywords = ['affirm', 'afterpay', 'klarna', 'sezzle', 'paywithfour', 'zip*']
    for kw in bnpl_keywords:
        if kw in name:
            return 'Services', 'PayPal Fees'

    if 'chime' in name or 'paypal inc' in name:
        return 'Services', 'PayPal Fees'

    # VENDING & SNACKS
    if 'vending' in name or 'nayax' in name or 'canteen' in name:
        return 'Groceries', 'Convenience Store'

    # SMOKE SHOPS / TOBACCO
    if 'smoke' in name or 'vape' in name or 'tobacco' in name or 'cigar' in name:
        return 'Tobacco/Vape', 'Tobacco/Vape'

    # ATM / CASH
    if 'atm' in name or 'pai atm' in name:
        return 'ATM/Cash', 'ATM Withdrawal'

    # HEALTH & WELLNESS
    health_keywords = ['cvs', 'walgreens', 'duane reade', 'pharmacy', 'rite aid']
    for kw in health_keywords:
        if kw in name:
            return 'Health', 'Pharmacy'

    # HOME & HARDWARE
    if 'home depot' in name or 'lowe' in name or 'hardware' in name:
        return 'Shopping', 'Electronics'

    # TRANSFERS / P2P (should be excluded)
    transfer_keywords = ['george kimson', 'darnell williams', 'joseph roszak', 'xoom', 'onepay']
    for kw in transfer_keywords:
        if kw in name:
            return 'P2P Transfers', 'P2P Transfer'

    # WAWA (convenience store)
    if 'wawa' in name or 'quick chek' in name or 'racestar' in name:
        return 'Groceries', 'Convenience Store'

    # DEFAULT
    return 'Other', 'Unknown'


def main():
    print("="*60)
    print("PREPARING DATA FOR UNIFIED DASHBOARD")
    print("="*60)

    # Load data
    df = pd.read_csv('July_December_2025_Audit.csv')

    # Filter to included only
    df = df[df['Analysis_Status'] == 'Included (True Spend)'].copy()

    print(f"\nLoaded {len(df)} transactions")

    # Apply comprehensive categorization
    print("Applying comprehensive categorization...")
    df[['Group', 'Category']] = df.apply(lambda row: pd.Series(comprehensive_categorize(row)), axis=1)

    # Filter out P2P transfers and ATM
    before_filter = len(df)
    df = df[~df['Group'].isin(['P2P Transfers', 'ATM/Cash'])].copy()
    print(f"Filtered out {before_filter - len(df)} P2P/ATM transactions")

    # Prepare final format for dashboard
    dashboard_data = pd.DataFrame()
    dashboard_data['Date'] = df['Date']
    dashboard_data['Description'] = df['Name']
    dashboard_data['Amount'] = df['Amount']  # Already negative
    dashboard_data['Group'] = df['Group']
    dashboard_data['Category'] = df['Category']

    # Save
    output_file = 'dashboard_data.csv'
    dashboard_data.to_csv(output_file, index=False)

    print(f"\n✓ Saved to: {output_file}")

    # Statistics
    print("\n" + "="*60)
    print("CATEGORIZATION RESULTS")
    print("="*60)

    group_summary = df.groupby('Group')['Amount'].agg(['count', 'sum']).abs()
    group_summary = group_summary.sort_values('sum', ascending=False)

    print(f"\nGroup Breakdown:")
    for group, row in group_summary.iterrows():
        pct = (row['sum'] / group_summary['sum'].sum() * 100)
        print(f"  {group:30s} {int(row['count']):4d} trans  ${row['sum']:10,.2f}  ({pct:5.1f}%)")

    print(f"\n✓ Total transactions: {len(df)}")
    print(f"✓ Total amount: ${abs(df['Amount'].sum()):,.2f}")

    # Check uncategorized
    uncategorized = df[df['Group'] == 'Other']
    print(f"\n⚠ Remaining uncategorized: {len(uncategorized)} transactions (${abs(uncategorized['Amount'].sum()):,.2f})")

    if len(uncategorized) > 0:
        print("\nTop 10 uncategorized merchants:")
        top_unc = uncategorized.groupby('Name')['Amount'].sum().abs().sort_values(ascending=False).head(10)
        for name, amt in top_unc.items():
            print(f"  {name:40s} ${amt:8,.2f}")

    print("\n" + "="*60)
    print("✓ Data ready for dashboard!")
    print("="*60)
    print("\nNext steps:")
    print("1. Open: unified-dashboard-ultimate.html")
    print("2. Upload: dashboard_data.csv")
    print("3. Explore your spending!")


if __name__ == "__main__":
    main()
