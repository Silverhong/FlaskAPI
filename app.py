from flask import Flask, request, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import func
from golden_marshmallows import GoldenSchema
import json
import psycopg2


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost/Evaluation"
connect=psycopg2.connect(database="Evaluation",user='postgres',password='123456',host='localhost',port='5432')
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

class User(db.Model):
    __tablename__ = 'User'
    UserId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Regcom_id = db.Column(db.Integer,db.ForeignKey('RegisterCompany.Regcom_id',onupdate='CASCADE',ondelete='CASCADE'))
    Username = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    Created_date = db.Column(db.String(100))
    Status = db.Column(db.String(100))
    StaffId = db.Column(db.String(100))
    Role = db.Column(db.String(100))


class RegisterCompany(db.Model):
    __tablename__='RegisterCompany'
    Regcom_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Regcom_name = db.Column(db.String(100))
    Address = db.Column(db.String(100))
    Phone = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Admin_Username = db.Column(db.String(100))
    Admin_Password = db.Column(db.String(100))
    Status = db.Column(db.String(100))

class EvaluationType(db.Model):
    __tablename__='EvaluationType'
    EvTId = db.Column(db.Integer,primary_key=True,autoincrement=True)
    EvTName = db.Column(db.String(100))

class EvaluationQuestion(db.Model):
    __tablename__='EvaluationQuestion'
    EvQId = db.Column(db.Integer,primary_key=True,autoincrement=True)
    CreatedDate = db.Column(db.String(100))
    EvQDescription = db.Column(db.String(100))
    StaffId = db.Column(db.Integer)

class EvaluationQuestionDetail(db.Model):
    __tablename__ = 'EvalutaionQuestionDetail'
    EvQId = db.Column(db.Integer,db.ForeignKey('EvaluationQuestion.EvQId',ondelete='CASCADE',onupdate='CASCADE'),primary_key=True)
    EvQDetailId = db.Column(db.Integer,primary_key=True,autoincrement=True)
    EvQName = db.Column(db.String(100))
    MinScore = db.Column(db.Integer)
    MaxScore = db.Column(db.Integer)
    Answer = db.Column(db.String(100))

class Evaluation(db.Model):
    __tablename__="Evaluation"
    EvId = db.Column(db.Integer,primary_key=True,autoincrement=True,onupdate='CASCADE')
    EvDescription = db.Column(db.String(100))
    FromDate = db.Column(db.String(100))
    ToDate = db.Column(db.String(100))
    CreatedDate = db.Column(db.String(100))
    EvTId = db.Column(db.Integer,db.ForeignKey('EvaluationType.EvTId',ondelete='CASCADE',onupdate='CASCADE'))
    StaffId = db.Column(db.Integer)
    Status = db.Column(db.String(100))

class EvaluationDetail(db.Model):
    __tablename__ = "EvaluationDetail"
    EvId = db.Column(db.Integer,db.ForeignKey('Evaluation.EvId',onupdate='CASCADE',ondelete='CASCADE'),primary_key=True)
    EvQId = db.Column(db.Integer,db.ForeignKey('EvaluationQuestion.EvQId'),primary_key=True)
    CreatedDate = db.Column(db.String(100))

class AssignStaff(db.Model):
    __tablename__="AssignStaff"
    Aid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Status = db.Column(db.String(100))
    Description = db.Column(db.String(100))
    EvID = db.Column(db.Integer,db.ForeignKey('Evaluation.EvId',ondelete='CASCADE',onupdate='CASCADE'))
    StaffId = db.Column(db.Integer,db.ForeignKey('Staff.StaffId',onupdate='CASCADE',ondelete='CASCADE'))

class AssignScore(db.Model):
    __tablename__ = "AssignScore"
    AssignScoreId = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Date = db.Column(db.String(100))
    AvgScore = db.Column(db.Integer)
    ForAssignId = db.Column(db.Integer,db.ForeignKey('AssignStaff.Aid',ondelete='CASCADE',onupdate='CASCADE'))
    ByAssignId = db.Column(db.Integer,db.ForeignKey('AssignStaff.Aid',ondelete='CASCADE',onupdate='CASCADE'))

class AssignScoreDetail(db.Model):
    __tablename__ = "AssignScoreDetail"
    AssignScoreDetailId = db.Column(db.Integer,primary_key=True,autoincrement=True)
    AssignScoreId = db.Column(db.Integer,db.ForeignKey('AssignScore.AssignScoreId',ondelete='CASCADE',onupdate='CASCADE'))
    EvQId = db.Column(db.Integer)
    Score = db.Column(db.Integer)
#DAO
class EvaluationDetailDAO():
    Sname = ""
    Score = ""
    Status = ""

#Route
@app.route('/')
def Wellcome():
    return "Wellcome to Evaluation Web Service";

