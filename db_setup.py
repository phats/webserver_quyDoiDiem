from numpy import genfromtxt
from sqlalchemy import Column, ForeignKey, Integer,String,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=1, converters={0: lambda s: str(s)})
    return data.tolist()

Base=declarative_base()

class Student(Base):
    __tablename__='student'

    sbd=Column(String(8), primary_key=True)
    toan=Column(Float)
    nguvan=Column(Float)
    ngoaingu=Column(Float)
    vatli=Column(Float)
    hoahoc=Column(Float)
    sinhhoc=Column(Float)
    lichsu=Column(Float)
    diali=Column(Float)
    gdcd=Column(Float)

if __name__=="__main__":
    engine=create_engine("sqlite:///diemthi2022.db")
    Base.metadata.create_all(engine)

    session=sessionmaker(bind=engine)
    s=session()
    try:
        filename='diem_thi_thpt_2022.csv'
        data=Load_Data(filename)
        for i in data:
            record=Student(sbd=i[0],
                toan=i[1],
                nguvan=i[2],
                ngoaingu=i[3],
                vatli=i[4],
                hoahoc=i[5],
                sinhhoc=i[6],
                lichsu=i[7],
                diali=i[8],
                gdcd=i[9]
                )
            print(record.sbd)
            s.add(record)
        s.commit()
    except:
        s.rollback()
    finally:
        s.close()
    print('Sucessfull import data')