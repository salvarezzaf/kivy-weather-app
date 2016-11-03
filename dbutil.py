from sqlalchemy.engine import create_engine
from models.models import Base, Location
import os
from sqlalchemy.orm.session import sessionmaker

class DbUtil():
    
    @staticmethod
    def create_db_session():    
        db_name = 'sqlite:///weatherdb.sqlite3'    
        engine = create_engine(db_name)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
        if not os.path.exists('weatherdb.sqlite3'):
            Base.metadata.create_all(engine)  # @UndefinedVariable
        return session
    
    def save(self, object):
        session = self.create_db_session()
        session.add(object)
        session.commit()
    
    def location_exists(self,location_name):
        session= self.create_db_session();
        q = session.query(Location.id).filter(Location.location_name==location_name)
        return session.query(q.exists()).scalar()
    
    def remove_existing_default(self):
        session = self.create_db_session()
        q = session.query(Location.id).filter(Location.isDefault==True)
        if session.query(q.exists()).scalar():
            session.query(Location).update({Location.isDefault:False})
            session.commit()
            
    def get_default(self):
        session = self.create_db_session()
        return session.query(Location).filter(Location.isDefault==True).first()
    '''
    @staticmethod
    def save_startup_location(session):
        statup_loc = Location(location_name="Glasgow",location_code="UK",location_lat="55.86999893",location_long="-4.42999983", isDefault=True)
        session.add(statup_loc)
        session.commit()
    '''