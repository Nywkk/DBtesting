from flask import Flask, render_template
from api.users import user_bp
from api.products import products_bp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

# Register the blueprints
app.register_blueprint(user_bp)
app.register_blueprint(products_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
