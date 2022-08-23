from cmath import isnan
from numpy import genfromtxt
from sqlalchemy import Column, ForeignKey, Integer,String,Float,text,sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
import math
KHOITHI={'A00':('toan','vatli','hoahoc'),
        'A01':('toan','vatli','ngoaingu'),
        'B00':('toan','hoahoc','sinhhoc'),
        'C00':('nguvan','lichsu','diali'),
        'D01':('toan','nguvan','ngoaingu')
        }
def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=1, converters={0: lambda s: str(s)})
    return data.tolist()

Base=declarative_base()

class Student2022(Base):
    __tablename__='student2022'

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
class Student2021(Base):
    __tablename__='student2021'

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
class DiemThiVaSoHocSinhHonDiem2022(Base):
    __tablename__='diemthi2022'

    diem=Column(Float(2),primary_key=True)
    for i in KHOITHI.keys():
        myVars=vars()
        myVars[i]=Column(Integer)
class DiemThiVaSoHocSinhHonDiem2021(Base):
    __tablename__='diemthi2021'

    diem=Column(Float(2),primary_key=True)
    for i in KHOITHI.keys():
        myVars=vars()
        myVars[i]=Column(Integer)
def convert_nan(f):
    if (isnan(f)):
        return sql.null()
    return f
if __name__=="__main__":
    engine=create_engine("sqlite:///diemthi.db")
    Base.metadata.create_all(engine)

    session=sessionmaker(bind=engine)
    s=session()
    try:
        # filename='diem_thi_thpt_2022.csv'
        # data=Load_Data(filename)
        # for i in data:
        #     record=Student2022(sbd=i[0][2:-1],
        #         toan=i[1],
        #         nguvan=i[2],
        #         ngoaingu=i[3],
        #         vatli=i[4],
        #         hoahoc=i[5],
        #         sinhhoc=i[6],
        #         lichsu=i[7],
        #         diali=i[8],
        #         gdcd=i[9]
        #         )
        #     print(i)
        #     s.add(record)
        # s.commit()
        # print('Read successful file 2022')
        # filename='diem_thi_thpt_2021.csv'
        # data=Load_Data(filename)
        # for i in data:
        #     # sbd=i[0][2:-1]
        #     # if (len(sbd)==7): sbd='0'+sbd
        #     # record=Student2021(
        #     #     sbd=sbd,
        #     #     toan=i[4],
        #     #     nguvan=i[5],
        #     #     ngoaingu=i[-1],
        #     #     vatli=i[6],
        #     #     hoahoc=i[7],
        #     #     sinhhoc=i[8],
        #     #     lichsu=i[10],
        #     #     diali=i[11],
        #     #     gdcd=i[12]
        #     #     )
        #     record=list(i)
        #     record[0]=record[0][2:-1]
        #     if (len(record[0])==7): record[0]='0'+record[0]
        #     addStudent2021='INSERT OR IGNORE into student2021 values({sbd},{toan},{nguvan},{ngoaingu},{vatli},{hoahoc},{sinhhoc},{lichsu},{diali},{gdcd})'.format(
        #         sbd=record[0],
        #         toan=convert_nan(record[4]),
        #         nguvan=convert_nan(record[5]),
        #         ngoaingu=convert_nan(record[-1]),
        #         vatli=convert_nan(record[6]),
        #         hoahoc=convert_nan(record[7]),
        #         sinhhoc=convert_nan(record[8]),
        #         lichsu=convert_nan(record[10]),
        #         diali=convert_nan(record[11]),
        #         gdcd=convert_nan(record[12]))
        #     print(addStudent2021)
        #     with engine.connect() as connection:
        #         result = connection.execute(text(addStudent2021))
        #     # try:
        #     #     s.commit()
        #     # #check UNIQUE constraint
        #     # except exc.SQLAlchemyError as e:
        #     #     print(e)
        #     #     s.rollback()
        # s.commit()
        # print('Read successful file 2021')
        for year in range(2,3):
            dataname='diemthi202'+str(year)
            database_diem='Student202'+str(year)
            i=0.0
            while i<=30:
                myVars=vars()
                for khoi in KHOITHI:
                    monthi=KHOITHI[khoi]
                    execute='{db_diem}.{0}+{db_diem}.{1}+{db_diem}.{2}>={diem}'.format(db_diem=database_diem,diem=i,*monthi)
                    vars()[khoi]=s.query(eval(database_diem)).filter(eval(execute)).count()
                exec='INSERT into {dataname} values({diem}'.format(dataname=dataname,diem=i)
                for khoi in KHOITHI:
                    exec+=',%s'%vars()[khoi]
                exec+=')'
                print(exec)
                with engine.connect() as connection:
                    result = connection.execute(text(exec))
                i=round(i+0.05,2)
            s.commit()
        print('Sucessfull import data')
    except Exception as e:
        print('Fail to commit database')
        print(e)
        s.rollback()
    finally:
        s.close()