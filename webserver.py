from flask import Flask,render_template,request
from quyDoiDiem import quyDoiDiem,diemTheoKhoi,getDiem
from db_setup import Student2022

app=Flask(__name__)
KHOITHI={'A00':('toan','vatli','hoahoc'),
        'A01':('toan','vatli','ngoaingu'),
        'B00':('toan','hoahoc','sinhhoc'),
        'C00':('nguvan','lichsu','diali'),
        'D01':('toan','nguvan','ngoaingu')
        }
@app.route('/')
@app.route('/home',methods=['POST','GET'])
def traCuu():
    if request.method=='GET':
        return render_template('home.html',KHOITHI=KHOITHI)
    elif request.method=='POST':
        sbd=request.form['sbd']
        print(sbd)
        khoi=request.form['khoi']
        print(khoi)
        diem2021=quyDoiDiem(khoi,sbd)
        diem2022=diemTheoKhoi(Student2022,khoi,sbd)
        diem=getDiem(Student2022,sbd)
        return render_template('home_respone.html',diem2021=diem2021,sbd=sbd,KHOITHI=KHOITHI,isFloat=isinstance(diem2021,float),khoi=khoi,diem2022=diem2022,diem=diem)
if __name__=='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=8888)