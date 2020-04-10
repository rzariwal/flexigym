import sys

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()


# we create the class Book and extend it from the Base Class.

# Database Models
class GymPackageModel(Base):
    __tablename__ = 'gym_package'
    id = Column(Integer, primary_key=True)
    package_name = Column(String(50))
    package_description = Column(String(500))
    price = Column(String(12))
    available_qty = Column(String(500))
    created_by = Column(String(300))
    updated_by = Column(String(300))
    #created_date = Column(DateTime(timezone=True), server_default=func.now())
    #updated_date = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def serialize(self):
        return {
            'id': self.id,
            'package_name': self.package_name,
            'package_description': self.package_description,
            'price': self.price,
            'available_qty': self.available_qty,
            'created_by': self.created_by,
            'updated_by': self.updated_by
            #,
            #'created_date': self.created_date,
            #'updated_date': self.updated_date
        }



# creates a create_engine instance at the bottom of the fil
# engine = create_engine('mysql+mysqlconnector://root:1234@localhost:3306/flexigym-advertise-service')
engine = create_engine('mysql+mysqlconnector://root:1234@flexigym-advertise-service-db/flexigym_advertise_service')
# engine = create_engine('sqlite:///books-collection.db')
Base.metadata.create_all(engine)