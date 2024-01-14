#!/usr/bin/python3
""" database storage module """
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from sqlalchemy import create_engine
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from os import getenv


class DBStorage:
    """ db storage class """
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        env = getenv("HBNB_ENV")
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ all classes  """
        classes = [User, State, City, Amenity, Place, Review]
        dic = {}
        if cls:
            if cls in classes:
                for obj in self.__session.query(cls).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    dic[key] = obj
        else:
            for class_name in classes:
                for obj in self.__session.query(class_name).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    dic[key] = obj
        return dic

    def new(self, obj):
        """ add a new object to the database """
        if obj:
            self.__session.add(obj)

    def save(self):
        """ commit changes to the database """
        self.__session.commit()

    def delete(self, obj=None):
        """ remove an object from the database """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()
