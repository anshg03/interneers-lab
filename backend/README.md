
# API Documentation:

## Products Collection

### Product Model:
 
The product model describes the object in JSON format using **ModelSerializer** for validation of each feild.

+ Model(application/json)

    {
      "name" : CharField (required) The name of the product
      "description: TextField (required) The description of the product
      "price": IntField (required) The price of the product
      "category": CharField (required) The product belongs to which category
      "brand": CharField (required) The brand of the poduct
      "quantity: IntField (required) The stock of the product     remaining
    }

All of the above feilds are required using serializers and a custom validate function is made to ensure name does'nt include special character , and the price and quantity of product cannot be negative.

## CRUD API's

All the API endpoints are surrounded by **api_view** decorator to ensure correctness of type of method call (POST,PUT,GET..etc).

### Create a New Product [POST]

As soon as the product is created we assign it an id which is equal to length of array dynamically in which it is inserted(products for in memory operation).


+ Url - http://127.0.0.1:8001/product/create

+ Request (application/json)

    {
    "name": "Badminton",
    "description": "Best purchase in market",
    "category": "Sports",
    "price": 5000,
    "brand": "konex",
    "quantity": 20
    }

+ Response 

    + Status - 201(created)

    + {
        "message": "Product created",
        "product": {
        "name": "Badminton",
        "description": "Best purchase in market",
        "price": 5000,
        "category": "Sports",
        "brand": "konex",
        "quantity": 20
            }
      }

<details>
<summary> Common errors </summary>
<br>

1) Missing feild error by serializer:

+ Request (application/json)
    
    {
    "name": "Badminton",
    "description": "Best purchase in market",
    "price": 5000,
    "brand": "konex",
    "quantity": 20
    }

+ Response 

    + Status - 400(Bad Request)

    + {
        "category": [
            "This field is required."
        ]
     }

2) Invalid quantity:

+ Request (application/json)

    {
    "name": "Badminton",
    "description": "Best purchase in market",
    "category": "Sports",
    "price": 5000,
    "brand": "konex",
    "quantity": -1
    }

+ Response

    + Status - 400(Bad Request)

    + {
        "quantity": [
            "Quantity should be greater than 0"
        ]
      }

3) Name Containing Special Characters:

+ Request (application/json)

    {
    "name": "Badminton@#",
    "description": "Best purchase in market",
    "category": "Sports",
    "price": 5000,
    "brand": "konex",
    "quantity": 20
    }

+ Response 

    + Status - 400(Bad Request)
  
    + {
        "name": [
            "Name cannot contain special characters"
        ]
     } 

</details>

### Update the Product [PUT/PATCH]

 **PUT**   - It requires all the feilds to be specified when updating 
 **PATCH** - It supports partial updation of the feild of product model

1)  **PUT Request**
+ Url-http://127.0.0.1:8001/product/update/1

+ Request (application/json)

    {
    "name": "Badminton",
    "description": "Best purchase in market",
    "category": "Sports",
    "price": 5000,
    "brand": "konex",
    "quantity": 20
    }

+ Response 

    + Status - 200(OK)

    +  {
        "message": "Product updated",
        "product": {
            "name": "Badminton",
            "description": "Best purchase in market",
            "price": 5000,
            "category": "Sports",
            "brand": "yonex",
            "quantity": 20
            }
        }
    


2) **PATCH Request**(Supports Partial Updation)
+ Url-http://127.0.0.1:8001/product/update/1

+ Request (application/json)

    {
    "price": 10000,
    "quantity": 20
    }

+ Response

    + Status -200(OK)

    + {
        "message": "Product updated",
        "product": {
            "name": "Badminton",
            "description": "Best purchase in market",
            "price": 10000,
            "category": "Sports",
            "brand": "yonex",
            "quantity": 20
            }
       }

### Delete the Product [DELETE]

1) **Delete Request**

+ Url-http://127.0.0.1:8001/product/delete/1

+ Response 
    
    + Status -200(OK)

    + {
        "message": "Product deleted successfully"
      }


### Get all products (using Pagination) [GET]

1) **Get Request**

+ Url-http://127.0.0.1:8001/product?page=1

+ Default page size has been set to 3.

+ Response

    + Status -200(OK)

    + {
        "status": true,
        "total_pages": 2,
        "current_page": 1,
        "products": [
                {
                "name": "Pen",
                "description": "A gel pen",
                "price": 20,
                "category": "Stationary",
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
                    "name": "ipad",
                    "description": "Best purchase in market",
                    "price": 100000,
                    "category": "Electronics",
                    "brand": "Apple",
                    "quantity": 10
                }
            ]
      }

<details>
<summary> Common errors </summary>
<br>

1) Page not an Integer

    + Url-http://127.0.0.1:8001/product?page=abc

    + Respose

        + Status -400(Bad Request)

        + {
            "status": false,
            "message": "Invalid page number"
          }

2) Page no. out of range

    + Url-http://127.0.0.1:8001/product?page=3

    + Respose

        + Status -400(Bad Request)

        + {
            "status": false,
            "message": "Page number out of  range"
          }

<details>




