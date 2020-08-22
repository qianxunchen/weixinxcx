from flask import Blueprint, request,g
import time
from models.db_base import *
from models.apireturn import *
from libs.auth_token import auth
from sqlalchemy import or_,and_

purapi = Blueprint('purapi', __name__)

'''采购页、首页'''


# 采购页面
@purapi.route('/inventory')
@auth.login_required
def inventorytime():
    uid = g.user.id
    # print(uid)
    # data = request.args.get('date')
    # date2 = request.args.get('date2')
    date = "2000-01-01"
    date2 = "2020-06-01"
    inventorys = {}
    batchs = []
    stocks = Inventory.query.filter(and_(Inventory.uid==uid,Inventory.Time.between(date, date2))).all()
    if(len(stocks)==0):
        data = {
            "msg": "没有库存，快去进货吧！",
        }
        return jsonify(data),1002
    else:
        data = Sales.to_json(stocks)#把结果转化为json
        for stock in stocks:
            batchs.append(stock.batch)
        for i in range(0, len(stocks), 1):
            inventorys[batchs[i]] = data[i]
    return jsonify(inventorys)

# 采购页面(按单据/货品名查找)
@purapi.route('/inventoryname')
@auth.login_required
def inventory():
    uid = g.user.id
    # name = request.args.get('name')
    # nameID = request.args.get('nameID')
    name = ' '
    nameID = '1003'
    inventorys = {}
    batchs = []
    stocks = Inventory.query.filter(and_(Inventory.uid==uid, or_(Inventory.nameID==nameID, Inventory.name==name))).all()
    if(len(stocks)==0):
        data = {
            "msg": "没有查到",
        }
        return jsonify(data),1002
    else:
        data = Sales.to_json(stocks)
        for stock in stocks:
            batchs.append(stock.batch)
        for i in range(0, len(stocks), 1):
            inventorys[batchs[i]] = data[i]
    return jsonify(inventorys)

# 进货(第一次)
@purapi.route('/stock',methods=['POST'])
@auth.login_required
def stock():
    uid = g.user.id
    # batch = int(request.args.get('batch'))
    # nameID = int(request.args.get('nameID'))
    # name = request.args.get('name')
    # brand = request.args.get('brand')]
    # size = request.args.get('size')
    # color = request.args.get('color')
    # PurchasingPrice = float(request.args.get('PurchasingPrice'))
    # SellingPrice = request.args.get('SellingPrice')
    # Number = int(request.args.get('Number'))
    data = request.get_json('batch')
    batch = int(data['batch'])
    nameID = int(data['nameID'])
    name = data['name']
    brand = data['brand']
    size = data['size']
    color = data['color']
    PurchasingPrice = float(data['PurchasingPrice'])
    SellingPrice = data['SellingPrice']
    Number = int(data['Number'])
    Time = time.strftime('%Y-%m-%d')
    NumberPrice = float(Number * PurchasingPrice)
    Inventory.stockfirst(uid,batch, nameID, name, brand, size, color, PurchasingPrice, SellingPrice, Number, NumberPrice, Time)
    return jsonify(data)


# # 进货(补货)
# @purapi.route('/stocktwo', methods=['POST'])
# @auth.login_required
# def stocktwo():
#     uid = g.user.id
#     data = request.get_json('nameID')
#     PurchasingPrice = float(data['PurchasingPrice'])
#     Number = int(data['Number'])
#     Time = time.strftime('%Y%m%d')
#     stock = Inventory.query.filter_by(uid=uid).first()
#     old_NumberPrice = stock.NumberPrice
#     old_Number = stock.Number
#     new_Number = old_Number + Number
#     add_NumberPrice = float(Number * PurchasingPrice)
#     new_NumberPrice = float(add_NumberPrice + old_NumberPrice)
#     Inventory.query.filter_by(uid=uid).update({'Number':new_Number,'NumberPrice': new_NumberPrice, 'Time': Time})
#     db.session.commit()
#     return Success()

# 盘点(总盈利页)
@purapi.route('/check')
@auth.login_required
def check():
    uid = g.user.id
    sale_price = 0
    expenditure_price = 0
    expenditures = Inventory.query.filter(uid==uid).all()
    sales = Sales.query.filter(uid==uid).all()
    if(len(sales)==0 and len(expenditures)==0):
        data = {
            "sale_price": sale_price,
            "expenditure_price": expenditure_price,
            "Profit": 0
        }
        return jsonify(data)
    else:
        for expenditure in expenditures:
            expenditure_price += expenditure.NumberPrice
        for sale in sales:
            sale_price += sale.NumberPrice
        Profit = sale_price - expenditure_price
        data = {
            "sale_price":sale_price,
            "expenditure_price":expenditure_price,
            "Profit":Profit
        }
        return jsonify(data)


# 今日盈利
@purapi.route('/CheckToday')
@auth.login_required
def checktoday():
    uid = g.user.id
    sale_price = 0
    expenditure_price = 0
    Time = time.strftime('%Y-%m-%d')
    expenditures = Inventory.query.filter_by(uid=uid,Time=Time).all()
    sales = Sales.query.filter_by(uid=uid,Time=Time).all()
    if(len(sales)==0 and len(expenditures)==0):
        data = {
            "sale_price": sale_price,
            "expenditure_price": expenditure_price,
            "Profit": 0
        }
        return jsonify(data)
    else:
        for expenditure in expenditures:
            expenditure_price += expenditure.NumberPrice
        for sale in sales:
            sale_price += sale.NumberPrice
        Profit = sale_price - expenditure_price
        data = {
            "sale_price":sale_price,
            "expenditure_price":expenditure_price,
            "Profit": Profit
        }
        return jsonify(data)

