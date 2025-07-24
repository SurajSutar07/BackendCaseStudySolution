# BackendCaseStudySolution
# 📦 Backend Case Study – Part 3: API Implementation

## 🔍 Low Stock Alert API Endpoint

This Flask API returns low-stock alerts for a given company.  
It handles business rules such as recent sales activity, thresholds, and supplier data.

---

## ✅ Handled Edge Cases

| # | Edge Case | How It's Handled |
|--|-----------|------------------|
| 1 | No recent sales for a product | Filtered using `Sale.date >= X days` |
| 2 | Division by zero | `func.coalesce(..., 999)` prevents crash in `days_until_stockout` |
| 3 | Product with no supplier | Joins only with products that have a supplier |
| 4 | Products in multiple warehouses | Alerts grouped by `product_id` and `warehouse_id` |
| 5 | Invalid `company_id` | Returns empty alert list; can be customized to 404 |
| 6 | Unexpected DB errors | Wrapped in `try-except`, returns 500 |
| 7 | Missing threshold | Query checks `Inventory.quantity < Product.low_stock_threshold` |
| 8 | Large dataset | Easily extendable to pagination with `limit`, `offset` |

---

## 🧠 Explanation of Approach

```python
@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    """
    Returns low-stock alerts for products with:
    - Recent sales (last 30 days)
    - Inventory below threshold
    - Supplier data available
    """

    # Define 30-day recent sales window
    recent_sales_window = datetime.datetime.utcnow() - datetime.timedelta(days=30)

    # Query product inventory and sales
    # Calculate days until stockout using: quantity / avg daily sales
    # Group results by product and warehouse
    # Join supplier for reorder info
