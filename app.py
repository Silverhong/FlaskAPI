from flask import Flask, request, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy, Model
from golden_marshmallows import GoldenSchema


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
    Dob = db.Column(db.String(100))
    Pob = db.Column(db.String(100))
    CurrentAddress = db.Column(db.String(255))
    Phone = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    DeptID = db.Column(db.Integer, db.ForeignKey('Department.DeptId',ondelete="CASCADE",onupdate="CASCADE"))
    OfficeId = db.Column(db.Integer,db.ForeignKey('Office.OfficeId',ondelete="CASCADE",onupdate="CASCADE"))
    Pid=db.Column(db.Integer,db.ForeignKey('Position.Pid',ondelete="CASCADE",onupdate="CASCADE"))
    CreatedBy = db.Column(db.String(100))
    UserGroupID = db.Column(db.Integer,db.ForeignKey('Usergroup.UserGroupID',ondelete="CASCADE",onupdate="CASCADE"));
class Usergroup(db.Model):
    __tablename__='Usergroup'
    UserGroupID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Name = db.Column(db.String(100))

class Position(db.Model):
    __tablename__='Position'
    Pid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Pname=db.Column(db.String(100))

class Department(db.Model):
    __tablename__ = 'Department'
    DeptId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Deptname = db.Column(db.String(255))
class Office(db.Model):
    __tablename__ = 'Office'
    OfficeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OfficeName = db.Column(db.String(255))
    DeptId = db.Column(db.Integer,db.ForeignKey('Department.DeptId',ondelete='CASCADE',onupdate="CASCADE"))

#Route
@app.route('/')
def Wellcome():
    return "Wellcome to Evaluation Web Service";

#Department
@app.route('/department/getAll')
def DeptGetAll():
    return jsonify(GetAll(Department))

@app.route('/department/getById')
def DeptGetById():
    return jsonify(GetById(Department,Department.DeptId,1))

@app.route('/department/Add',methods=["POST"])
def DeptAdd():
    # getJSON
    json = request.get_json()
    Add(Department,json)
    return "Successfull"
@app.route('/department/deleteById',methods=["DELETE"])
def DeptDeleteById():
    id = request.args.get('DeptId')
    return jsonify(DeleteById(Department,Department.DeptId,id))

#Office
@app.route('/office/getAll')
def OfficeGetAll():
    return jsonify(GetAll(Office))
@app.route('/office/Add',methods=["POST"])
def OfficeAdd():
    json = request.get_json()
    Add(Office,json)
    return "successfull"

@app.route('/office/getById')
def OfficeGetById():
    return jsonify(GetById(Office,Office.OfficeId,2))

@app.route('/office/deleteById', methods=["DELETE"])
def OfficeDeleteById():
    id = request.args.get('OfficeId')
    return jsonify(DeleteById(Office,Office.OfficeId,id))

#Staff
@app.route('/staff/getAll')
def StaffGetAll():
    return jsonify(GetAll(Staff))
@app.route('/staff/Add',methods=["POST"])
def StaffAdd():
    json = request.get_json()
    Add(Staff,json)
    return "Successfull"
@app.route('/staff/deleteById',methods=["DELETE"])
def StaffDeleteById():
    id = request.args.get('StaffId')
    return jsonify(DeleteById(Staff,Staff.StaffId,id))

#Position
@app.route('/position/getAll')
def positionGetAll():
    return jsonify((GetAll(Position)))

#Usergroup
@app.route('/usergroup/getAll')
def usergroupGetAll():
    return jsonify((GetAll(Usergroup)))
#RepositoryPattern
def GetAll(type):
    listRaw = db.session.query(type).all()
    schema = GoldenSchema(type)
    list = []
    for obj in listRaw:
        deserialize = schema.dump(obj).data
        list.append(deserialize)
    return list

def GetById(type,colFilter,value):
    schema = GoldenSchema(type)
    obj = db.session.query(type).filter(colFilter==value).first()
    return schema.dump(obj).data

def DeleteById(type,colFilter,value):
    schema = GoldenSchema(type)
    if(bool(db.session.query(type).filter(colFilter==value).first())):
        obj = db.session.query(type).filter(colFilter==value).delete()
        db.session.commit()
        return "Successfull"
    else:
        return "Unsuccessful"
def Add(type,json):
    # #Instance DAO
    schema = GoldenSchema(type);
    ##Deserialize
    obj = schema.load(json).data
    db.session.add(obj)
    db.session.commit()