import os
import time
from datetime import datetime

# In-memory Database
database = {}
product_number = 1  # Product counter

# Directory to save uploaded images
upload_folder = 'uploads'
os.makedirs(upload_folder, exist_ok=True)

# Method to store images in a folder
def store_images(images):
    try:
        global product_number
        list_of_filenames = []
        for image in images:
            filetype = str(image.mimetype.split('/')[1])
            filename = f"product{product_number}_{time.time()}.{filetype}"
            file_path = os.path.join(upload_folder, filename)
            image.save(file_path)
            list_of_filenames.append(filename)
        return list_of_filenames
    except Exception as e:
        print(f"Image Storage Failed | {datetime.now()} | Error: {e}")
        raise

# Method to write into the in-memory database
def databaseWrite(name, description, dimensions, color, price, currency, images):
    global product_number
    try:
        list_of_filenames = store_images(images)
        insert_data = {
            "name": name,
            "description": description,
            "dimensions": dimensions,
            "color": color,
            "price": price,
            "currency": currency,
            "images": list_of_filenames
        }
        key = f"product{product_number}"
        database[key] = insert_data
        product_number += 1
        print(f"Database Write Successful | {datetime.now()} | Product ID: {key}")
        return key
    except Exception as e:
        print(f"Database Write Failed | {datetime.now()} | Error: {e}")
        raise

# Method to read from the in-memory database
def databaseRead(pid):
    try:
        return database[pid]
    except KeyError:
        print(f"Product Not Found | {datetime.now()} | Product ID: {pid}")
        return None

# Method to format product data
def format_record(record):
    try:
        data = {
            "name": record["name"],
            "description": record["description"],
            "dimensions": record["dimensions"],
            "color": record["color"],
            "price": record["price"],
            "currency": record["currency"],
        }
        for idx, file in enumerate(record['images'], 1):
            data[f"Image{idx}"] = file
        return data
    except Exception as e:
        print(f"Format Record Failed | {datetime.now()} | Error: {e}")
        raise

# Method to get and format product data
def get_and_format_product(pid):
    record = databaseRead(pid)
    if not record:
        return None
    try:
        formatted_record = format_record(record)
        print(f"Product Found and Formatted | {datetime.now()} | Product ID: {pid}")
        return formatted_record
    except Exception as e:
        print(f"Format Failed | {datetime.now()} | Product ID: {pid} | Error: {e}")
        return None

# Method to update product data
def updateProduct(product, data, pid):
    try:
        for key in data.keys():
            product[key] = data[key]
        database[pid] = product
        print(f"Product Updated Successfully | {datetime.now()} | Product ID: {pid}")
        return True
    except Exception as e:
        print(f"Update Failed | {datetime.now()} | Product ID: {pid} | Error: {e}")
        return False
