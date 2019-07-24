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
    Dob = db.Column(db.Date)
    Pob = db.Column(db.String(100))
    CurrrentAddress = db.Column(db.String(255))
    Phone = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    DeptID = db.Column(db.Integer, db.ForeignKey('Department.DeptId',ondelete="CASCADE"))
    OfficeId = db.Column(db.Integer,db.ForeignKey('Office.OfficeId',ondelete="CASCADE"))


class Department(db.Model):
    __tablename__ = 'Department'
    DeptId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Deptname = db.Column(db.String(255))

class Office(db.Model):
    __tablename__ = 'Office'
    OfficeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OfficeName = db.Column(db.String(255))
    DeptId = db.Column(db.Integer,db.ForeignKey('Department.DeptId',ondelete='CASCADE'))

#Route
@app.route('/')
def Wellcome():
    return "Wellcome to Evaluation Web Service";


@app.route('/department/add', methods=['GET'])
def DeptAdd():
    name = request.args.get('name')
    dept = Department(str(name))
    db.session.add(dept)
    db.session.commit()
    return "Hello"

#Department
@app.route('/department/getAll')
def DeptGetAll():
    return jsonify(GetAll(Department))

@app.route('/department/getById')
def DeptGetById():
    return jsonify(GetById(Department,Department.DeptId,1))

@app.route('/department/deleteById')
def DeptDeleteById():
    return jsonify(DeleteById(Department,Department.DeptId,1))

#Office
@app.route('/office/getAll')
def OfficeAdd():
    return jsonify(GetAll(Office))

@app.route('/office/getById')
def OfficeGetById():
    return jsonify(GetById(Office,Office.OfficeId,2))

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
    if(len(GetById(type,colFilter,2)>0)):
        obj = db.session.query(type).filter(colFilter==2).delete()
        db.session.commit()
        return "Successfull"
    else:
        return "Unsuccessful"
