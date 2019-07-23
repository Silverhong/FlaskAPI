from flask import Flask, request, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost/Evaluation"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Entity
class Staff(db.Model):
    __tablename__ = 'Staff'
    StaffId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SName = db.Column(db.String(100))
    Sex = db.Column(db.String(100))
    Dob = db.Column(db.Date)
    Pob = db.Column(db.String(100))
    CurrrentAddress = db.Column(db.String(255))
    Phone = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    DeptID = db.Column(db.Integer, db.ForeignKey('Department.DeptId'))
    OfficeId = db.Column(db.Integer,db.ForeignKey('Office.OfficeId'))


class Department(db.Model):
    __tablename__ = 'Department'
    DeptId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Deptname = db.Column(db.String(255))
    def __init__(self,name):
        self.Deptname=name

class Office(db.Model):
    __tablename__ = 'Office'
    OfficeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OfficeName = db.Column(db.String(255))


@app.route('/')
def Wellcome():
    return "Wellcome to Evaluation Web Service";


@app.route('/department/add', methods=['GET'])
def Add():
    name = request.args.get('name')
    dept = Department(str(name))
    db.session.add(dept)
    db.session.commit()
    return "Hello"


@app.route('/department/getAll')
def Get():
    listDict = []
    list = db.session.query(Department).all()
    for obj in list:
        listDict.append(Department(obj.Deptname).__dict__)
    return jsonify(listDict.__dict__)
# @app.route('/getEmp',methods=['GET'])
# def empList():
#     count = request.args.get('count')
#     list = []
#     for i in range(int(count)):
#         UserObj = User(i,"Hello "+str(i))
#         list.append(UserObj.__dict__)
#     return jsonify(list)


#RepositoryPattern