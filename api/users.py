from flask import Blueprint, jsonify, request, current_app
from .database import get_db
import mysql.connector

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
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
    
    connection = None
    try:
        connection = get_db()
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO Users (FirstSurname, SecondSurname, Name, Address, City, Email, Password, role_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        record_to_insert = (first_surname, second_surname, name, address, city, email, password, role)
        cursor.execute(insert_query, record_to_insert)
        
        connection.commit()
        return jsonify({"message": "User added successfully"})
        
    except mysql.connector.Error as error:
        return jsonify({"error": f"Error inserting user: {error}"})
        
    finally:
        if connection:
            cursor.close()
            connection.close()

@users_bp.route('/users', methods=['GET'])
def fetch_users():
    connection = None
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, FirstSurname, SecondSurname, Name, Address, City, Email FROM Users")

        users = cursor.fetchall()
        return jsonify(users)

    except mysql.connector.Error as e:
        print(f"Error fetching users: {e}")
        return jsonify({"error": "Failed to fetch users"})
        
    finally:
        if connection:
            cursor.close()
            connection.close()

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    connection = None
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, FirstSurname, SecondSurname, Name, Address, City, Email FROM Users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            return jsonify(user)
        else:
            return jsonify({"error": f"User with ID {user_id} not found"})
    except mysql.connector.Error as e:
        print(f"Error fetching user: {e}")
        return jsonify({"error": "Failed to fetch user"})
    finally:
        if connection:
            cursor.close()
            connection.close()

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    first_surname = data.get('first_surname')
    second_surname = data.get('second_surname')
    name = data.get('name')
    address = data.get('address')
    city = data.get('city')
    email = data.get('email')
    password = data.get('password')
    
    connection = None
    try:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Users
            SET FirstSurname = %s, SecondSurname = %s, Name = %s, Address = %s, City = %s, Email = %s, Password = %s
            WHERE id = %s
        """, (first_surname, second_surname, name, address, city, email, password, user_id))
        connection.commit()
        return jsonify({"message": f"User with ID {user_id} updated successfully"})
    except mysql.connector.Error as e:
        print(f"Error updating user: {e}")
        return jsonify({"error": f"Failed to update user with ID {user_id}"})
    finally:
        if connection:
            cursor.close()
            connection.close()
