from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean


Base = declarative_base()

class Location(Base):
    
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True)
    location_name = Column(String, nullable= False)
    location_code = Column(String, nullable= False)
    location_lat = Column(String, nullable = False)
    location_long = Column(String, nullable = False)
    isDefault = Column(Boolean, nullable = False)

class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    temp_unit = Column(String, nullable= False)