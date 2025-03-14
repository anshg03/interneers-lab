# API Documentation


## Table of Contents

1. [Products Collection](#products-collection)  
   - [Product Model](#product-model)  

2. [CRUD API's](#crud-apis)  
   - [Create a New Product (POST)](#create-a-new-product-post)  
   - [Update the Product (PUT/PATCH)](#update-the-product-putpatch)  
   - [Delete the Product (DELETE)](#delete-the-product-delete)  
   - [Get All Products (Using Pagination and Recently created) (GET)](#get-all-products-using-pagination-recently_created-get)
  
3. [Discount Logic](#discount-logic)  

4. [Controller-Service-Repository Pattern](#controller-service-repository-pattern)  
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
      "quantity": "IntField (required) The stock of the product remaining",
      "initial_quantity": "IntField (editable=False) This is quantity of product during creation is not editable",
      "created_at":"DateTimeField (required) This is assigned as time instance during object creation",
      "updated_at":"DateTimeField (required) This is assigned as time instance during object creation and get update when put/patch request is hit"
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
        "quantity": 20,
        "inital_quantity":20,
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

+ **URL:** `http://127.0.0.1:8001/product/update/{ObjectId}`

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
        "quantity": 20,
        "inital_quantity":20,
      }
    }
    ```

#### 2) PATCH Request (Partial Update)

+ **URL:** `http://127.0.0.1:8001/product/update/{ObjectId}`

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
        "quantity": 20,
        "inital_quantity":20,
      }
    }
    ```

---

### Delete the Product [DELETE]

#### Delete Request

+ **URL:** `http://127.0.0.1:8001/product/delete/{ObjectId}`

+ **Response** 

    + **Status - 200 (OK)**

    ```json
    {
      "message": "Product deleted successfully"
    }
    ```

---

### Get All Products (Using Pagination and most recently created) [GET]

It returns the products which is created recently defined by parameter in the request url `recent` whose default value is set to all the products.

#### Get Request

+ **URL:** `http://127.0.0.1:8001/product?page=1&recent=2`

+ **Default Page Size:** `3`

+ **Response**

    + **Status - 200 (OK)**
    
    ```json
    {
    "status": true,
    "total_pages": 1,
    "current_page": 1,
    "products": [
        {
            "name": "ipad",
            "description": "Good purchase in markett",
            "price": 75000,
            "category": "Electronics",
            "brand": "apple",
            "quantity": 10,
            "initial_quantity": 15
        },
        {
            "name": "Phone",
            "description": "Good purchase in markett",
            "price": 15000,
            "category": "Electronics",
            "brand": "Samsung",
            "quantity": 9,
            "initial_quantity": 10
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

---

### Discount Logic

We filter out products where the time elapsed since their creation (`created_at`) exceeds a certain threshold, and the current quantity is the same as the initial quantity. If these conditions are met, a discount specified in the request body is applied, and the product price is updated.

+ **URL:** `http://127.0.0.1:8001/product/discount/`

+ **Time Threshold:** `1 hour` (for testing purposes)

+ **Request (application/json)**

    ```json
    {
      "discount": 5
    }
    ```

+ **Response**

    + **Status - 200 (OK)**

    ```json
    {
      "message": "Discount of 5% applied successfully",
      "products": [
        {
          "name": "Badminton",
          "description": "Good purchase in market",
          "price": 4750,
          "category": "Sports",
          "brand": "Yonex",
          "quantity": 20,
          "initial_quantity": 20
        }
      ]
    }
    ```

---

### Controller-Service-Repository Pattern

1) **Controller Layer**: Manages incoming requests and sends appropriate responses.

2) **Service Layer**: Contains business logic and processing operations.

3) **Repository Layer**: Handles all database interactions, including querying, creating, and updating records.
