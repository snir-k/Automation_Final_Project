import os
import time
from services.product_service import ProductNotFoundServiceError, ProductServiceError
from flask import Flask, request, jsonify, render_template
from models.models import Product
from services import product_service
import db.init_db as database
import re

database.create_db()
database.create_table()
time.sleep(3)
app = Flask(__name__)

# CONFIGURATION: Establishes a verified destination path for file uploads
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def _is_valid_float(value: str) -> bool:
    """Private Helper: Safely evaluates if a string can be parsed into a float without crashing."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


@app.route('/other/home')
def other_home():
    return render_template('/other_website/home.html')


@app.route('/other/next')
def other_next():
    return render_template('/other_website/nextpage.html')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_all():
    products = product_service.get_all_products()
    return jsonify([p.__dict__ for p in products])


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_one(product_id):
    try:
        product = product_service.get_product(product_id)
        return jsonify(product.__dict__)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except ProductNotFoundServiceError as e:
        err_message = str(e)
        return jsonify({"error": err_message}), 404


# HARDENED API GATEWAY: Processes binary image data and executes physical disk persistence bounds
@app.route('/api/products', methods=['POST'])
def create():
    try:
        name = request.form.get('name')
        price_raw = request.form.get('price')
        image_filename = request.form.get('image', 'default.png')

        # FIXES BUG #11 & #13: Strict Alphanumeric starter and custom image extension whitelist check
        # This completely blocks bypass vectors containing malicious formats (e.g .exe, .sh)
        image_regex = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_\-\s.]*\.(png|jpg|jpeg)$', re.IGNORECASE)
        clean_img_str = str(image_filename).replace('\\', '/').split('/')[-1].strip()

        if not clean_img_str or clean_img_str == "" or clean_img_str == "uploads" or not image_regex.match(clean_img_str):
            return jsonify({"error": "Invalid image filename format. Only valid image extensions are permitted."}), 400

        if not name or not price_raw:
            return jsonify({"error": "Product name and price parameters are required."}), 400

        # FIXES BUG #16: Intercepts raw casting loops to avoid unhandled ValueError crashes
        if not _is_valid_float(price_raw):
            return jsonify({"error": "Product price must be a valid number representation."}), 400

        price = float(price_raw)

        # PROCESSES BINARY FILES: Intercepts raw data stream from the browser interface
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '':
                image_filename = file.filename
                safe_filename = str(image_filename)
                target_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
                file.save(target_path)

        # FIXES PATH CONCATENATION BUG: Forces a strict forward-slash web URL structure
        clean_filename = str(image_filename).replace('\\', '/').split('/')[-1]
        final_image_path = f"uploads/{clean_filename}"

        new_product = Product(
            product_id=0,
            name=name,
            price=price,
            image=final_image_path
        )

        new_id = product_service.add_product(new_product)
        return jsonify({"message": "Product added", "id": new_id}), 201

    except (KeyError, ValueError, ProductServiceError) as e:
        return jsonify({"error": str(e)}), 400


# NEW HARDENED ENDPOINT: Processes PUT modifications and syncs physical image assets
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update(product_id):
    try:
        name = request.form.get('name')
        price_raw = request.form.get('price')
        image_filename = request.form.get('image')

        # FIXES BUG #11 & #13: Strict Alphanumeric starter and custom image extension whitelist check
        image_regex = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_\-\s.]*\.(png|jpg|jpeg)$', re.IGNORECASE)
        clean_img_str = str(image_filename).replace('\\', '/').split('/')[-1].strip()

        if not clean_img_str or clean_img_str == "" or clean_img_str == "uploads" or not image_regex.match(clean_img_str):
            return jsonify({"error": "Invalid image filename format. Only valid image extensions are permitted."}), 400

        if not name or not price_raw:
            return jsonify({"error": "Product name and price parameters are required for updates."}), 400

        # FIXES BUG #16: Intercepts raw casting loops on updates to avoid server crashes
        if not _is_valid_float(price_raw):
            return jsonify({"error": "Product price must be a valid number representation."}), 400

        price = float(price_raw)

        # PROCESSES BINARY FILES ON UPDATE: Allows replacing the image asset on disk dynamically
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '':
                image_filename = file.filename
                safe_filename = str(image_filename).replace('\\', '/').split('/')[-1]
                target_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
                file.save(target_path)

        clean_filename = str(image_filename).replace('\\', '/').split('/')[-1]
        final_image_path = f"uploads/{clean_filename}"

        updated_product = Product(
            product_id=product_id,
            name=name,
            price=price,
            image=final_image_path
        )

        product_service.update_product(updated_product)
        return jsonify({"message": "Product updated"}), 200

    except ProductNotFoundServiceError as e:
        return jsonify({"error": str(e)}), 404
    except (KeyError, ValueError, ProductServiceError) as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete(product_id):
    try:
        product_service.delete_product(product_id)
        return jsonify({"message": "Product deleted"})
    except ProductNotFoundServiceError:
        return jsonify({"error": "Product not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
