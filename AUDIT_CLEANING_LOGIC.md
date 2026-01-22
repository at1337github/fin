# Audit Cleaning Logic Documentation

## Overview
This document explains the cleaning and deduplication logic applied to PayPal and Cash App transaction data to create the "True Spend" audit file.

---

## PayPal Cleaning Logic

### Exclusion Categories

#### 1. **Non-Finalized Transactions**
Transactions that are not completed should be excluded:
- **Status: Denied** - Transaction was denied/declined
- **Status: Pending** - Transaction still pending (not finalized)
- **Status: Reversed** - Transaction was reversed/refunded
- **Status: Canceled** - Transaction was canceled
- **Status: Removed** - Transaction was removed from system

**Exclusion Reason:** `Non-Finalized (Status: [STATUS])`

#### 2. **Money In / Refunds**
Transactions where money is received (not spending):
- Deposits
- Refunds
- Money received from others
- Card deposits (positive amounts)
- Any transaction with positive amount

**Exclusion Reason:** `Money In / Refund`

#### 3. **Transfers / Noise**
Internal transfers that don't represent actual spending:
- Transfers between accounts
- Balance movements
- Internal account operations
- Mobile payments between own accounts

**Exclusion Reason:** `Transfer / Noise`

### Deduplication Logic

PayPal transactions often appear multiple times due to authorization and settlement:

**Common Duplicate Patterns:**
1. **Authorization + Settlement Pairs**
   - PreApproved Payment Bill User Payment (settlement)
   - General Authorization (hold)
   - **Keep:** Settlement transaction
   - **Remove:** Authorization hold

2. **Card Withdrawal + Payment Pairs**
   - General Card Withdrawal
   - Actual payment transaction
   - **Keep:** One instance (usually the payment)
   - **Remove:** Duplicate

3. **Truly Identical Transactions**
   - Same date, amount, merchant, and type
   - **Keep:** One instance
   - **Remove:** Duplicates

---

## Cash App Cleaning Logic

### Exclusion Categories

#### 1. **Non-Finalized Transactions**
**Exclude Status:**
- `FAILED` - Transaction failed
- `WAITING_ON_RECIPIENT` - Transaction pending
- `REFUNDED` - Transaction refunded
- `CANCELED` - Transaction canceled

**Keep Status:**
- `COMPLETE` - Only completed transactions

#### 2. **Money In / Refunds**
**Exclude Transaction Types:**
- `Deposits` - Money deposited (positive amounts)
- Positive P2P transfers (money received)
- Positive amounts in any transaction type

**Logic:** If `Amount` or `Net Amount` > 0, exclude (it's money in)

#### 3. **Transfers / Noise**
**Exclude Transaction Types:**
- `Account Notifications` - System notifications
- `Withdrawal` - Withdrawals to bank (not spending)
- P2P transfers (peer-to-peer, not merchant spending)

#### 4. **True Spending**
**Include Transaction Types:**
- `Cash Card` - Spending with Cash App card (if COMPLETE and negative)
- `Cash App Pay Payment` - Payments via Cash App (if COMPLETE and negative)
- Other transaction types with negative amounts and COMPLETE status

### Deduplication Logic

Cash App transactions are generally unique, but check for:
1. **Identical Transactions**
   - Same date, amount, merchant
   - Keep one instance only

2. **Pending + Complete Pairs**
   - Same transaction may appear as WAITING_ON_RECIPIENT then COMPLETE
   - **Keep:** COMPLETE version only
   - **Remove:** WAITING_ON_RECIPIENT version if later completed

---

## Combined Audit Logic

### Step 1: Load and Clean Each Source
1. Load PayPal Personal transactions
2. Load PayPal Business transactions
3. Load Cash App file 1
4. Load Cash App file 2

### Step 2: Apply Exclusions
For each source, exclude:
- Non-finalized (failed, denied, pending, canceled, reversed)
- Money in / refunds (positive amounts)
- Transfers / noise (internal movements)
- System notifications

### Step 3: Deduplicate Within Each Source
- Remove authorization holds that have corresponding settlements
- Remove duplicate transactions (same date, amount, merchant)
- Keep only one instance of truly identical transactions

### Step 4: Deduplicate Across Sources
- Check for transactions that appear in multiple sources
- Keep one instance per unique transaction

### Step 5: Categorize
Assign spending categories:
- Tech & Subs
- Grocery/Daily
- Transportation
- Delivery
- Services/Laundry
- Entertainment
- Other/Uncategorized

### Step 6: Add Metadata
- Analysis_Status: "Included (True Spend)" or "Excluded"
- Exclusion_Reason: Why excluded (if applicable)
- Category: Spending category
- Source: Which account/source
- Type: Original transaction type
- Status: Original status

---

## Implementation Notes

### Column Mapping

**PayPal Personal:**
- Date: `Date`
- Amount: `Total` (net amount)
- Merchant: `Name`
- Type: `Type`
- Status: `Status`

**PayPal Business:**
- Date: `Date`
- Amount: `Net` (net amount after fees)
- Merchant: `Name`
- Type: `Type`
- Status: `Status`

**Cash App:**
- Date: `Date` (convert from datetime to date)
- Amount: `Net Amount` (includes fees)
- Merchant: `Notes` (merchant name)
- Type: `Transaction Type`
- Status: `Status`

### Date Normalization
- PayPal: MM/DD/YYYY format
- Cash App: YYYY-MM-DD HH:MM:SS TZ format → convert to MM/DD/YYYY

### Amount Normalization
- PayPal: Already numeric
- Cash App: Remove "$" and "," characters, convert to float
- Keep negative values (spending) as negative

---

## Expected Results

**Before Cleaning:**
- PayPal Personal: ~4,817 transactions
- PayPal Business: ~4,333 transactions
- Cash App 1: ~1,218 transactions
- Cash App 2: ~1,376 transactions
- **Total:** ~11,744 transactions

**After Cleaning:**
- Remove ~848 failed Cash App transactions (33% of Cash App)
- Remove ~18 pending Cash App transactions
- Remove ~395 Cash App deposits (money in)
- Remove PayPal denied/pending/reversed transactions
- Remove PayPal refunds and money in
- Remove duplicates
- **Estimated True Spend:** ~2,500-3,500 transactions

---

## Validation Checks

After cleaning, verify:
1. ✓ All included transactions have negative amounts (spending)
2. ✓ All included transactions have COMPLETE/Completed status
3. ✓ No duplicate transactions (same date + amount + merchant)
4. ✓ No authorization holds without settlement
5. ✓ Categories assigned to all included transactions
6. ✓ Source attribution correct for each transaction
7. ✓ Date range coverage matches source files

---

## Future Enhancements

1. **Machine Learning Categorization**
   - Auto-categorize based on merchant name patterns
   - Learn from manual categorizations

2. **Recurring Transaction Detection**
   - Identify subscriptions
   - Flag unusual spending patterns

3. **Budget Tracking**
   - Compare against budget limits
   - Alert on overspending by category

4. **Multi-Currency Support**
   - Handle foreign currency transactions
   - Apply exchange rates for unified reporting
