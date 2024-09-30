from flask import Flask, request, jsonify
import requests

 # create the Flask app instance
app = Flask(__name__) 

carts = {}

# retrieve the current cart of a user
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, [])
    return jsonify(cart)

# add a product to a user's cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    product_service_url = f"http://127.0.0.1:5000/products/{product_id}"
    product_response = requests.get(product_service_url)

    if product_response.status_code == 200:
        product = product_response.json()
        cart = carts.get(user_id, [])
        cart.append({
            'id': product['id'],
            'name': product['name'],
            'quantity': 1,
            'price': product['price']
        })
        carts[user_id] = cart
        return jsonify(cart), 201
    else:
        return jsonify({'message': 'Product not found'}), 404

# remove a product from a user's cart
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    cart = carts.get(user_id, [])
    carts[user_id] = [item for item in cart if item['id'] != product_id]
    return jsonify(carts[user_id])

# start the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
