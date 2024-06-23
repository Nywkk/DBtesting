from flask import Blueprint, jsonify, request, current_app
from .database import get_db_connection
import mysql.connector

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def fetch_all_products():
    connection = None
    try:
        db_config = {
            'DB_HOST': current_app.config['DB_HOST'],
            'DB_USERNAME': current_app.config['DB_USERNAME'],
            'DB_PASSWORD': current_app.config['DB_PASSWORD'],
            'DB_NAME': current_app.config['DB_NAME'],
            'DB_PORT': current_app.config['DB_PORT']
        }
        connection = get_db_connection(db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        return jsonify(products)
    except mysql.connector.Error as e:
        print(f"Error fetching products: {e}")
        return jsonify({"error": "Failed to fetch products"})
    finally:
        if connection:
            cursor.close()
            connection.close()

@products_bp.route('/products', methods=['POST'])
def add_product():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    image = data.get('image')
    stock = data.get('stock')
    
    connection = None
    try:
        db_config = {
            'DB_HOST': current_app.config['DB_HOST'],
            'DB_USERNAME': current_app.config['DB_USERNAME'],
            'DB_PASSWORD': current_app.config['DB_PASSWORD'],
            'DB_NAME': current_app.config['DB_NAME'],
            'DB_PORT': current_app.config['DB_PORT']
        }
        connection = get_db_connection(db_config)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Products (name, price, description, image, stock)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, price, description, image, stock))
        connection.commit()
        return jsonify({"message": "Product added successfully"})
    except mysql.connector.Error as e:
        print(f"Error inserting product: {e}")
        return jsonify({"error": "Failed to add product"})
    finally:
        if connection:
            cursor.close()
            connection.close()

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    connection = None
    try:
        db_config = {
            'DB_HOST': current_app.config['DB_HOST'],
            'DB_USERNAME': current_app.config['DB_USERNAME'],
            'DB_PASSWORD': current_app.config['DB_PASSWORD'],
            'DB_NAME': current_app.config['DB_NAME'],
            'DB_PORT': current_app.config['DB_PORT']
        }
        connection = get_db_connection(db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if product:
            return jsonify(product)
        else:
            return jsonify({"error": f"Product with ID {product_id} not found"})
    except mysql.connector.Error as e:
        print(f"Error fetching product: {e}")
        return jsonify({"error": "Failed to fetch product"})
    finally:
        if connection:
            cursor.close()
            connection.close()

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    image = data.get('image')
    stock = data.get('stock')
    
    connection = None
    try:
        db_config = {
            'DB_HOST': current_app.config['DB_HOST'],
            'DB_USERNAME': current_app.config['DB_USERNAME'],
            'DB_PASSWORD': current_app.config['DB_PASSWORD'],
            'DB_NAME': current_app.config['DB_NAME'],
            'DB_PORT': current_app.config['DB_PORT']
        }
        connection = get_db_connection(db_config)
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Products
            SET name = %s, price = %s, description = %s, image = %s, stock = %s
            WHERE id = %s
        """, (name, price, description, image, stock, product_id))
        connection.commit()
        return jsonify({"message": f"Product with ID {product_id} updated successfully"})
    except mysql.connector.Error as e:
        print(f"Error updating product: {e}")
        return jsonify({"error": f"Failed to update product with ID {product_id}"})
    finally:
        if connection:
            cursor.close()
            connection.close()
