from flask import Blueprint, jsonify, request
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

products_bp = Blueprint('products', __name__)

load_dotenv()

def get_products_from_db():
    try:
        # Establish the database connection
        connection = mysql.connector.connect(
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Products")

            products = cursor.fetchall()
            return products

    except Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@products_bp.route('/api/products', methods=['GET'])
def fetch_products():
    products = get_products_from_db()
    return jsonify(products)

@products_bp.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    image = data.get('image')
    stock = data.get('stock')
    
    try:
        connection = mysql.connector.connect(
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Products (name, price, description, image, stock)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, price, description, image, stock))
            connection.commit()
            return jsonify({"message": "Product added successfully"})
    except Error as e:
        print(f"Error inserting product: {e}")
        return jsonify({"error": "Failed to add product"})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@products_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        connection = mysql.connector.connect(
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            if product:
                return jsonify(product)
            else:
                return jsonify({"error": f"Product with ID {product_id} not found"})
    except Error as e:
        print(f"Error fetching product: {e}")
        return jsonify({"error": "Failed to fetch product"})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@products_bp.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    image = data.get('image')
    stock = data.get('stock')
    
    try:
        connection = mysql.connector.connect(
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Products
                SET name = %s, price = %s, description = %s, image = %s, stock = %s
                WHERE id = %s
            """, (name, price, description, image, stock, product_id))
            connection.commit()
            return jsonify({"message": f"Product with ID {product_id} updated successfully"})
    except Error as e:
        print(f"Error updating product: {e}")
        return jsonify({"error": f"Failed to update product with ID {product_id}"})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
