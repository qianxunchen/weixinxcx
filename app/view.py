from flask import Blueprint, g
import time
import datetime
from models.db_base import *
from models.apireturn import *
from libs.auth_token import auth
from sqlalchemy import and_

api = Blueprint('api', __name__)

'''采购页、首页'''


# 首页
@api.route('/')
@auth.login_required
def index():
    uid = g.user.id
    data = []
    deta = ['Today','Yesterday','Month']
    allsale = {}
    saleToday = 0
    saleYesterday = 0
    saleMonth = 0
    TimeToday = time.strftime('%Y-%m-%d')
    sales = Sales.query.filter_by(uid=uid, Time=TimeToday).all()
    if (len(sales) == 0):
        data.append(saleToday)
    else:
        for sale in sales:
            saleToday += sale.NumberPrice
        data.append(saleToday)
    #昨日
    TimeYesterday = str(datetime.date.today() + datetime.timedelta(-1))
    sales = Sales.query.filter_by(uid=uid, Time=TimeYesterday).all()
    if (len(sales) == 0):
        data.append(saleYesterday)
    else:
        for sale in sales:
            saleYesterday += sale.NumberPrice
        data.append(saleYesterday)
    #本月
    TimeMonth = time.strftime('%Y-%m')
    TimeMonth = TimeMonth + '%'
    sales = Sales.query.filter(and_(Sales.uid==uid, Sales.Time.like(TimeMonth))).all()
    if (len(sales) == 0):
        data.append(saleMonth)
    else:
        for sale in sales:
            saleMonth += sale.NumberPrice
        data.append(saleMonth)
    print(data)
    d = dict(zip(deta, data))
    return jsonify(d)
