from flask import Flask
from .products import products_bp
from .users import users_bp
from .database import init_db

def create_app():
    app = Flask(__name__)

    # Cargar configuración desde variables de entorno
    app.config.from_pyfile('config.py')

    # Inicializar base de datos
    init_db(app)

    # Registrar Blueprints
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')

    return app
