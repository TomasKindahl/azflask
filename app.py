from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

products = [
    {'id': 143, 'name': 'Notebook', 'price': 5.49},
    {'id': 144, 'name': 'Black Marker', 'price': 1.99}
]

API_doc = """
<!DOCTYPE html>
<html>
  <head>
    <title>API documentation</title>
  </head>
  <body>
    <h1>API documentation</h1>

    <table>
      <tr>
        <th>URL</th>
        <th>method(s)</th>
        <th>description</th>
      </tr>
      <tr>
        <td>/</td>
        <td><i>any</a></td>
        <td>view this documentation</td>
      </tr>
      <tr>
        <td><a href="/products">/products</a></td>
        <td>GET</td>
        <td>return a list of all products</td>
      </tr>
      <tr>
        <td><a href="/products/143/">/products/<i>ID</i></a></td>
        <td>GET</td>
        <td>return the product with integer ID</td>
      </tr>
    </table>
  </body>
</html>
"""

@app.route('/', strict_slashes=False) 
def write_API_doc():
    """writes the API doc"""
    return API_doc

@app.route('/products', methods=['GET'], strict_slashes=False) 
def get_products():
    """returns all products"""
    return jsonify(products)

@app.route('/products/<int:id>', methods=['GET'], strict_slashes=False)
def get_product(id):
    """returns a specific product"""
    for product in products:
        if product['id'] == id:
            return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products', methods=['POST'], strict_slashes=False)
def create_product():
    """creates a new product"""
    product = request.get_json()
    if not product:
        return jsonify({'error': 'Product not found'}), 400
    if 'name' not in product:
        return jsonify({'error': 'Missing name'}), 400
    if 'price' not in product:
        return jsonify({'error': 'Missing price'}), 400
    if 'id' not in product:
        product['id'] = len(products) + 1
    products.append(product)
    return jsonify(product), 201
    

@app.route('/products/<int:id>', methods=['PUT'], strict_slashes=False)
def update_product(id):
    id = int(id)
    updated_product = request.get_json()
    for product in products:
        if product['id'] == id:
            for key, value in updated_product.items():
                product[key] = value
            return jsonify(product), 200
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products/<int:id>', methods=['DELETE'], strict_slashes=False)
def delete_product(id):
    id = int(id)
    for product in products:
        if product['id'] == id:
            products.remove(product)
            return jsonify({'message': 'Product deleted'}), 200
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
