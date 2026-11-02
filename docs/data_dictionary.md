# TrustLens Data Dictionary

## Overview

This document describes the nine raw tables in the TrustLens PostgreSQL database, based on the exported `information_schema.columns` result.

- **Schema:** `raw`
- **Tables:** 9
- **Columns:** 52
- **Observed raw data type:** `text` for all 52 columns

The raw tables preserve the source values as text. Convert values to appropriate types (such as timestamps, numeric amounts, and counts) in analytical queries or curated views when required. Do not assume that a raw text column is already numeric or a date.

## 1. `raw.orders`

**Purpose:** One row per order, containing customer, status, purchase, approval, and delivery timestamps.

| Column | PostgreSQL type | Description |
|---|---|---|
| `order_id` | text | Identifier of the order. |
| `customer_id` | text | Customer identifier associated with the order. |
| `order_status` | text | Current/final order status recorded in the source data. |
| `order_purchase_timestamp` | text | Timestamp when the order was placed. |
| `order_approved_at` | text | Timestamp when the order was approved. |
| `order_delivered_carrier_date` | text | Timestamp when the order was handed to the carrier. |
| `order_delivered_customer_date` | text | Timestamp when the order was delivered to the customer. |
| `order_estimated_delivery_date` | text | Estimated delivery timestamp/date. |

## 2. `raw.order_items`

**Purpose:** Order line items, including the product, seller, price, freight, and shipping deadline.

| Column | PostgreSQL type | Description |
|---|---|---|
| `order_id` | text | Order identifier; links an item to an order. |
| `order_item_id` | text | Sequential item number within an order. |
| `product_id` | text | Product identifier. |
| `seller_id` | text | Seller identifier for the item. |
| `shipping_limit_date` | text | Shipping deadline recorded for the item. |
| `price` | text | Item price as stored in the raw source. |
| `freight_value` | text | Freight charge for the item as stored in the raw source. |

## 3. `raw.order_payments`

**Purpose:** Payment records associated with orders.

| Column | PostgreSQL type | Description |
|---|---|---|
| `order_id` | text | Order identifier associated with the payment. |
| `payment_sequential` | text | Sequence number for a payment within an order. |
| `payment_type` | text | Payment method/type. |
| `payment_installments` | text | Number of payment installments. |
| `payment_value` | text | Payment amount as stored in the raw source. |

## 4. `raw.order_reviews`

**Purpose:** Customer review information associated with orders.

| Column | PostgreSQL type | Description |
|---|---|---|
| `review_id` | text | Review identifier. |
| `order_id` | text | Order identifier being reviewed. |
| `review_score` | text | Customer review score as stored in the raw source. |
| `review_comment_title` | text | Review comment title. |
| `review_comment_message` | text | Review comment text. |
| `review_creation_date` | text | Review creation timestamp/date. |
| `review_answer_timestamp` | text | Timestamp/date when the review was answered. |

## 5. `raw.customers`

**Purpose:** Customer identifiers and customer location attributes.

| Column | PostgreSQL type | Description |
|---|---|---|
| `customer_id` | text | Customer identifier used in orders. |
| `customer_unique_id` | text | Identifier representing a customer across orders. |
| `customer_zip_code_prefix` | text | Customer postal-code prefix. |
| `customer_city` | text | Customer city. |
| `customer_state` | text | Customer state abbreviation. |

## 6. `raw.geolocation`

**Purpose:** Geographic attributes associated with postal-code prefixes.

| Column | PostgreSQL type | Description |
|---|---|---|
| `geolocation_zip_code_prefix` | text | Postal-code prefix associated with the location. |
| `geolocation_lat` | text | Latitude value as stored in the raw source. |
| `geolocation_lng` | text | Longitude value as stored in the raw source. |
| `geolocation_city` | text | City associated with the postal-code prefix. |
| `geolocation_state` | text | State abbreviation associated with the location. |

## 7. `raw.products`

**Purpose:** Product attributes and physical dimensions.

| Column | PostgreSQL type | Description |
|---|---|---|
| `product_id` | text | Product identifier. |
| `product_category_name` | text | Product category in the source language. |
| `product_name_lenght` | text | Product-name character length. The source column spelling is preserved. |
| `product_description_lenght` | text | Product-description character length. The source column spelling is preserved. |
| `product_photos_qty` | text | Number of product photos. |
| `product_weight_g` | text | Product weight in grams. |
| `product_length_cm` | text | Product length in centimeters. |
| `product_height_cm` | text | Product height in centimeters. |
| `product_width_cm` | text | Product width in centimeters. |

## 8. `raw.sellers`

**Purpose:** Seller identifiers and seller location attributes.

| Column | PostgreSQL type | Description |
|---|---|---|
| `seller_id` | text | Seller identifier. |
| `seller_zip_code_prefix` | text | Seller postal-code prefix. |
| `seller_city` | text | Seller city. |
| `seller_state` | text | Seller state abbreviation. |

## 9. `raw.category_translation`

**Purpose:** Maps source product-category names to English category names.

| Column | PostgreSQL type | Description |
|---|---|---|
| `product_category_name` | text | Product category name in the source language. |
| `product_category_name_english` | text | English translation of the product category name. |

## Key relationships

The following are logical relationships indicated by matching identifier columns. Confirm uniqueness and referential integrity with data-quality checks before treating them as enforced database constraints.

| From | To | Relationship |
|---|---|---|
| `raw.orders.customer_id` | `raw.customers.customer_id` | Orders to customer details |
| `raw.order_items.order_id` | `raw.orders.order_id` | Order items to orders |
| `raw.order_payments.order_id` | `raw.orders.order_id` | Payments to orders |
| `raw.order_reviews.order_id` | `raw.orders.order_id` | Reviews to orders |
| `raw.order_items.product_id` | `raw.products.product_id` | Order items to products |
| `raw.order_items.seller_id` | `raw.sellers.seller_id` | Order items to sellers |
| `raw.products.product_category_name` | `raw.category_translation.product_category_name` | Products to category translations |

`raw.geolocation.geolocation_zip_code_prefix` can be matched to customer or seller postal-code prefixes for geographic analysis. Postal-code prefixes may not be unique in the geolocation source, so check the join cardinality before joining.

## Data-type and modeling notes

1. All 52 columns in the inspected raw schema are `text`.
2. Cast timestamps before date calculations and time-based analysis.
3. Cast `price`, `freight_value`, and `payment_value` to numeric types before arithmetic or aggregation.
4. Cast `review_score`, installment counts, item numbers, photo counts, dimensions, and weight to suitable numeric types when needed.
5. Preserve postal-code prefixes and identifiers as text to avoid losing leading zeros.
6. The raw schema is a staging layer. Apply type conversion and business rules in validated analytical queries or views rather than silently changing the documented raw types.

## Source

Prepared from the PostgreSQL `information_schema.columns` export for schema `raw` supplied during TrustLens project documentation.
