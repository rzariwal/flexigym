from datetime import datetime

from flask import request, jsonify, make_response
from sqlalchemy import engine, and_
from sqlalchemy.orm import sessionmaker
from model.model import ShoppingCart, Item, Product, db
from . import subscribe_api_blueprint
import requests
import json
from urllib.parse import urlparse, parse_qs

# service-endpoint
ADVERTISE_API_OK = True
# ADVERTISE_URL = "http://34.87.167.97:9100/packagesApi"
ADVERTISE_URL = "http://34.69.67.237/packagesApi"

NOTIFICATION_API_OK = True
# NOTIFICATION_URL = "http://34.87.167.97:7000/api/sms/send_sms"
NOTIFICATION_URL = "http://34.69.67.237/api/sms/send_sms"

USER_API_OK = True
# USER_URL = "http://34.87.167.97:7000/packagesApi"
USER_URL = "http://web:5000/packagesApi"

PAYMENT_API_OK = True
PAYMENT_URL = "http://34.69.67.237/payment"

Session = sessionmaker(bind=engine)
session = Session()

# add an item to cart
'''
{
    "user_id": "ekl",
    "package_id": 5,
    "qty": 1,
    "cart_id": 1
}
"cart_id" field is not for the first time.
'''


@subscribe_api_blueprint.route("/subscribe/add", methods=['POST', "GET"])
def addToCart():
    try:
        # parse request
        post_data = request.get_json()
        user = request.json['user_id']
        package_id = request.json['package_id']
        count = request.json['qty']
        #r = None
        # try to get cart_id from request -> decides later to create a new cart or not.
        try:
            cart_id = request.json['cart_id']
        except KeyError:
            cart_id = -1
        # get all information about the item
        if ADVERTISE_API_OK:
            response = requests.get(url=ADVERTISE_URL + "/" + str(package_id))
            r = Product(response.json()['packages']["id"], response.json()['packages']["package_name"], response.json()['packages']["price"], response.json()['packages']["available_qty"])
            print(r.to_json())
        else:
            r = Product(package_id, "p1", 100, 100)

        if count > int(r.qty):
            responseObject = {
                'status': 'fail',
                'message': 'Item requested is more than available quantity'
            }
            return jsonify(responseObject), 201
        else:
            # create the item object to be added to cart
            item = Item(package_id, r.price, count, r.name)
            itemToCommit = Item(package_id, r.price, count, r.name)

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
                        i = Item(each.package_id, each.price, each.qty, each.package_name)
                        cart.update(i)
                    # calculate cart total
                    cart.update(itemToCommit)
                    cart.total = cart.get_total()
                    cart.updated_time = datetime.now()
                    cart.payment_status = False
                    cart.cart_status = "OPEN"
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
        responseObject = {
            'status': 'fail',
            'message': 'Something went wrong!'
        }
        return make_response(jsonify(responseObject)), 500


# delete an item from cart
@subscribe_api_blueprint.route("/subscribe/delete", methods=['POST', 'GET'])
def deleteFromCart():
    try:
        # parse request -> get cart_id, package_id and quantity to be deleted.
        package_id = request.json['package_id']
        cart_id = request.json['cart_id']
        # get cart
        cart = (ShoppingCart.query.filter_by(cart_id=cart_id)).first()
        # delete the cart item
        item_to_delete = Item.query.filter_by(package_id=package_id).filter_by(cart_id=cart_id).first()
        if item_to_delete:
            db.session.delete(item_to_delete)
            cart.updated_time = datetime.now()
            db.session.commit()
            # get cart items
            cart_items = Item.query.filter_by(cart_id=cart_id).all()
            whole_cart = []
            for item in cart_items:
                i = Item(item.package_id, item.price, item.qty, item.package_name)
                cart.update(i)
            for k, v in cart.content.items():
                print(k, '->', v.to_json())
                whole_cart.append(v.to_json())

            response_object = {
                'status': 'success',
                'cartInfo': cart.to_json(),
                'cart_Items': whole_cart
            }
            return make_response(jsonify(response_object)), 200

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Delete Operation gone wrong!'
        }
    return make_response(jsonify(response_object)), 500


# get cart content with either cart_id or user_id
'''
example
{
   "cart_id": 1
   "user_id": 1
}
'''

@subscribe_api_blueprint.route("/subscribe/get", methods=['GET', "POST"])
def getCartItems():
    try:
        try:
            # get cart_Id and return all items in cart!
            cart_id = request.json['cart_id']
            # get cartItems from Item table.
            cart = (ShoppingCart.query.filter_by(cart_id=cart_id)).first()
            cartItems = Item.query.filter_by(cart_id=cart_id).all()
        except Exception as e:
            # get user_id and return all items in an OPEN cart!
            user_id = request.json['user_id']
            # cart = (ShoppingCart.query.filter_by(user_id=user_id)).filter_by(cart_status="OPEN").first()
            cart = (ShoppingCart.query.filter_by(user_id=user_id, cart_status="OPEN")).first()
            if(cart is not None):
                cartItems = Item.query.filter_by(cart_id=cart.cart_id).all()
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'No OPEN cart found for this user'
                }
                return make_response(jsonify(responseObject)), 404

        userCartObject = []
        for each in cartItems:
            i = Item(each.package_id, each.price, each.qty, each.package_name)
            cart.update(i)
        for k, v in cart.content.items():
            print(k, '->', v.to_json())
            userCartObject.append(v.to_json())
        # return cartId if add to cart is success.
        cart.total = cart.get_total()
        responseObject = {
            'status': 'success',
            'cartInfo': cart.to_json(),
            'cart_Items': userCartObject
        }
        return make_response(jsonify(responseObject)), 200

    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Something went wrong!'
        }
        return make_response(jsonify(responseObject)), 500


