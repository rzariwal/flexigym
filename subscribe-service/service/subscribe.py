import uuid
from . import subscribe_api_blueprint
from flask import request, jsonify, make_response
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from service.model.model import ShoppingCart, Item, Product, db

# api-endpoint
ADVERTISE_API_OK = False
ADVERTISE_URL = "http://localhost:4996/packagesApi"
Session = sessionmaker(bind=engine)
session = Session()


def generateCartId():
    cart_Id = uuid.uuid1()
    return str(cart_Id)


# add an item to cart
@subscribe_api_blueprint.route("/add", methods=['POST',"GET"])
def addToCart():
    try:
        # parse request
        post_data = request.get_json()
        user = request.json['user_id']
        product_id = request.json['product_id']
        count = request.json['count']
        # try to get cart_id from request -> decides later to create a new cart or not.
        try:
            cart_id = request.json['cart_id']
        except KeyError:
            cart_id = -1
        # get all information about the item
        if ADVERTISE_API_OK:
            r = request.get(url=ADVERTISE_URL + "/" + product_id)
        else:
            r = Product(1,"p1",100, 100)
        if count > int(r.qty):
            return jsonify(message="Sorry, we don't have that many packages available!"), 201
        else:
            # create the item object to be added to cart
            item = Item(product_id, r.price, count)

            if cart_id == -1:
                # create a new cart
                cart = ShoppingCart(user)
                cart.update(item)
                cart.total = r.price
                cart.paid = False
                db.session.add(cart)
                db.session.commit()
            else:
                # look into ShopingCart db to get cart and use the same cart to add items
                cart = ShoppingCart.query.filter_by(cart_id=cart_id)
                cart.update(item)
                cart.total = 100
                cart.paid = False
                db.session.add(cart)
                db.session.commit()

            # return cartId if add to cart is success.

            responseObject =  {
                'status': 'success',
                'cart_info': cart.to_json()
            }
            return make_response(jsonify(responseObject)), 200
            pass
        pass
    except Exception as e:
        print(e)
        return jsonify(message="Sorry, exception"), 201


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
