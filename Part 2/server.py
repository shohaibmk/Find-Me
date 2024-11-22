from flask import Flask, request, jsonify
from threading import Lock
from datetime import datetime
import os
import time


app = Flask(__name__)

#in memory Database
database = dict()
product_number = 1  #product counter

# Directory to save uploaded images
upload_folder = 'uploads'
os.makedirs(upload_folder, exist_ok=True)  
app.config['upload_folder'] = upload_folder

#method to store images in a folder
def store_images(images):
    list_of_filenames = []
    for image in images:
        filetype = str(image.mimetype.split('/')[1])
        filename = "product"+str(product_number)+"_"+str(time.time())+"."+filetype
        file_path = os.path.join(app.config['upload_folder'], filename)
        image.save(file_path)
        list_of_filenames.append(filename)
    return list_of_filenames

#method to write into the in memory database
def databaseWrite(name,description,dimensions,color,price,currency,image):
    global product_number
    list_of_filenames = store_images(image)
    # print("Writing in DB")
    insert_data = {
        "name":name,
        "description": description,
        "dimensions": dimensions,
        "color": color,
        "price": price,
        "currency": currency,
        "images":list_of_filenames
    }
    
    print("Product Details:\n",insert_data)
    key = "product" + str(product_number)
    # print("after")
    database[key] = insert_data
    product_number+=1
    return key

def databaseRead(pid):
    try:
        return database[pid]
    except KeyError:
        print("Product Not Found: ",pid)
        return None

def format_record(record):
    data = {
        "name": record["name"],
        "description": record["description"],
        "dimensions": record["dimensions"],
        "color": record["color"],
        "price": record["price"],
        "currency": record["currency"],
    }
    files = record['images']
    counter = 1
    for file in files:
        
        id = "Image"+ str(counter)
        data[id] = file
        counter += 1
    
    # print("\n\n\n\nin format record: ",)
    return data

def get_and_format_product(pid):
    record =  databaseRead(pid)
    if not record:
        return None
    else:
        print("Product Found: ",pid)
        print(record)
        record = format_record(record)
        return record

#method: POST
#route: '/products'
@app.route('/products', methods=['POST'])
def add_product():  # Adding new product
    print("\nWrite initiated |",datetime.now())
    try:
        data = request.form
        list_of_files = []

        #check for complete form data
        if not data or len(data) !=6:
            return jsonify({"Error":"Incomplete request","Message":"Make sure to include name,description,dimensions,color,price,currency"}),400

        #check for complete image files
        if request.files:        
            for file in request.files:
                list_of_files.append(request.files[file])

            # print("\n\nlist of images:",list_of_files)
        elif not request.files:
            return jsonify({"Error":"Incomplete request","Message":"Missing product images"}),400
                
        try:
            pid = databaseWrite(data['Name'],data['Description'],data['Dimensions'],data['Color'],data['Price'],data['Currency'],list_of_files)
        except:
            print("Write Failed |",datetime.now())
            return jsonify({"Error":"Write Unsuccessful","Message":"Error creating new product DB"}),400
        print("Write Successful |",datetime.now())
        return jsonify({"Message":"Write Successful" ,"Data": str(data),"Images":str(list_of_files),"ProductID":pid}), 201
    except:
        print("Write Failed |",datetime.now())
        return jsonify({"Error":"Write Unsuccessful","Message":"Error creating new product"})
    
#method: POST
#route: '/products'
#query parameters: pid
@app.route('/products', methods=['GET'])
def get_product():
    pid = request.args.get('pid')
    if pid:
        pid = request.args.get('pid')
        
        product = get_and_format_product(pid)
        if not product:
            return jsonify({"status":"Product Not Found"}), 201
        
        return jsonify(product), 201
    else:    
        return jsonify({"Message":"Unknown Request"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    print("\n\n\n\n\n\n")