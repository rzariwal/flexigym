from flask import request, jsonify

from app import app
from service.model.model import ShoppingCart, Item

# api-endpoint 
ADVERTISE_URL = "http://localhost:4996/packagesApi"

#add an item to cart
@app.route("/add", methods=['POST'])
def addToCart():
    try:
        #parse request
        product_id =  request.json['product_id']
        count = request.json['count']
        #get all information about the item
        r = request.get(url = ADVERTISE_URL + "/" + product_id)
        if (count > int(r.available_qty)):
            return jsonify(message = "Sorry, we don't have that many sessions!" ), 201
        else:
            #try to add the item to cart
            item = Item(product_id, r.package_name, count)
            ShoppingCart.update(item)
            ShoppingCart.add()
            ShoppingCart.commit()
            pass
        """
        #advertise_api return
        'id': self.id,
            'package_name': self.package_name,
            'package_description': self.package_description,
            'price': self.price,
            'available_qty': self.available_qty,
            'created_by': self.created_by,
            'updated_by': self.updated_by
        )"""
        pass
    except Exception as e:
        print(e)

#delete an item from cart
@app.route("/delete", methods=['POST'])
def deleteFromCart():
    try:
       #parse request
        product_id =  request.json['product_id']
        pass
    except Exception as e:
        print(e)

#get cart content
@app.route("/get", methods=['GET'])
def getCartItems():
    try:

        pass
    except Exception as e:
        print(e)