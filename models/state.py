#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv

class State(BaseModel, Base):
    """ State class """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        name = ""

    @property
    def cities(self):
        """ Retrieve all the cities """
        from models import storage
        cities_list = []
        dic = storage.all(City)
        for city in dic.values():
            if city.state_id == self.id:
                cities_list.append(city)
        return cities_list