#AssignScore
@app.route('/assignscore/Add',methods=["POST"])
def assignScoreAdd():
    json = request.get_json()
    for o in json:
        assign = {}
        assign['Date'] = o['Date']
        assign['AvgScore'] = o['AvgScore']
        assign['ForAssignId'] = o['ForAssignId']
        assign['ByAssignId'] = o['ByAssignId']
        schema = GoldenSchema(AssignScore)
        obj = schema.load(assign).data
        db.session.add(obj)
        db.session.commit()
        assignId = obj.AssignScoreId
        detail = o['ListAssignScoreDetails']
        detailSchema = GoldenSchema(AssignScoreDetail)
        for row in detail:
            row['AssignScoreId']=str(assignId)
            dObj = detailSchema.load(row).data
            db.session.add(dObj)
    db.session.commit()
    return "Successful"


#AssignStaff
@app.route('/assignstaff/Add',methods=["POST"])
def assignStaffAdd():
    json = request.get_json()
    for o in json:
        schema = GoldenSchema(AssignStaff);
        obj = schema.load(o).data
        db.session.add(obj)
    db.session.commit()
    return "Successful"

@app.route('/assignstaff/updateStatusByAid',methods=["POST"])
def assignStaffUpdateStatus():
    aid = request.args.get("Aid")
    sql = r"""UPDATE "AssignStaff" set "Status" = 'InActive' WHERE "Aid" = """+aid
    cursor = con.cursor()
    cursor.execute()
    cursor.commit()
    return "Successful"

#UserGroup
@app.route('/usergroup/getAll')
def UserGroupGetAll():
    return jsonify(GetAll(Usergroup))

@app.route('/usergroup/Add',methods=["POST"])
def UserGroupAdd():
    json = request.get_json()
    Add(Usergroup,json)
    return "Successful"

@app.route('/usergroup/deleteById',methods=["DELETE"])
def UserGroupDeleteById():
    id = request.args.get("UserGroupID")
    DeleteById(Usergroup,Usergroup.UserGroupID,id)
    return "Successful"

#Position
@app.route('/position/getAll')
def PositionGetAll():
    return jsonify(GetAll(Position))

@app.route('/position/deleteById',methods=["DELETE"])
def PositionDeleteById():
    id = request.args.get('Pid')
    DeleteById(Position,Position.Pid,id)
    return "Successful"

@app.route('/position/Add',methods=["POST"])
def PositionAdd():
    json = request.get_json()
    Add(Position,json)
    return "Successfull"

#Evaluation
@app.route('/evaluation/getAll')
def EvGetAll():
    return jsonify(GetAll(Evaluation))

@app.route('/evaluation/deleteById',methods=["DELETE"])
def EvDeleteById():
    id = request.args.get('EvId')
    DeleteById(Evaluation,Evaluation.EvId,id)
    return "Successful"

@app.route('/evaluation/Add',methods=["POST"])
def EvAdd():
    json = request.get_json()
    Add(Evaluation,json)
    id = db.session.query(Evaluation).order_by(Evaluation.EvId.desc()).first()
    return str(id.EvId)

@app.route('/evaluation/getById')
def EvGetById():
    id = request.args.get('EvId')
    return jsonify(GetById(Evaluation,Evaluation.EvId,id))

@app.route('/evaluation/getByStaffId')
def EvGetByStaffId():
    result = {}
    staffId = request.args.get("StaffId")
    sql = r"""SELECT "Evaluation"."EvId","EvDescription" from "Evaluation" WHERE "Evaluation"."EvId"=(SELECT MAX("AssignStaff"."EvID") FROM "AssignStaff" WHERE "StaffId"="""+staffId+")"
    cursor = connect.cursor()
    cursor.execute(sql)
    evaId = cursor.fetchone()
    if(evaId==None):
        return "[]"
    evaDescription = str(evaId[1])
    evStaffSql = r"""SELECT "StaffId","Aid" from "AssignStaff" WHERE "EvID"="""+str(evaId[0])
    cursor.execute(evStaffSql)
    evaStaff = cursor.fetchall()
    listEvStaff = []
    for row in evaStaff:
        obj = {}
        obj['id']=row[0]
        obj['assignId']=row[1]
        listEvStaff.append(obj)
    evAssignId = r"""SELECT "Aid" from "AssignStaff" WHERE "EvID"="""+str(evaId[0])+""" AND "StaffId"="""+str(staffId)
    cursor.execute(evAssignId)
    assignId = cursor.fetchone()
    result['AssignId']=assignId[0]
    result['EvaDescription'] = evaDescription
    result['Staff']=listEvStaff
    evQuestionSql = r"""SELECT "EvaluationQuestion"."EvQId","EvaluationQuestion"."EvQDescription" FROM "EvaluationQuestion" INNER JOIN "EvaluationDetail" ON "EvaluationDetail"."EvQId" = "EvaluationQuestion"."EvQId" WHERE "EvaluationDetail"."EvId"="""+str(evaId[0])
    cursor.execute(evQuestionSql)
    evaQuestion = cursor.fetchall()
    listEvQuestion = []
    for row in evaQuestion:
        obj = {}
        obj['EvQId']=row[0]
        obj['Description']=row[1]
        listEvQuestion.append(obj)
    result['Questions']=listEvQuestion
    return jsonify(result)


#EvaluationDetail
@app.route("/evaluationDetail/Add",methods=["POST"])
def EvDAdd():
    jsonText = request.get_json()
    for o in jsonText:
        schema = GoldenSchema(EvaluationDetail);
        obj = schema.load(o).data
        db.session.add(obj)
    db.session.commit()
    return "Successful"

