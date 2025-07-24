from flask import request, jsonify
from sqlalchemy.exc import IntegrityError # Assuming SQLAlchemy and an ORM are used

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    # 1. Basic input validation: Check for required fields
    required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # 2. Data type validation and conversion
    try:
        name = data['name']
        sku = data['sku']
        price = float(data['price']) # Ensure price is a float/decimal
        warehouse_id = int(data['warehouse_id'])
        initial_quantity = int(data['initial_quantity'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data type for one or more fields. Price should be numeric, IDs and quantity should be integers."}), 400

    # 3. Business logic validation (e.g., SKU uniqueness)
    # Assuming Product model has a query method to check for existing SKUs
    if Product.query.filter_by(sku=sku).first():
        return jsonify({"error": f"Product with SKU '{sku}' already exists."}), 409 # Conflict

    # Create new product
    try:
        product = Product(
            name=name,
            sku=sku,
            price=price,
            warehouse_id=warehouse_id # This might be problematic - see Issue 2
        )
        db.session.add(product)
        db.session.commit()

        # Update inventory count
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=warehouse_id,
            quantity=initial_quantity
        )
        db.session.add(inventory)
        db.session.commit()

        return jsonify({"message": "Product created", "product_id": product.id}), 201 # 201 Created
    except IntegrityError:
        db.session.rollback() # Rollback in case of database integrity errors (e.g., foreign key)
        return jsonify({"error": "Database integrity error. Check warehouse_id or other constraints."}), 400
    except Exception as e:
        db.session.rollback()
        # Log the error for debugging
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500