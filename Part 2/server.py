from flask import Flask, request, jsonify
from threading import Lock
import time
import logging

app = Flask(__name__)

# Configure logging
# logging.basicConfig(level=logging.DEBUG)  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# logger = logging.getLogger(__name__)


@app.route('/products', methods=['POST'])
def add_product():                                          #Adding new product
    if request.headers.get('Content-Type') == 'application/json':              #posting JSON Object
        app.logger.info('JSON incoming')
        data = request.json
    if request.headers.get('Content-Type') == 'application/text': 
        app.logger.info('Text incoming')
        data = request.get_data()
    # app.logger.info('A value for debugging'+str(data))
    # logger.info('hola',data)
    return jsonify({"hola":"world","data":str(data)}), 201

    
@app.route('/products',methods = ['GET'])
def get_product():
    return "This product",201
    
if __name__ == '__main__':
    app.run(debug=True,port = 5000)
    # print("\n\n\n\n\n\n\n\n\n")
    # app.logger.debug("\n\n\n\n\n\n\n\n\n")