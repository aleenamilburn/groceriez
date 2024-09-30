from flask import Flask, request, jsonify

app = Flask(__name__)

products = [
    {'id': 1, 'name': 'Apples', 'price': 0.50, 'quantity': 100},
    {'id': 2, 'name': 'Bread', 'price': 1.20, 'quantity': 50}
]

# retrieve all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# retrieve a product by id
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({'message': 'product not found'}), 404

# add a new product
@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    products.append(new_product)
    return jsonify(new_product), 201

# reduce the quantity of a product
@app.route('/products/<int:product_id>/reduce_quantity', methods=['POST'])
def reduce_product_quantity(product_id):
    product = next((p for p in products if p['id'] == product_id), None)

    if product and product['quantity'] > 0:
        product['quantity'] -= 1
        return jsonify({'message': 'quantity reduced', 'new_quantity': product['quantity']}), 200
    else:
        return jsonify({'message': 'product not found or out of stock'}), 404

# start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