@subscribe_api_blueprint.route('/subscribe/test')
def hello_world():
    return 'test!'

@subscribe_api_blueprint.route('/subscribe/notify', methods=['GET', 'POST'])
def notify(to_number, content):
    '''
    s = requests.Session()
    s.auth = ('user', 'pass')
    s.headers.update({'x-test': 'true'})

    # both 'x-test' and 'x-test2' are sent
    s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
    :return:
    '''
    try:
        # user_detail = {"to_number": "+6594300664", "content": "You have paid SGD X for cart id:cart_id in FlexiGYM Portal.", "requestor_service": "subscribe", "requestor_service_event": "payment-made"}
        # user_detail = {"to_number": "+6594300664", "content": "You have paid SGD X for cart id:cart_id in FlexiGYM Portal."}
        user_detail = {"to_number": to_number,
                       "content": content }
        if NOTIFICATION_API_OK:
            print("calling notification url"+NOTIFICATION_URL)
            response = requests.post(url=NOTIFICATION_URL, json=user_detail)
            print("after calling notification url")
            return jsonify(message=response.status_code)
        # if response.status_code == 200:
            # return jsonify(message="SMS Sent.")

    except Exception as e:
        print(e)
        return "SMS Send failed."


# get cart id and proceed to call payment service
@subscribe_api_blueprint.route('/subscribe/checkout', methods=['GET', 'POST'])
def checkout():
    try:
        cart_id = request.json['cart_id']
        response = "*"
        #get cart info
        cart = (ShoppingCart.query.filter_by(cart_id=cart_id)).first()
        #payment_info = {"amount":str(cart.total)}
        print("cart is ok...")
        payment_info = {"amount":"1"}
        if PAYMENT_API_OK:
            response_payment = requests.post(url=PAYMENT_URL + "/create", json=payment_info)
            to_number = "+6594300664"
            # content = "You have paid SGD X for cart id:cart_id in FlexiGYM Portal."
            content = "You have paid SGD " + str(cart.total) + " for cart id:" + str(cart_id) + " in FlexiGYM Portal."
            notify(to_number, content)
            if response_payment.status_code == 200:
                cart.cart_status = "CLOSED"
                cart.payment_status = True
                cart.updated_time = datetime.now()
                db.session.add(cart)
                db.session.commit()
                resp_json = json.loads(response_payment.text)
                resp_json["cart_id"]=cart_id
                return make_response(jsonify(resp_json)), 200
            else:
                responseObject = {
                    "status":"fail",
                    "message":"payment creation status is not 200 OK"
                }
        else:
            return make_response(jsonify("PAYMENT_API not Ok")), 400

    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Something went wrong!'
        }
        return make_response(jsonify(responseObject)), 500

# update a cart Item; expect cartId, itemId, Qty.
@subscribe_api_blueprint.route('/subscribe/update', methods=['GET', 'POST'])
def updateItem():
    try:
        cart_id = request.json['cart_id']
        package_id = request.json['package_id']
        qty = request.json['quantity']

        # get cart
        cart = (ShoppingCart.query.filter_by(cart_id=cart_id)).first()
        # delete the cart item
        item_to_update = Item.query.filter_by(package_id=package_id).filter_by(cart_id=cart_id).first()
        if item_to_update:
            item_to_update.qty = qty
            db.session.add(item_to_update)
            cart.updated_time = datetime.now()
            db.session.commit()
            # get cart items
            cart_items = Item.query.filter_by(cart_id=cart_id).all()
            whole_cart = []
            for item in cart_items:
                i = Item(item.package_id, item.price, item.qty, item.package_name)
                cart.update(i)
            for k, v in cart.content.items():
                print(k, '->', v.to_json())
                whole_cart.append(v.to_json())
            cart.total = cart.get_total()
            response_object = {
                'status': 'success',
                'cartInfo': cart.to_json(),
                'cart_Items': whole_cart
            }
            return make_response(jsonify(response_object)), 200
        responseObject = {
            'status': 'success',
            'user_id': cart.user_id,
            'total_amount': cart.total
        }
        return make_response(jsonify(responseObject)), 200

    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Something went wrong!'
        }
        return make_response(jsonify(responseObject)), 500

@subscribe_api_blueprint.route('/subscribe/completeCheckout', methods=['GET', 'POST'])
def completeCheckout():
    try:
        cart_id = request.json['cart_id']
        payload=request.json['payload']
        parsed_params = parse_qs(urlparse(payload).query)
        response_payment = requests.get(PAYMENT_URL+"/complete", params = parsed_params)
        cart_items = Item.query.filter_by(cart_id=cart_id).all()

        for item in cart_items:
            if ADVERTISE_API_OK:
                response = requests.get(url=ADVERTISE_URL + "/" + str(item.package_id))
                if response.status_code == 200:
                    package_dict = response.json()['packages']
                    available_qty = response.json()['packages']["available_qty"]
                    package_dict["available_qty"]=available_qty-item.qty
                    response = requests.put(url=ADVERTISE_URL + "/" + str(item.package_id), params = package_dict)

        return make_response(response_payment.text.encode('utf8')), 200
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Something went wrong!'
        }
        return make_response(jsonify(responseObject)), 500


