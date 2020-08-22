from flask import Blueprint, request, g
import time
import datetime
from models.db_base import *
from models.apireturn import *
from libs.auth_token import auth
from models import db
from sqlalchemy import and_, func

salesapi = Blueprint('salesapi', __name__)


# 销售统计页
@salesapi.route('/sale')
@auth.login_required
def sale():
    uid = g.user.id
    # data = request.args.get('date')
    # date2 = request.args.get('date2')
    date = "2000-01-01"
    date2 = "2020-06-01"
    sales = db.session.query(func.sum(Sales.NumberPrice)).filter(Sales.uid==uid,Sales.Time.between(date, date2)).scalar()
    print(sales)
    sa = db.session.query(func.count(Inventory.NumberPrice)).filter(Inventory.uid == uid,Inventory.Time.between(date, date2)).scalar()
    print(sa)
    if sales and sa:
        data={
            "sale":sales,
            "salenumber":sa
        }
        return jsonify(data)
    else:
        data={
            "sale":0,
            "salenumber":0
        }
        return jsonify(data),1002


# # 销售明细页(我自己想的逻辑
@salesapi.route('/saledetail')
@auth.login_required
def saledetail():
    # uid = g.user.id
    uid = 5
    # data = request.args.get('date')
    # date2 = request.args.get('date2')
    date = "2000-01-01"
    date2 = "2020-06-01"
    Sale = {}
    SerialNumbers = []
    sales = Sales.query.filter(Sales.uid==uid,Sales.Time.between(date, date2)).all()
    if(len(sales)==0):
        data = {
            "msg": "还没有卖出商品，努力吧！",
        }
        return jsonify(data),1002
    else:
        data = Sales.to_json(sales)
        for sale in sales:
            SerialNumbers.append(sale.SerialNumber)
        for i in range(0,len(sales),1):
            Sale[SerialNumbers[i]] = data[i]
        return jsonify(Sale)

# 销售
@salesapi.route('/sales',methods=['POST'])
@auth.login_required
def sales():
    uid = g.user.id
    # SerialNumber = int(request.args.get('SerialNumber'))
    # nameID = int(request.args.get('nameID'))
    # name = request.args.get('name')
    # brand = request.args.get('brand')
    # size = request.args.get('size')
    # color = request.args.get('color')
    # SellingPrice = float(request.args.get('SellingPrice'))
    # sale_Number = int(request.args.get('Number'))
    data = request.get_json('SerialNumber')
    SerialNumber = int(data['SerialNumber'])
    nameID = int(data['nameID'])
    name = data['name']
    brand = data['brand']
    size = data['size']
    color = data['color']
    SellingPrice = float(data['SellingPrice'])
    sale_Number = int(data['Number'])
    Time = time.strftime('%Y-%m-%d')
    stock = Inventory.query.filter_by(uid=uid).first()
    stock_number = stock.Number
    old_NumberPrice = stock.NumberPrice
    if(stock_number < sale_Number):
        data = {
            "error": "库存不足"
        }
        return jsonify(data)
    else:
        NumberPrice = float(sale_Number * SellingPrice)
        new_number = stock_number - sale_Number
        new_NumberPrice = old_NumberPrice - NumberPrice
        Sales.sales(uid,SerialNumber, nameID, name, brand, size, color, SellingPrice, sale_Number, NumberPrice, Time)
        Inventory.query.filter_by(uid=uid,nameID=nameID).update({'Number':new_number , 'NumberPrice':new_NumberPrice, 'Time': Time})
        db.session.commit()
        return Success()

# 今日销售
@salesapi.route('/SaleToday',methods=['POST'])
@auth.login_required
def saletoday():
    uid = g.user.id
    sale_price = 0
    Time = time.strftime('%Y-%m-%d')
    sales = Sales.query.filter_by(uid=uid,Time=Time).all()
    if(len(sales)==0):
        data = {
            "sale_price": sale_price
        }
        return jsonify(data)
    else:
        for sale in sales:
            sale_price += sale.NumberPrice
        data = {
            "sale_price":sale_price
        }
        return jsonify(data)

# 昨日销售
@salesapi.route('/SaleYesterday',methods=['POST'])
@auth.login_required
def saleyesterday():
    uid = g.user.id
    sale_price = 0
    Time = str(datetime.date.today() + datetime.timedelta(-1))
    sales = Sales.query.filter_by(uid=uid,Time=Time).all()
    if(len(sales)==0):
        data = {
            "sale_price": sale_price
        }
        return jsonify(data)
    else:
        for sale in sales:
            sale_price += sale.NumberPrice
        data = {
            "sale_price":sale_price
        }
        return jsonify(data)


# 本月销售
@salesapi.route('/SaleMonth',methods=['POST'])
@auth.login_required
def salemonth():
    uid = g.user.id
    sale_price = 0
    Time = time.strftime('%Y-%m')
    Time = Time + '%'
    sales = Sales.query.filter(and_(Sales.uid==uid, Sales.Time.like(Time))).all()
    if (len(sales) == 0):
        data = {
            "sale_price": sale_price
        }
        return jsonify(data)
    else:
        for sale in sales:
            sale_price += sale.NumberPrice
        data = {
            "sale_price": sale_price
        }
        return jsonify(data)


# 退货
@salesapi.route('/salesreturn',methods=['POST'])
@auth.login_required
def salesreturn():
    uid = g.user.id
    # SerialNumber = int(request.args.get('SerialNumber'))  # 退货单号
    # nameID = int(request.args.get('nameID'))
    # name = request.args.get('name')
    # brand = request.args.get('brand')
    # size = request.args.get('size')
    # color = request.args.get('color')
    # SellingPrice = float(request.args.get('SellingPrice'))
    # sale_Number = int('Number')  # 退货数量
    data = request.get_json('SerialNumber')
    SerialNumber = int(data['SerialNumber'])#退货单号
    nameID = int(data['nameID'])
    name = data['name']
    brand = data['brand']
    size = data['size']
    color = data['color']
    SellingPrice = float(data['SellingPrice'])
    sale_Number = int(data['Number'])#退货数量
    Time = time.strftime('%Y-%m-%d')
    stock = Sales.query.filter_by(uid=uid,SerialNumber=SerialNumber).first()#销售表
    inven = Inventory.query.filter_by(uid=uid, nameID=nameID).first()  # 库存表
    Number = stock.Number-sale_Number# 退货后的销售单剩余数量
    if(Number < 0):
        data = {
            "error": "退货数大于销售数量"
        }
        return jsonify(data)
    else:
        NumberPrice = float(Number * sale.SellingPrice)#销售单剩余金额
        Sales.query.filter_by(uid=uid, SerialNumber=SerialNumber).update({'Number': Number, 'NumberPrice': NumberPrice, 'Time': Time})#更新销售单
        Inventory.query.filter_by(uid=uid, nameID=nameID).update({'Number':inven.Number+sale_Number , 'NumberPrice':inven.NumberPrice+sale_Number*SellingPrice, 'Time': Time})#更新库存
        SalesReturn.saleReturn(uid,SerialNumber, nameID, name, brand, size, color, SellingPrice, sale_Number, sale_Number*SellingPrice, Time)
        db.session.commit()
        return Success()
