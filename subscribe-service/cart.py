from flask import Flask, request, redirect, url_for, session
from model import Order
from app import app

def getUserStatus():

    if 'auth_token' not in session:
        loggedIn = False
        firstName = ''
        noOfItems = 0


@app.route("/addtocart", methods=['POST'])
def addToCart():
    try:
        #parse request
        product_id = request.form.get('id')
        name = request.form.get('name')
        price = request.form.get('price')
        count = request.form.get('count')


        Order.addToOrder()

        pass
    except Exception as e:
        print(e)
