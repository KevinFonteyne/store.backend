from flask import Flask, request, abort
import json
import random
from data import me, catalog
from flask_cors import CORS
from config import db
from bson import ObjectId


app = Flask(__name__)
CORS(app) # disable CORS, anyone can access the API

@app.get('/')
def home():
    return "Hello from flask!"

@app.get ("/api/about")
def get_about_me():
    about = me
    return json.dumps(about)

def fix_id(obj):
    obj["_id"] = str(obj["_id"])
    return obj

@app.get("/api/catalog")   
def get_catalog():
    cursor = db.Products.find({}) # read all products
    results = []
    for prod in cursor:
        prod = fix_id(prod)
        results.append(prod)

    return json.dumps(results)   


@app.post("/api/catalog")
def save_product():
    product = request.get_json()
    # validating
    if not "title" in product:
        return abort (400, "ERROR: Title is required")
    # title should have at least 5 characters 
    if len(product["title"]) < 2:
        return abort (400, "ERROR: Title is too short")
    

    # must have a price
    if not "price" in product:
        return abort (400, "ERROR: Price is required")
    # price must be greater than 1
    if product["price"] < 1:
        return abort (400, "ERROR: Price must be greater than 1")
    
    # assigns a unique _id
    # product["_id"] =  random.randint(100, 100000) 
    # catalog.append(product)
    db.Products.insert_one(product)
    
    # fix _id
    product["_id"] = str(product["_id"]) 


    return json.dumps(product)




    

@app.get("/api/count")
def get_count():
    cursor = db.Products.find({})
    products = []
    for prod in cursor:
        products.append(prod)

    count = len(products)
    return json.dumps(count)

@app.get("/api/catalog/total")
def catalog_total():
    total = 0
    cursor = db.Products.find({})
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)

@app.get("/api/catalog/cheapest")        
def catalog_cheapest(): 
    cheapest = catalog[0]
    for prod in catalog:
        if prod["price"] < cheapest["price"]:
            # found a better fit
            cheapest = prod
    return json.dumps(cheapest)


@app.post("/api/coupons")
def save_coupon():
    coupon = request.get_json()
    # validations
    if not "code" in coupon:
        abort(400, "code is required")
    if not "discount" in coupon:
        abort(400, "discount is required")

    db.CouponCodes.insert_one(coupon)
    coupon = fix_id(coupon)
    return json.dumps(coupon)        

@app.get("/api/coupons")
def get_coupons():
    cursor = db.CouponCodes.find({})
    results = []
    for cp in cursor:
        cp = fix_id(cp)
        results.append(cp)

    return json.dumps(results)    

@app.get("/api/product/<id>")
def get_product_by_id(id):
    prod = db.Products.find_one({"_id": ObjectId(id)})
    if not prod:
        return abort(404, "Product not found")
    prod = fix_id(prod)
    return json.dumps(prod)
    

@app.get ("/api/products/<category>")
def get_category(category):
    cursor = db.Products.find({ "category" : category})
    results = []
    for prod in cursor:
        prod = fix_id(prod)
        results.append(prod)

    return json.dumps(results)

# step 1: create endpoint return {"you": rock }
# @app.get("/api/game/<pick>")
# def game(pick):
    
#     num = random.randint(0,2)
#     pc = ""
#     if num == 0:
#         pc = "rock"
#     elif num == 1:
#         pc = "paper"
#     else:
#         pc = "scissors" 


#     winner =""           
#     if pick == "paper":
#         if pc == "rock":
#             winner = "you"
#         elif pc == "scissors":
#             winner = "pc"
#         else:
#             winner = "draw"
#     elif pick == "rock":
#         if pc == "scissors":
#             winner = "you"
#         elif pc == "paper":
#             winner = "pc"  
#         else:
#             winner = "draw" 
#     elif pick == "scissors":
#         if pc == "paper":
#             winner = "you"
#         elif pc == "rock":
#             winner = "pc"  
#         else:
#             winner = "draw"                     
#     results = {
#         "you": pick,
#         "pc": pc,
#         "winner": winner
#     }

#     return json.dumps(results)


# step 2: generate a random number between 0 and 2
    
# change the number to be rock, paper or scissors
# return 
# {
#   "you": paper,
#   "pc": rock,
# }

# step 3
# finish the logic to pick the winner





    


# app.run(debug=True)
