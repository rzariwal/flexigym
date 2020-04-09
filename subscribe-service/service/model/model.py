from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean

from sqlalchemy import create_engine

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)
    return db


def create_tables(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine


# represent each item -> should aligned with advertise-api
class Item(db.Model):

    __tablename__ = 'item'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, nullable = False)
    package_id = Column(Integer, nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    def __init__(self, unq_id, price, qty):
        self.package_id = unq_id
        self.price = price
        self.qty = qty

    def updateCartId(self, id):
        self.cart_id = id


# represent a shopping cart -> includes 1 or more items with varying quantities
class ShoppingCart(db.Model):

    __tablename__ = 'shopping-cart'
    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    cart_status = Column(db.String(20)) #OPEN --> CLOSED
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(Integer)
    payment_status = Column(Boolean, default=False)

    def __init__(self, user_id):
        self.content = dict() #content of cart
        self.user_id = user_id
        self.payment_status = False
        self.cart_status = "OPEN"

    def update(self, item):
        if item.unq_id not in self.content:
            self.content.update({item.unq_id: item})
            return
        try:
            for k, v in self.content.get(item.unq_id).items():
                if k == 'unq_id':
                    continue
                elif k == 'qty':
                    total_qty = v.qty + item.qty
                    if total_qty:
                        v.qty = total_qty
                        continue
                    self.remove_item(k)
                else:
                    v[k] = item[k]
        except AttributeError:
            pass

    def get_total(self):
        return sum([v.i_price * v.i_qty for _, v in self.content.items()])

    def get_num_items(self):
        return sum([v.qty for _, v in self.content.items()])

    def remove_item(self, key):
        self.content.pop(key)

class Product(object):

    def __init__(self, id, name, price, qty):
        self.product_id = id
        self.qty = qty
        self.name = name
        self.price = price
'''
    item1 = Item(1, "Banana", 1., 1)
    item2 = Item(2, "Eggs", 1., 2)
    item3 = Item(3, "Donut", 1., 5)
    cart = ShoppingCart()
    cart.update(item1)
    cart.update(item2)
    cart.update(item3)
    print "You have %i items in your cart for a total of $%.02f" % (cart.get_num_items(), cart.get_total())
    cart.remove_item(1)
    print "You have %i items in your cart for a total of $%.02f" % (cart.get_num_items(), cart.get_total())
'''
