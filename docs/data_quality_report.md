# TrustLens — Data Quality Report

## 1. Dataset Validation

The Olist dataset was loaded into PostgreSQL under the `raw` schema. All nine expected tables are present.

| Table | Rows |
|---|---:|
| customers | 99,441 |
| geolocation | 1,000,163 |
| order_items | 112,650 |
| order_payments | 103,886 |
| order_reviews | 99,224 |
| orders | 99,441 |
| products | 32,951 |
| sellers | 3,095 |
| category_translation | 71 |

## 2. Checks Passed

- Order IDs are present and unique.
- Customer IDs are unique.
- Order-item combinations are unique.
- Payment record combinations are unique.
- Review ID and order ID combinations are unique.
- No negative product prices or freight values were found.
- No missing product IDs, seller IDs, prices or freight values were found in order items.
- No unmatched customer, product or seller references were found.
- No missing or negative payment values were found.
- No missing or invalid review scores were found.
- Estimated delivery dates are complete.

## 3. Data Quality Issue

Eight orders marked as delivered have missing actual delivery dates.

**Impact:** These records cannot be reliably classified as early, on-time or late using actual delivery dates.

**Action:** Investigate these records and exclude them from delivery-variance calculations where actual dates are unavailable. Document the exclusion in any resulting metrics.
### Missing Payment Record

One order marked as delivered has no matching record in `raw.order_payments`.

- Item count: 3
- Total item value: 134.97
- Total freight: 8.49
- Matching payment records: 0

**Impact:** Payment-based revenue analysis may not fully represent this order.

**Action:** Flag the order for investigation. Do not assume payment was or was not received based on the available tables alone.

## 4. Conclusion

The initial checks found no duplicate keys in the tested combinations and no issues in the tested price, freight, payment and review-score fields. The eight delivered orders with missing actual delivery dates remain an anomaly requiring investigation.

These checks cover the fields tested so far; they do not establish that every field in the dataset is error-free.