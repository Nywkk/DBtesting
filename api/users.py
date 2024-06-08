from aifc import Error
from flask import Blueprint, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

user_bp = Blueprint('user', __name__)

load_dotenv()

def insert_user(first_surname, second_surname, name, address, city, email, password, role):
    try:
        connection = mysql.connector.connect(
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO Users (FirstSurname, SecondSurname, Name, Address, City, Email, Password, role_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        record_to_insert = (first_surname, second_surname, name, address, city, email, password, role)
        cursor.execute(insert_query, record_to_insert)
        
        connection.commit()
        return {"message": "User added successfully"}
        
    except Exception as error:
        return {"error": f"Error inserting user: {error}"}
        
    finally:
        if connection:
            cursor.close()
            connection.close()


@user_bp.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    first_surname = data.get('first_surname')
    second_surname = data.get('second_surname', None)  # Default value if not provided
    name = data.get('name')
    address = data.get('address')
    city = data.get('city')
    email = data.get('email')
    password = data.get('password')
    role = 2  # Assuming role ID 2 corresponds to a specific role (e.g., "user")
    
    if all([first_surname, name, address, city, email, password]):
        result = insert_user(first_surname, second_surname, name, address, city, email, password, role)
        return jsonify(result)
    else:
        return jsonify({"error": "Please fill out all required fields"})


@user_bp.route('/api/users', methods=['GET'])
def fetch_users():
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
            cursor.execute("SELECT id, FirstSurname, SecondSurname, Name, Address, City, Email, Password FROM Users")

            users = cursor.fetchall()
            return jsonify(users)

    except Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return jsonify({"error": "Failed to fetch users"})
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
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
            cursor.execute("SELECT id, FirstSurname, SecondSurname, Name, Address, City, Email, Password FROM Users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                return jsonify(user)
            else:
                return jsonify({"error": f"User with ID {user_id} not found"})
    except Error as e:
        print(f"Error fetching user: {e}")
        return jsonify({"error": "Failed to fetch user"})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    first_surname = data.get('first_surname')
    second_surname = data.get('second_surname')
    name = data.get('name')
    address = data.get('address')
    city = data.get('city')
    email = data.get('email')
    password = data.get('password')
    
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
                UPDATE Users
                SET FirstSurname = %s, SecondSurname = %s, Name = %s, Address = %s, City = %s, Email = %s, Password = %s
                WHERE id = %s
            """, (first_surname, second_surname, name, address, city, email, password, user_id))
            connection.commit()
            return jsonify({"message": f"User with ID {user_id} updated successfully"})
    except Error as e:
        print(f"Error updating user: {e}")
        return jsonify({"error": f"Failed to update user with ID {user_id}"})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
