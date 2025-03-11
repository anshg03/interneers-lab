# API Documentation


## Table of Contents

1. [Products Collection](#products-collection)  
   - [Product Model](#product-model)  

2. [CRUD API's](#crud-apis)  
   - [Create a New Product (POST)](#create-a-new-product-post)  
   - [Update the Product (PUT/PATCH)](#update-the-product-putpatch)  
   - [Delete the Product (DELETE)](#delete-the-product-delete)  
   - [Get All Products (Using Pagination) (GET)](#get-all-products-using-pagination-get)  

---


## Products Collection

### Product Model

The product model describes the object in JSON format using **ModelSerializer** for validation of each field.

+ **Model (application/json)**

    ```json
    {
      "name": "CharField (required) The name of the product",
      "description": "TextField (required) The description of the product",
      "price": "IntField (required) The price of the product",
      "category": "CharField (required) The product belongs to which category",
      "brand": "CharField (required) The brand of the product",
      "quantity": "IntField (required) The stock of the product remaining"
    }
    ```

All of the above fields are required using serializers, and a custom `validate` function is made to:
- Ensure the **name** does not include special characters.
- Validate that **price** and **quantity** cannot be negative.

---

## CRUD API's

All the API endpoints are surrounded by the `@api_view` decorator to ensure correctness of the method type (POST, PUT, GET, etc.).

### Create a New Product [POST]

As soon as the product is created, we assign it an ID, which is equal to the length of the array dynamically in which it is inserted (for in-memory operations).

+ **URL:** `http://127.0.0.1:8001/product/create`

+ **Request (application/json)**

    ```json
    {
      "name": "Badminton",
      "description": "Best purchase in market",
      "category": "Sports",
      "price": 5000,
      "brand": "Konex",
      "quantity": 20
    }
    ```

+ **Response**

    + **Status - 201 (Created)**

    ```json
    {
      "message": "Product created",
      "product": {
        "name": "Badminton",
        "description": "Best purchase in market",
        "price": 5000,
        "category": "Sports",
        "brand": "Konex",
        "quantity": 20
      }
    }
    ```

<details>
<summary>Common Errors</summary>

1) **Missing Field Error by Serializer:**

    + **Request (application/json)**

        ```json
        {
          "name": "Badminton",
          "description": "Best purchase in market",
          "price": 5000,
          "brand": "Konex",
          "quantity": 20
        }
        ```

    + **Response** 

        + **Status - 400 (Bad Request)**

        ```json
        {
          "category": [
            "This field is required."
          ]
        }
        ```

2) **Invalid Quantity:**

    + **Request (application/json)**

        ```json
        {
          "name": "Badminton",
          "description": "Best purchase in market",
          "category": "Sports",
          "price": 5000,
          "brand": "Konex",
          "quantity": -1
        }
        ```

    + **Response**

        + **Status - 400 (Bad Request)**

        ```json
        {
          "quantity": [
            "Quantity should be greater than 0"
          ]
        }
        ```

3) **Name Containing Special Characters:**

    + **Request (application/json)**

        ```json
        {
          "name": "Badminton@#",
          "description": "Best purchase in market",
          "category": "Sports",
          "price": 5000,
          "brand": "Konex",
          "quantity": 20
        }
        ```

    + **Response** 

        + **Status - 400 (Bad Request)**

        ```json
        {
          "name": [
            "Name cannot contain special characters"
          ]
        }
        ```

</details>

---

### Update the Product [PUT/PATCH]

+ **PUT** - Requires all fields to be specified when updating.
+ **PATCH** - Supports partial updating of the product model.

#### 1) PUT Request (Full Update)

+ **URL:** `http://127.0.0.1:8001/product/update/1`

+ **Request (application/json)**

    ```json
    {
      "name": "Badminton",
      "description": "Best purchase in market",
      "category": "Sports",
      "price": 5000,
      "brand": "Konex",
      "quantity": 20
    }
    ```

+ **Response**

    + **Status - 200 (OK)**

    ```json
    {
      "message": "Product updated",
      "product": {
        "name": "Badminton",
        "description": "Best purchase in market",
        "price": 5000,
        "category": "Sports",
        "brand": "Yonex",
        "quantity": 20
      }
    }
    ```

#### 2) PATCH Request (Partial Update)

+ **URL:** `http://127.0.0.1:8001/product/update/1`

+ **Request (application/json)**

    ```json
    {
      "price": 10000,
      "quantity": 20
    }
    ```

+ **Response**

    + **Status - 200 (OK)**

    ```json
    {
      "message": "Product updated",
      "product": {
        "name": "Badminton",
        "description": "Best purchase in market",
        "price": 10000,
        "category": "Sports",
        "brand": "Yonex",
        "quantity": 20
      }
    }
    ```

---

### Delete the Product [DELETE]

#### Delete Request

+ **URL:** `http://127.0.0.1:8001/product/delete/1`

+ **Response** 

    + **Status - 200 (OK)**

    ```json
    {
      "message": "Product deleted successfully"
    }
    ```

---

### Get All Products (Using Pagination) [GET]

#### Get Request

+ **URL:** `http://127.0.0.1:8001/product?page=1`
+ **Default Page Size:** `3`

+ **Response**

    + **Status - 200 (OK)**

    ```json
    {
      "status": true,
      "total_pages": 2,
      "current_page": 1,
      "products": [
        {
          "name": "Pen",
          "description": "A gel pen",
          "price": 20,
          "category": "Stationery",
          "brand": "Agny",
          "quantity": 20
        },
        {
          "name": "Phone",
          "description": "Best purchase in market",
          "price": 20000,
          "category": "Electronics",
          "brand": "Samsung",
          "quantity": 20
        },
        {
          "name": "iPad",
          "description": "Best purchase in market",
          "price": 100000,
          "category": "Electronics",
          "brand": "Apple",
          "quantity": 10
        }
      ]
    }
    ```

<details>
<summary>Common Errors</summary>

1) **Page Not an Integer**

    + **URL:** `http://127.0.0.1:8001/product?page=abc`

    + **Response**

        + **Status - 400 (Bad Request)**

        ```json
        {
          "status": false,
          "message": "Invalid page number"
        }
        ```

2) **Page Number Out of Range**

    + **URL:** `http://127.0.0.1:8001/product?page=3`

    + **Response**

        + **Status - 400 (Bad Request)**

        ```json
        {
          "status": false,
          "message": "Page number out of range"
        }
        ```

</details>
