# PART 1: Image Processing and Machine Learning with Python

This project demonstrates how to use YOLO (You Only Look Once) for object detection using OpenCV and the Ultralytics library in Python.

## Requirements

- Python 3.8 or higher
- `opencv-python` library
- `ultralytics` library
- Required dependencies listed in `requirements.txt` 

You can install the required libraries using the following command:

```bash
pip install opencv-python ultralytics
```

## Usage

This code imports necessary libraries to perform object detection. Here's a brief overview of the two main libraries used:

- OpenCV: A computer vision library used for image processing and video analysis.
- Ultralytics YOLO: A library providing pre-trained YOLO models for object detection.


## Running the Code
To utilize this script:

- Load an image, video, or live feed using OpenCV.
- Use the finetuned model based the ultralytics library for object detection.


## Example Code
Here’s an extended example of how you can use the imported libraries for object detection:

```python
import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('./Part 1/model/finetuned_yolo11n.pt')  

# Load an image
image = cv2.imread('example.jpg')

# Perform object detection
results = model(image,conf = 0.5,save = True)

# Display results
results.show()
```

## References

- OpenCV Documentation
- Ultralytics YOLO

<br><br>

# PART 2: Backend and API Development with Python

This project is a simple Flask-based API for managing product information. It supports CRUD (Create, Read, Update, Delete) operations for products. The API allows adding products, retrieving details, updating product information, and deleting products. It also handles product images and validates form data.

## Features

- **POST /products**: Add a new product with name, description, dimensions, color, price, currency, and image files.
- **GET /products?pid={product_id}**: Retrieve the details of a product using its ID.
- **PUT /products?pid={product_id}**: Update the product details based on the product ID.
- **DELETE /products?pid={product_id}**: Delete a product based on the product ID.

## Requirements

- Python 3.6 or higher
- `Flask` library
- Required dependencies listed in `requirements.txt` 

## Installation

1. Clone this repository:

    ```bash
    git clone "https://github.com/shohaibmk/Fynd-me.git"
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure that the `database.py` file exists and contains the necessary database functions (`databaseWrite`, `get_and_format_product`, `databaseRead`, `updateProduct`, and `database`).

4. Run the Flask app:

    ```bash
    python app.py
    ```

    The server will start on `localhost:5001`.

## API Endpoints

### 1. `POST /products`

Adds a new product to the system. Requires the following form data:

- `Name`: Product name (string)
- `Description`: Product description (string)
- `Dimensions`: Product dimensions (string)
- `Color`: Product color (string)
- `Price`: Product price (string)
- `Currency`: Currency of the price (string)

Additionally, the product should include image files (e.g., `.jpg`, `.png`) which are uploaded as part of the form.

#### Example Request:

```bash
POST /products
Content-Type: multipart/form-data

{
    Name: "Product A",
    Description: "Description of Product A",
    Dimensions: "10x10x10",
    Color: "Red",
    Price: "100",
    Currency: "USD",
    Images: [image1.jpg, image2.png]
}

```

#### Example Response:

```json
{
    "Message": "Write Successful",
    "ProductID": "product2"
}
```



## 2. `GET /products?pid={product_id}`
Retrieves the details of a product based on the provided `pid`.

### Example Request:

```bash
GET /products?pid=product2
```

### Example Response:
```json
{
    "Name": "Product A",
    "Description": "Description of Product A",
    "Dimensions": "10x10x10",
    "Color": "Red",
    "Price": "100",
    "Currency": "USD",
    "Images": ["image1.jpg", "image2.png"]
}
```

## 3. `PUT /products?pid={product_id}`

Updates the details of an existing product. Requires the pid as a query parameter and the updated form data.

### Example Request:
```bash
PUT /products?pid=123
Content-Type: multipart/form-data
{
    "Name": "Updated Product A",
    "Description": "Updated description of Product A",
    "Dimensions": "20x20x20",
    "Color": "Blue",
    "Price": "150",
    "Currency": "USD"
}
```
### Example Response:
```json
{
    "Message": "Product updated successfully"
}
```
## 4. `DELETE /products?pid={product_id}`

### Deletes a product based on its pid.

Example Request:
```bash
DELETE /products?pid=product4
```
Example Response:
```json
{
    "Message": "Product deleted successfully"
}
```

## Logging

- The API logs various actions (e.g., adding, updating, deleting products) along with timestamps to track operations.
- Errors are logged with details to help in debugging.

## Troubleshooting

- Ensure that the database.py file and the required database functions are properly implemented.
- If you encounter any issues with missing images or incomplete form data, make sure the request includes all required fields.