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
class GymPackageModel(db.Model):
    __tablename__ = 'gym_package'
    id = Column(Integer, primary_key=True, autoincrement=True)
    package_name = Column(String(50))
    package_description = Column(String(500))
    price = Column(Integer)
    available_qty = Column(Integer)
    created_by = Column(String(300))
    updated_by = Column(String(300))
    valid_from = Column(DateTime(timezone=True))
    valid_to = Column(DateTime(timezone=True))
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def to_json(self):
        return {
            'id': self.id,
            'package_name': self.package_name,
            'package_description': self.package_description,
            'price': self.price,
            'available_qty': self.available_qty,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'valid_from': self.valid_from,
            'valid_to': self.valid_to,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }
