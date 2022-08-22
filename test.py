from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Student
Base=declarative_base()

if __name__=='__main__':
    engine = create_engine('sqlite:///diemthi2022.db')
    Base.metadata.bind = engine
    
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    test=session.query(Student).filter_by(sbd=str(b'01000030')).one()
    print(test.gdcd)
