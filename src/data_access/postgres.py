from sqlalchemy import create_engine, inspect
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect    

declarative_base = declarative_base()


class DbRepository:

    def __init__(self, db_string):
        self.db_engine = create_engine(db_string)
        self.session_macker = sessionmaker(self.db_engine)
        self.session = self.session_macker()
    
    def create(self, create_entity):
        self.session.add(create_entity)
        self.session.commit()
        return True

    def get_all(self, entity_class):
        result_entities = self.session.query(entity_class).all()
        return result_entities
    
    def get_with_fiter(self, entity_class, filter):
        result_entities = self.session.query(entity_class).filter(filter)
        return result_entities
    
    def get_only_with_fiter(self, entity_class, filter):
        result_entity = self.session.query(entity_class).filter(filter).one()
        return result_entity

    def update(self, updated_entity):
        self.session.add(updated_entity)
        self.session.commit()
        return True
 # print(inspect.has_table(SealCoin.__tablename__, "Public"))
        # db.execute(CreateSchema(SealCoin.__tablename__))

    # # Create 
    # doctor_strange = SealCoin(audience="small_seal_test", coin=100)  
    # session.add(doctor_strange)  
    # session.commit()