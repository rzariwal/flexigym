from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, func

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


# Database Models
class Order(db.Model):
    __tablename__ = 'order'
    user_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    description = Column(String(100))
    name = Column(String(100), nullable=False)
    price = Column(db.Numeric(10, 2), nullable=False)
    requested_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    def to_json(self):
        return {
            'user_id': self.order_id,
            'order_id': self.order_id,
            'count': self.count,
            'description': self.description,
            'name': self.name,
            'price': self.price,
            'requested_time': self.requested_time,
            'updates_time': self.updated_time
        }


class ShoppingCart(object):

    def __init__(self):
        self.total = 0
        self.items = {}

    def add_item(self, item_name, quantity, price):
        self.total += (quantity * price)
        self.items = {item_name: quantity}

    def remove_item(self, item_name, quantity, price):
        self.total -= (quantity * price)
        if quantity > self.items[item_name]:
            del self.items[item_name]
        self.items[item_name] -= quantity

    def checkout(self, cash_paid):
        balance = 0
        if cash_paid < self.total:
            return "Cash paid not enough"
        balance = cash_paid - self.total
        return balance

'''
class Shop(ShoppingCart):

    def __init__(self):
        ShoppingCart.__init__(self)
        self.quantity = 100

    def remove_item(self):
        self.quantity -= 1
'''