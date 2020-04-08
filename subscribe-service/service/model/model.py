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


'''
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



# Database Models
class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = Column(Integer, primary_key=True)

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
'''


# represent each item -> should aligned with advertise-api
class Item(db.Model):
    __tablename__ = 'item'
    unq_id = Column(Integer, nullable=False, primary_key=True)
    cart_id = Column(Integer)

    def __init__(self, unq_id, name, price, qty):
        self.unq_id = unq_id
        self.product_name = name
        self.price = price
        self.qty = qty
        self.cart_id = 0


# respresent a shopping cart -> includes 1 or more items with varying quantities
class ShoppingCart(db.Model):
    __tablename__ = 'shopping-cart'
    cart_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, foreign_key=True, nullable=False)
    total = Column(Integer)
    paid = Column(Boolean, unique=False, default=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    content = Column(String(100))

    def __init__(self, user, cartId):
        self.content = dict()
        self.user = user
        self.cart_id = cartId
        self.paid = False

    def update(self, item):
        if item.unq_id not in self.content:
            self.content.update({item.unq_id: item})
            return
        for k, v in self.content.get(item.unq_id).iteritems():
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


    def get_total(self):
        return sum([v.price * v.qty for _, v in self.content.iteritems()])

    def get_num_items(self):
        return sum([v.qty for _, v in self.content.iteritems()])

    def remove_item(self, key):
        self.content.pop(key)


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
