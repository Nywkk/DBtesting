import os
from flask import Blueprint, jsonify, request, current_app
from .database import get_db
import mysql.connector

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
def fetch_all_products():
    connection = None
    try:
        connection = get_db()
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


@products_bp.route("/products", methods=["POST"])
def add_product():
    # Obtener datos del formulario
    name = request.form.get("name")
    price = request.form.get("price")
    description = request.form.get("description")
    stock = request.form.get("stock")

    # Verificar si se recibió un archivo de imagen
    if "image" not in request.files:
        return jsonify({"error": "No se proporcionó una imagen"}), 400

    imagen = request.files["image"]

    # Validar que el archivo tenga un nombre
    if imagen.filename == "":
        return jsonify({"error": "Nombre de archivo de imagen vacío"}), 400

    # Guardar la imagen en el servidor
    try:
        # Define la carpeta donde se guardarán las imágenes
        upload_folder = r"static\img"
        # Si no existe la carpeta, créala
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Guarda la imagen en el servidor con un nombre único
        imagen.save(os.path.join(upload_folder, imagen.filename))
        ruta_imagen = os.path.join(upload_folder, imagen.filename)

        # Aquí deberías insertar el producto en la base de datos
        connection = (
            get_db()
        )  # Asegúrate de tener una función get_db() que devuelva una conexión a la base de datos
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO Products (name, price, description, image, stock)
            VALUES (%s, %s, %s, %s, %s)
        """,
            (name, price, description, ruta_imagen, stock),
        )
        connection.commit()

        return (
            jsonify(
                {"message": "Producto añadido exitosamente", "ruta_imagen": ruta_imagen}
            ),
            200,
        )

    except Exception as e:
        print(f"Error al guardar la imagen o insertar en la base de datos: {e}")
        return (
            jsonify(
                {"error": "Error al guardar la imagen o insertar en la base de datos"}
            ),
            500,
        )
    finally:
        if connection:
            cursor.close()
            connection.close()


@products_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    connection = None
    try:
        connection = get_db()
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


@products_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.json
    name = data.get("name")
    price = data.get("price")
    description = data.get("description")
    image = data.get("image")
    stock = data.get("stock")

    connection = None
    try:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE Products
            SET name = %s, price = %s, description = %s, image = %s, stock = %s
            WHERE id = %s
        """,
            (name, price, description, image, stock, product_id),
        )
        connection.commit()
        return jsonify(
            {"message": f"Product with ID {product_id} updated successfully"}
        )
    except mysql.connector.Error as e:
        print(f"Error updating product: {e}")
        return jsonify({"error": f"Failed to update product with ID {product_id}"})
    finally:
        if connection:
            cursor.close()
            connection.close()


@products_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    connection = None
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM Products WHERE id = %s", (product_id,))
        connection.commit()  # Realizar commit después de DELETE

        if cursor.rowcount > 0:
            return jsonify(
                {"message": f"Product with ID {product_id} deleted successfully"}
            )
        else:
            return jsonify({"error": f"Product with ID {product_id} not found"}), 404

    except mysql.connector.Error as e:
        print(f"Error deleting product: {e}")
        return jsonify({"error": "Failed to delete product"}), 500

    finally:
        if connection:
            cursor.close()
            connection.close()
