import sys
import os
# for a mapper code
from sqlalchemy import Column, ForeignKey, String, Integer
# for configuration in the class code
from sqlalchemy.ext.declarative import declarative_base
# to create a ForignKey relationsip
from sqlalchemy.orm import relationship
# will used for the configuration code
from sqlalchemy import create_engine

# will let sql know that our classes is a special SQLAlchemy classes
# that correspond to tables in our DB
Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    # mapper
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {'name': self.name, 'id': self.id}


class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    # create a ForignKey relatiosip between MenuItem and Restaurant
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


# insert into the end of file
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
