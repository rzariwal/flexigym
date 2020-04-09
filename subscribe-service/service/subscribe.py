import uuid
from datetime import datetime

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


def populateCart(id):
    # get all rows with this cartid from Item
    cartItems = Item.query.filter_by(cart_id=id).all()
    userCart = ShoppingCart('current')
    for each in cartItems:
        userCart.update(each)
    # return cartItems.__dict__


# add an item to cart
@subscribe_api_blueprint.route("/add", methods=['POST', "GET"])
def addToCart():
    try:
        # parse request
        post_data = request.get_json()
        user = request.json['user_id']
        package_id = request.json['product_id']
        count = request.json['qty']
        # try to get cart_id from request -> decides later to create a new cart or not.
        try:
            cart_id = request.json['cart_id']
        except KeyError:
            cart_id = -1
        # get all information about the item
        if ADVERTISE_API_OK:
            r = request.get(url=ADVERTISE_URL + "/" + package_id)
        else:
            r = Product(1, "p1", 100, 100)
        if count > int(r.qty):
            responseObject = {
                'status': 'fail',
                'message': 'Item requested is more than available quantity'
            }
            return jsonify(responseObject), 201
        else:
            # create the item object to be added to cart
            item = Item(package_id, 100, count)
            itemToCommit = Item(package_id, 100, count)

            if cart_id == -1:
                # create a new cart
                cart = ShoppingCart(user)
                cart.total = r.price
                cart.created_time = datetime.now()
                cart.payment_status = False
                cart.cart_status = 'OPEN'
                db.session.add(cart)
                db.session.commit()
                item.updateCartId(cart.cart_id)
                db.session.add(item)
                db.session.commit()

            else:
                # look into ShoppingCart db to get cart and use the same cart to add items
                cart = (ShoppingCart.query.filter_by(cart_id=cart_id)).first()
                # confirm if the cart is OPEN
                if cart.cart_status == 'OPEN':
                    # get cartItems from Item table.
                    cartItems = Item.query.filter_by(cart_id=cart.cart_id).all()
                    for each in cartItems:
                        i = Item(each.package_id,each.price,each.qty)
                        cart.update(i)
                    # calculate cart total
                    cart.update(itemToCommit)
                    cart.total = cart.get_total()
                    cart.updated_time = datetime.now()
                    cart.payment_status = False
                    cart.cart_status = 'OPEN'
                    db.session.add(cart)
                    db.session.commit()

                    # commit item to db first.
                    # commit item with respective cart_ids to database
                    itemToCommit.updateCartId(cart_id)
                    db.session.add(itemToCommit)
                    db.session.commit()

            # return cartId if add to cart is success.
            responseObject = {
                'status': 'success',
                'cart_Info': cart.to_json()
            }
            return make_response(jsonify(responseObject)), 200
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
