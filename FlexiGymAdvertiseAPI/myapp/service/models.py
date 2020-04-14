from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

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
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    package_name = sqlalchemy.Column(sqlalchemy.String(50))
    package_description = sqlalchemy.Column(sqlalchemy.String(500))
    price = sqlalchemy.Column(sqlalchemy.Integer)
    available_qty = sqlalchemy.Column(sqlalchemy.Integer)
    created_by = sqlalchemy.Column(sqlalchemy.String(300))
    updated_by = sqlalchemy.Column(sqlalchemy.String(300))
    valid_from = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))
    valid_to = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))
    created_date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.func.now())
    updated_date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), onupdate=sqlalchemy.func.now())

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
