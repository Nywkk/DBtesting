from flask import Flask, render_template, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_url_path='/static')

# Function to insert user into the database
def insert_user(first_surname, second_surname, name, address, city, email, password):
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
        INSERT INTO Users (FirstSurname, SecondSurname, Name, Address, City, Email, Password)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        record_to_insert = (first_surname, second_surname, name, address, city, email, password)
        cursor.execute(insert_query, record_to_insert)
        
        connection.commit()
        return {"message": "User added successfully"}
        
    except Exception as error:
        return {"error": f"Error inserting user: {error}"}
        
    finally:
        if connection:
            cursor.close()
            connection.close()

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle form submission
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    first_surname = data.get('first_surname')
    second_surname = data.get('second_surname', None)  # Default value if not provided
    name = data.get('name')
    address = data.get('address')
    city = data.get('city')
    email = data.get('email')
    password = data.get('password')
    
    if all([first_surname, name, address, city, email, password]):
        result = insert_user(first_surname, second_surname, name, address, city, email, password)
        return jsonify(result)
    else:
        return jsonify({"error": "Please fill out all required fields"})


if __name__ == '__main__':
    app.run(debug=True)