@app.route('/evaluationDetail/getByEvId')
def EvDGetByEvId():
    id = request.args.get('EvId')
    schema = GoldenSchema(EvaluationQuestion)
    cursor = connect.cursor()
    sql='SELECT "Staff"."SName",SUM ("AssignScoreDetail"."Score" ) AS Total FROM "Staff" INNER JOIN "AssignStaff" ON "Staff"."StaffId" = "AssignStaff"."StaffId" LEFT JOIN "AssignScore" ON "AssignScore"."ForAssignId" = "AssignStaff"."Aid" LEFT JOIN "AssignScoreDetail" ON "AssignScoreDetail"."AssignScoreId" = "AssignScore"."AssignScoreId" GROUP BY "Staff"."SName","AssignStaff"."EvID" HAVING "AssignStaff"."EvID"='+id
    cursor.execute(sql)
    list =cursor.fetchall()
    result = []
    for row in list:
        obj = {}
        obj['Sname'] = row[0]
        obj['Total'] = row[1] or 0
        result.append(obj)
    EvQ = db.session.query(EvaluationQuestion).join(EvaluationDetail).filter(EvaluationDetail.EvId == id).all()
    listEvQ=[]
    for row in EvQ:
        listEvQ.append(schema.dump(row).data)
    biglist = {}
    biglist['VEvaluationDetailStaff']=result
    biglist['VEvaluationQuestion']=listEvQ
    return jsonify(biglist)



#EvaluationQuestion
@app.route('/evaluationQuestion/getAll')
def EvQGetAll():
    return jsonify(GetAll(EvaluationQuestion))

@app.route('/evaluationQuestion/Add',methods=["POST"])
def EvQAdd():
    json = request.get_json()
    Add(EvaluationQuestion,json)
    schema = GoldenSchema(EvaluationQuestion)
    id = db.session.query(EvaluationQuestion).order_by(EvaluationQuestion.EvQId.desc()).first()
    return str(id.EvQId)

@app.route('/evaluationQuestion/deleteById',methods=["DELETE"])
def EvQDeleteById():
    id = request.args.get('EvQId')
    return jsonify(DeleteById(EvaluationQuestion,EvaluationQuestion.EvQId,id))

#EvaluationQuestionDetail
@app.route('/evaluationQuestionDetail/Add',methods=["POST"])
def EvQDAdd():
    json = request.get_json()
    Add(EvaluationQuestionDetail, json)
    return "Successfull"
@app.route('/evaluationQuestionDetail/getById')
def EvQDGetById():
    EvQId = request.args.get('EvQId')
    return jsonify(GetById(EvaluationQuestionDetail,EvaluationQuestionDetail.EvQId,EvQId))

#EvaluationType
@app.route('/evaluationType/getAll')
def EvtTypeGetAll():
    return jsonify(GetAll(EvaluationType))

@app.route('/evaluationType/Add',methods=["POST"])
def EvtTypeAdd():
    json = request.get_json()
    Add(EvaluationType,json)
    return "Successful"

@app.route('/evaluationType/deleteById',methods=["DELETE"])
def EvtTypeDelete():
    id = request.args.get('EvTId')
    return jsonify(DeleteById(EvaluationType,EvaluationType.EvTId,id))

#Department
@app.route('/department/getAll')
def DeptGetAll():
    return jsonify(GetAll(Department))

@app.route('/department/getById')
def DeptGetById():
    id = request.args.get('DeptId')
    return jsonify(GetById(Department,Department.DeptId,id))

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

#User
@app.route('/user/getAll')
def UserGetAll():
    return jsonify(GetAll(User))

@app.route('/user/deleteById',methods=["DELETE"])
def UserDeleteById():
    id = request.args.get('UserId')
    return jsonify(DeleteById(User,User.UserId,id))

@app.route('/user/Add',methods=["POST"])
def UserAdd():
    json = request.get_json()
    Add(User,json)
    return "Successfull"

@app.route('/user/CheckExist',methods=["POST"])
def UserCheck():
    json = request.get_json()
    schema = GoldenSchema(User);
    obj = schema.load(json).data
    if (bool(db.session.query(User).filter(User.Username.like(obj.Username), User.Password.like(obj.Password)).first())):
        row = db.session.query(User).filter(User.Username.like(obj.Username), User.Password.like(obj.Password)).first()
        schema = GoldenSchema(User)
        obj = schema.dump(row).data
        return jsonify(obj)
    else:
        return "Unsuccessfull"

#Company
@app.route('/company/CheckExist')
def CompanyExist():
    value = request.args.get('Regcom_name')
    if (bool(db.session.query(RegisterCompany).filter(RegisterCompany.Regcom_name == value).first())):
        obj = db.session.query(RegisterCompany).filter(RegisterCompany.Regcom_name == value).first()
        schema = GoldenSchema(RegisterCompany)
        obj = schema.dump(obj).data
        return jsonify(obj)
    else:
        return "0"

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
    list = []
    list.append(schema.dump(obj).data)
    return list

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

