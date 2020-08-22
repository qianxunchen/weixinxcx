from flask import Blueprint, request,g
from models.db_base import *
from models.apireturn import *
from libs.auth_token import auth, generate_token
from models import db
import re

user = Blueprint('user', __name__)


#注册
@user.route('/register', methods=['POST'])
def register():
    # email = request.args.get('email')
    # name = request.args.get('name')
    # password = request.args.get('password')
    data = request.get_json('name')
    name = data['name']
    email = data['email']
    password = data['password']
    if len(email) > 7:
        if re.match("[\w]+@[0-9a-zA-z]+(\.[a-zA-z0-9]+)", email) != None:
            # password = md(password)
            User.register_test(name,email,password)
            return Success()
        else:
            return jsonify({"msg":"邮箱不可用"})
    else:
        return jsonify({"msg":"邮箱错误"})

# 登陆
@user.route('/login', methods=['POST'])
def login():
    # email = request.args.get('email')
    # password = request.args.get('password')
    data = request.get_json('name')
    name = data['name']
    password = data['password']
    # password = md(data['password'])
    user = User.query.filter_by(name=name, password=password).first()
    if (user):
        token = generate_token(user.id)
        data = {
            "token": token.decode('ascii'),
            "msg": '登陆成功'
        }
        return jsonify(data)
    else:
        return Error()

#修改密码
@user.route('/changePassword', methods=['POST'])
@auth.login_required
def changePassword():
    # email = request.args.get('email')
    # # password = md(data['password'])
    # password = request.args.get('password')
    data = request.to_json('email')
    email = data['email']
    # password = md(data['password'])
    password = data['password']
    User.query.filter_by(email=email).update({"password": password})
    db.session.commit()
    return Success()

# 用户页
@user.route('/myuser')
@auth.login_required
def myuser():
    id = g.user.id
    userdata = User.query.filter_by(id=id).first()
    name = userdata.name
    locatioon = userdata.location
    data = {
        "name":name,
        "location":locatioon
    }
    return jsonify(data),200


# 订单
@user.route('/dindan')
@auth.login_required
def dindan():
    uid = g.user.id
    print(uid)
    inventorys = {}
    batchs = []
    stocks = Inventory.query.filter(Inventory.uid==uid).all()
    if(len(stocks)==0):
        data = {
            "msg": "没有库存，快去进货吧！",
        }
        return jsonify(data)
    else:
        data = Sales.to_json(stocks)#把结果转化为json
        for stock in stocks:
            batchs.append(stock.batch)
        for i in range(0, len(stocks), 1):
            inventorys[batchs[i]] = data[i]
    return jsonify(inventorys)





