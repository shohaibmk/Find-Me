from flask import Flask, request, jsonify
from datetime import datetime
from database import databaseWrite, get_and_format_product, databaseRead, updateProduct, database

app = Flask(__name__)

#method: POST
#route: '/products'
@app.route('/products', methods=['POST'])
def add_product():
    print(f"Add Product Initiated | {datetime.now()}")
    try:
        data = request.form
        if not data or len(data) != 6:
            print(f"Incomplete Form Data | {datetime.now()}")
            return jsonify({
                "Error": "Incomplete request",
                "Message": "Include name, description, dimensions, color, price, and currency"
            }), 400

        if request.files:
            list_of_files = [request.files[file] for file in request.files]
        else:
            print(f"No Images Provided | {datetime.now()}")
            return jsonify({
                "Error": "Incomplete request",
                "Message": "Missing product images"
            }), 400

        pid = databaseWrite(
            data['Name'], data['Description'], data['Dimensions'], 
            data['Color'], data['Price'], data['Currency'], list_of_files
        )
        return jsonify({
            "Message": "Write Successful",
            "ProductID": pid
        }), 201
    except Exception as e:
        print(f"Add Product Failed | {datetime.now()} | Error: {e}")
        return jsonify({"Error": "Write Unsuccessful"}), 400


#method: GET
#route: '/products'
#query parameters: pid
@app.route('/products', methods=['GET'])
def get_product():
    pid = request.args.get('pid')
    if pid:
        product = get_and_format_product(pid)
        if not product:
            print(f"Get Product Failed | {datetime.now()} | Product ID: {pid}")
            return jsonify({"Error": "Product Not Found"}), 404
        return jsonify(product), 200
    else:
        print(f"Bad Request | {datetime.now()}")
        return jsonify({"Error": "Unknown Request"}), 400


#method: PUT
#route: '/products'
#query parameters: pid
@app.route('/products', methods=['PUT'])
def put_product():
    pid = request.args.get('pid')
    if pid:
        data = request.form
        product = databaseRead(pid)
        if not product:
            print(f"Product Not Found for Update | {datetime.now()} | Product ID: {pid}")
            return jsonify({"Error": "Product Not Found"}), 404
        if updateProduct(product, data, pid):
            return jsonify({"Message": "Product updated successfully"}), 200
        else:
            return jsonify({"Error": "Update Failed"}), 400
    else:
        print(f"Bad Request | {datetime.now()}")
        return jsonify({"Error": "Unknown Request"}), 400


#method: DELETE
#route: '/products'
#query parameters: pid
@app.route('/products', methods=['DELETE'])
def delete_product():
    pid = request.args.get('pid')
    if pid:
        if pid in database:
            del database[pid]
            print(f"Product Deleted | {datetime.now()} | Product ID: {pid}")
            return jsonify({"Message": "Product deleted successfully"}), 200
        else:
            print(f"Delete Failed | Product Not Found | {datetime.now()} | Product ID: {pid}")
            return jsonify({"Error": "Product Not Found"}), 404
    else:
        print(f"Bad Request | {datetime.now()}")
        return jsonify({"Error": "Unknown Request"}), 400

if __name__ == '__main__':
    print(f"Starting Server | {datetime.now()} | Port: 5001")
    app.run(debug=True, port=5001)
