from sqlalchemy.engine import create_engine
from models.models import Base
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
    
    