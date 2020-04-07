import uuid
from . import subscribe_api_blueprint
from flask import request, jsonify
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from service.model.model import ShoppingCart, Item


# api-endpoint
ADVERTISE_URL = "http://localhost:4996/packagesApi"
Session = sessionmaker(bind=engine)
session = Session()

def generateCartId():
    cart_Id = uuid.uuid1()
    return cart_Id


# add an item to cart
@subscribe_api_blueprint.route("/add", methods=['POST'])
def addToCart():
    try:
        # parse request
        user = request.json['user_id']
        product_id = request.json['product_id']
        count = request.json['count']
        # get all information about the item
        r = request.get(url=ADVERTISE_URL + "/" + product_id)
        if (count > int(r.available_qty)):
            return jsonify(message="Sorry, we don't have that many packages available!"), 201
        else:
            # create the item object to be added to cart
            item = Item(product_id, r.package_name, r.price, count)

            #create a cart if doesn't exist in db.
            #query cart db and get get all cart of user and check cartId;
            #if cartId exists, don't create one...
            #session.query(ShoppingCart).filter_by(user=user).first()

            cart = ShoppingCart(user, generateCartId())
            cart.update(item)
            cart.add()
            cart.commit()

            #return cartId if add to cart is success.
            return jsonify(message=ShoppingCart.cart_id), 200
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
        return jsonify(message="Sorry, we don't have that many packages available!"), 201
        print(e)


# delete an item from cart
@subscribe_api_blueprint.route("/delete", methods=['POST'])
def deleteFromCart():
    try:
        # parse request
        product_id = request.json['product_id']
        pass
    except Exception as e:
        print(e)


# get cart content
@subscribe_api_blueprint.route("/get", methods=['GET'])
def getCartItems():
    try:

        pass
    except Exception as e:
        print(e)

@subscribe_api_blueprint.route('/test')
def hello_world():
    return 'test!'
