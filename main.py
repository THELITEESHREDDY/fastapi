from fastapi import FastAPI,Request
from mock_data import products
from dtos import ProductDTO

app = FastAPI()



@app.get("/")
def home():
    return "Welcome to server!"



@app.get("/products")
def get_products():
    return products


@app.get("/products/{product_id}")
def get_product(product_id:int):

    for product in products:
        if product.get("id") == product_id:
            return product

        
    return {"message" : "product not found"}



@app.get("/greet")
def greet(request:Request):
    print(request.query_params)
    query = dict(request.query_params)

    return {"greet" : f"Hello,{query.get("name")} age is {query.get("age")}"}

# post send data from client to server
# through body, header(request header), query params


#pydantic 
#provides data types in python helps in validating data
@app.post("/create_products")
def create_product(product_data:ProductDTO):
    product_data =product_data.model_dump()

    print(product_data)
    products.append(product_data)
    return {"status": "Product Created Successfully...", "data" : products}


@app.put("/update_products/{product_id}")
def update_product(product_data:ProductDTO,product_id:int):

    for index,product in enumerate(products):
        if product.get("id") == product_id:
            products[index] = product_data
            return {"status" : "Product updated successfully..", "product":product_data}

    return {"error" : "Product not found"}


@app.delete("/delete_products/{product_id}")
def delete_product(product_id:int):

    for index,product in enumerate(products):
        if product.get("id") == product_id:
            delete_product = products.pop(index)
            return {"status" : "Product deleted successfully..", "product":delete_product}

    return {"error " : "product with id not found"}