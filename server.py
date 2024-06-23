from flask import Flask, render_template
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['DB_USERNAME'] = os.getenv("DB_USERNAME")
app.config['DB_PASSWORD'] = os.getenv("DB_PASSWORD")
app.config['DB_HOST'] = os.getenv("DB_HOST")
app.config['DB_PORT'] = os.getenv("DB_PORT")
app.config['DB_NAME'] = os.getenv("DB_NAME")

# Create database URI
db_uri = f"mysql+pymysql://{app.config['DB_USERNAME']}:{app.config['DB_PASSWORD']}@{app.config['DB_HOST']}:{app.config['DB_PORT']}/{app.config['DB_NAME']}"

# Create a SQLAlchemy engine
engine = create_engine(db_uri)

def test_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return result.fetchone() is not None
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return False

# Check the database connection
if test_db_connection():
    print("Database connection successful")
else:
    print("Database connection failed")

# Register Blueprints
from api.products import products_bp
from api.users import users_bp

app.register_blueprint(users_bp, url_prefix='/api')  # Asegúrate de agregar el prefijo '/api'
app.register_blueprint(products_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
