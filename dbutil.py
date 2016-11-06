import urllib
import requests
from sqlalchemy.engine import create_engine
from models.models import Base, Location
import os
from sqlalchemy.orm.session import sessionmaker

from weatherutil import WeatherUtil

"""
    Utility class to help with CRUD operations on database
"""

class DbUtil():

    """
        Create sqlite database if does not exists
        and initialize database session.
    """
    @staticmethod
    def create_db_session():
        db_name = 'sqlite:///weatherdb.sqlite3'
        engine = create_engine(db_name)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
        if not os.path.exists('weatherdb.sqlite3'):
            Base.metadata.create_all(engine)  # @UndefinedVariable
        return session
    """
        Utility method to save object to database
        Args:
            object: the object to be saved
    """
    def save(self, object):
        session = self.create_db_session()
        session.add(object)
        session.commit()

    """
        Utility method to evaluate if a location already exists
        in database
        Args:
            location_name: name of location to check
    """
    def location_exists(self, location_name):
        session = self.create_db_session();
        q = session.query(Location.id).filter(Location.location_name == location_name)
        return session.query(q.exists()).scalar()

    """
        Utility method to remove location, previously selected as default,
        from database
    """
    def remove_existing_default(self):
        session = self.create_db_session()
        q = session.query(Location.id).filter(Location.isDefault == True)
        if session.query(q.exists()).scalar():
            session.query(Location).update({Location.isDefault: False})
            session.commit()

    """
        Utility method to get location currently selected as default
    """
    def get_default(self):
        session = self.create_db_session()
        return session.query(Location).filter(Location.isDefault == True).first()

    """
        Utility method to retrieve all favourite locations stored in database

    """
    def find_all(self):
        session = self.create_db_session()
        return session.query(Location).all()


    def set_default(self, location_name):
        session = self.create_db_session()
        location = session.query(Location).filter(Location.location_name==location_name).first()
        location.isDefault=True
        session.commit()


    # TODO Refactor current query methods to have centralize place to perform queries
    def save_selected_location(self, location):
        search_query = WeatherUtil.get_property_from_config_file("WeatherUrls", "SearchLocation")
        query_formatted = search_query.format(urllib.quote(location))
        response = requests.get(query_formatted)
        self.save_location(response.json())

    def save_location(self, data):

        for city in data['RESULTS']:

            format_loc_name = city['name'].split(",")
            selected_location = Location(location_name=format_loc_name[0], location_code=city['c'],
                                         location_lat=city['lat'], location_long=city['lon'], isDefault=True)
            if not self.location_exists(format_loc_name[0]):
                self.remove_existing_default()
                self.save(selected_location)
            break
