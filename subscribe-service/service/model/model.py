from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, orm

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
    cart_id = Column(Integer, nullable=False)
    package_id = Column(Integer, nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    def __init__(self, unq_id, price, qty):
        self.package_id = unq_id
        self.price = price
        self.qty = qty

    def updateCartId(self, id):
        self.cart_id = id

    def to_json(self):
        return {
            'item_id': self.item_id,
            'cart_id': self.user_id,
            'package_id': self.package_id,
            'qty': self.qty,
            'price': self.price
        }


# represent a shopping cart -> includes 1 or more items with varying quantities
class ShoppingCart(db.Model):
    __tablename__ = 'shopping-cart'
    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    cart_status = Column(db.String(20))  # OPEN --> CLOSED
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(Integer)
    payment_status = Column(Boolean, default=False)


    def __init__(self, user_id):
        self.content = dict()  # content of cart
        self.user_id = user_id
        self.payment_status = False
        self.cart_status = "OPEN"

    @orm.reconstructor
    def init_on_load(self):
        self.content = dict()  # content of cart

    def update(self, item):
        if item.package_id not in self.content:
            self.content.update({item.package_id: item})
            return
        else:
            try:
                self.content[item.package_id].qty = self.content[item.package_id].qty + item.qty
            except AttributeError:
                pass
            return

    def get_total(self):
        return sum([v.price * v.qty for _, v in self.content.items()])

    def get_num_items(self):
        return sum([v.qty for _, v in self.content.items()])

    def remove_item(self, key):
        self.content.pop(key)

    def to_json(self):
        return {
            'cart_id': self.cart_id,
            'user_id': self.user_id,
            'cart_status': self.cart_status,
            'created_time': self.created_time,
            'updated_time': self.updated_time,
            'total': self.total,
            'payment_status': self.payment_status
        }


class Product(object):

    def __init__(self, id, name, price, qty):
        self.product_id = id
        self.qty = qty
        self.name = name
        self.price = price