from flask import Flask, render_template
from .products import products_bp
from .users import users_bp
from .database import init_db
import os


def create_app():
    # Configurar la ruta de templates
    template_dir = os.path.abspath("templates")
    app = Flask(__name__, template_folder=template_dir)

    # Cargar configuración desde variables de entorno
    app.config.from_pyfile("config.py")

    # Inicializar base de datos
    init_db(app)

    # Registrar Blueprints
    app.register_blueprint(products_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api")

    # Ruta para renderizar index.html
    @app.route("/")
    def index():
        return render_template("index.html")

    # Ruta para renderizar products.html
    @app.route("/products")
    def products():
        return render_template("products.html")

    return app
