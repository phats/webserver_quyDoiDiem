from numbers import Rational
from unittest import result
from webbrowser import get
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from db_setup import DiemThiVaSoHocSinhHonDiem2022, Student2021, Student2022

Base=declarative_base()
engine = create_engine('sqlite:///diemthi.db')
Base.metadata.bind = engine


KHOITHI={'A00':('toan','vatli','hoahoc'),
        'A01':('toan','vatli','ngoaingu'),
        'B00':('toan','hoahoc','sinhhoc'),
        'C00':('nguvan','lichsu','diali'),
        'D01':('toan','nguvan','ngoaingu')
        }
def getDiem(database,sbd):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    result=session.query(database).filter_by(sbd=sbd).first()
    return result

def diemTheoKhoi(database,khoi,sbd):
    diem=getDiem(database,sbd)
    if diem is None:
        return -1
    monThi=KHOITHI[khoi]
    
    diemTheoKhoi=0
    for mon in monThi:
        #Kiem tra thi sinh phai thuoc khoi nay khong?
        if getattr(diem,mon):
            diemTheoKhoi+=getattr(diem,mon)
        else: return -1
    return diemTheoKhoi
def soHocSinhHonDiem(database,khoi,sbd):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    diemKhoi=diemTheoKhoi(database,khoi,sbd)
    if diemKhoi==-1: return -1
    result=session.query(DiemThiVaSoHocSinhHonDiem2022).filter_by(diem=diemKhoi).first()
    return getattr(result,khoi)

def tongSoThiSinhTheoKhoi(database,khoi):
    monThi=KHOITHI[khoi]
    execute='''SELECT count(s.sbd) as sohocsinh  FROM %s s where s.%s is not NULL and s.%s is not NULL  and s.%s is not NULL'''%(database,*monThi)
    with engine.connect() as connection:
        result = connection.execute(text(execute))
        for row in result:
            return row['sohocsinh']
def quyDoiDiem(khoi,sbd):
    honDiem=soHocSinhHonDiem(Student2022,khoi=khoi,sbd=sbd)
    if honDiem==-1:
        return 'Thi sinh khong thuoc khoi nay'
    tongThiSinh22=tongSoThiSinhTheoKhoi('Student2022',khoi=khoi)
    ratio=honDiem/tongThiSinh22
    honDiem21=int(ratio*tongSoThiSinhTheoKhoi('Student2021',khoi=khoi))
    findMinDistance='''SELECT min(abs(d1.{khoi}-{honDiem21})) as minDistance
                FROM diemthi2021 d1
                '''.format(khoi=khoi,honDiem21=honDiem21)
    with engine.connect() as connection:
        result = connection.execute(text(findMinDistance))
        for row in result:
            minDistance=row['minDistance']
        diemGanNhat='''SELECT d.diem as Diem
                FROM diemthi2021 d
                WHERE abs(d.{khoi}-{honDiem21}) = {minDistance}'''.format(khoi=khoi,honDiem21=honDiem21,minDistance=minDistance)
        result = connection.execute(text(diemGanNhat))
        for row in result:
            return row['Diem']
