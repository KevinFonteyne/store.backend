from flask import Flask, request, abort
import json
import random
from data import me, catalog

app = Flask(__name__)

@app.get ("/api/about")
def get_about_me():
    about = me
    return json.dumps(about)

@app.get("/api/catalog")   
def get_catalog():
    return json.dumps(catalog)

@app.post("/api/catalog")
def save_product():
    product = request.get_json()
    # validating
    if not "title" in product:
        return abort (400, "ERROR: Title is required")
    # title should have at least 5 characters 
    if len(product["title"]) < 5:
        return abort (400, "ERROR: Title is too short")
    

    # must have a price
    if not "price" in product:
        return abort (400, "ERROR: Price is required")
    # price must be greater than 1
    if product["price"] < 1:
        return abort (400, "ERROR: Price must be greater than 1")
    
    # assigns a unique _id
    product["_id"] =  random.randint(100, 100000) 
    catalog.append(product)


    return product




    

@app.get("/api/count")
def get_count():
    count = len(catalog)
    return json.dumps(count)

@app.get("/api/catalog/total")
def catalog_total():
    total = 0
    for prod in catalog:
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

@app.get("/api/product/<id>")
def get_product_by_id(id):
    for prod in catalog:
        if prod["_id"] == id:
            return json.dumps(prod)

    return json.dumps("Error:Invalid id")  

@app.get ("/api/products/<category>")
def get_category(category):
    results = []
    for prod in catalog:
        if prod["category"].lower() == category.lower():
            results.append(prod)

    return json.dumps(results)

# step 1: create endpoint return {"you": rock }
@app.get("/api/game/<pick>")
def game(pick):
    
    num = random.randint(0,2)
    pc = ""
    if num == 0:
        pc = "rock"
    elif num == 1:
        pc = "paper"
    else:
        pc = "scissors" 


    winner =""           
    if pick == "paper":
        if pc == "rock":
            winner = "you"
        elif pc == "scissors":
            winner = "pc"
        else:
            winner = "draw"
    elif pick == "rock":
        if pc == "scissors":
            winner = "you"
        elif pc == "paper":
            winner = "pc"  
        else:
            winner = "draw" 
    elif pick == "scissors":
        if pc == "paper":
            winner = "you"
        elif pc == "rock":
            winner = "pc"  
        else:
            winner = "draw"                     
    results = {
        "you": pick,
        "pc": pc,
        "winner": winner
    }

    return json.dumps(results)


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
