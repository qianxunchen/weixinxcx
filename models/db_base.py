# from models.base import *
from models import db
from sqlalchemy.orm import relationship

#商品库存表
class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    user = relationship('User')  # 关联User
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    batch = db.Column(db.Integer,unique=True)#批次
    nameID = db.Column(db.String(50))#商品编号
    name = db.Column(db.String(50))#商品名
    brand = db.Column(db.String(50))#品牌
    size = db.Column(db.String(100))#大小
    color = db.Column(db.String(10))#颜色
    PurchasingPrice = db.Column(db.Float)#进价
    SellingPrice = db.Column(db.Float)#售价
    Number = db.Column(db.Integer)#库存数量
    NumberPrice = db.Column(db.Float)#库存总金额
    Time = db.Column(db.String(10))#操作时间

# db.create_all()# 要先创建表，不然会提示找不到表

    #进货(第一次)
    @staticmethod
    def stockfirst(uid,batch,nameID, name, brand, size, color, PurchasingPrice,SellingPrice,Number,NumberPrice,time):
        inventory = Inventory()
        inventory.uid = uid
        inventory.batch = batch
        inventory.nameID = nameID
        inventory.name = name
        inventory.brand = brand
        inventory.size = size
        inventory.color = color
        inventory.PurchasingPrice = PurchasingPrice
        inventory.SellingPrice = SellingPrice
        inventory.Number = Number
        inventory.NumberPrice = NumberPrice
        inventory.Time = time
        db.session.add(inventory)
        db.session.commit()

    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self,key) is not None:
                result[key] = str(getattr(self,key))
            else:
                result[key] = getattr(self, key)
        return result

    def to_json(all_vendors):
        v = [ven.dobule_to_dict() for ven in all_vendors]
        return v

# 销售表
class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    user = relationship('User')  # 关联User
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    SerialNumber = db.Column(db.Integer,unique=True)#销售单号
    nameID = db.Column(db.String(50))#商品编号
    name = db.Column(db.String(50))#商品名
    brand = db.Column(db.String(50))#品牌
    size = db.Column(db.String(100))#大小
    color = db.Column(db.String(10))#颜色
    SellingPrice = db.Column(db.Float)#售价
    Number = db.Column(db.Integer)#销售数量
    NumberPrice = db.Column(db.Float)#本次销售金额
    Time = db.Column(db.String(10))#操作时间

    #销售
    @staticmethod
    def sales(uid,SerialNumber,nameID, name, brand, size, color,SellingPrice,Number,NumberPrice,time):
        sale = Sales()
        sale.uid = uid
        sale.SerialNumber = SerialNumber
        sale.nameID = nameID
        sale.name = name
        sale.brand = brand
        sale.size = size
        sale.color = color
        sale.SellingPrice = SellingPrice
        sale.Number = Number
        sale.NumberPrice = NumberPrice
        sale.Time = time
        db.session.add(sale)
        db.session.commit()

    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self,key) is not None:
                result[key] = str(getattr(self,key))
            else:
                result[key] = getattr(self, key)
        return result

    def to_json(all_vendors):
        v = [ven.dobule_to_dict() for ven in all_vendors]
        return v

# 退货表
class SalesReturn(db.Model):
    __tablename__ = 'SalesReturn'
    id = db.Column(db.Integer, primary_key=True)
    user = relationship('User')  # 关联User
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    SerialNumber = db.Column(db.Integer,unique=True)#销售单号
    nameID = db.Column(db.String(50))#商品编号
    name = db.Column(db.String(50))#商品名
    brand = db.Column(db.String(50))#品牌
    size = db.Column(db.String(100))#大小
    color = db.Column(db.String(10))#颜色
    SellingPrice = db.Column(db.Float)#售价
    Number = db.Column(db.Integer)#退货数量
    NumberPrice = db.Column(db.Float)#本次退货金额
    Time = db.Column(db.String(10))#操作时间

    #退货
    @staticmethod
    def saleReturn(uid,SerialNumber,nameID, name, brand, size, color,SellingPrice,Number,NumberPrice,time):
        sale = Sales()
        sale.uid = uid
        sale.SerialNumber = SerialNumber
        sale.nameID = nameID
        sale.name = name
        sale.brand = brand
        sale.size = size
        sale.color = color
        sale.SellingPrice = SellingPrice
        sale.Number = Number
        sale.NumberPrice = NumberPrice
        sale.Time = time
        db.session.add(sale)
        db.session.commit()

    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self,key) is not None:
                result[key] = str(getattr(self,key))
            else:
                result[key] = getattr(self, key)
        return result

    def to_json(all_vendors):
        v = [ven.dobule_to_dict() for ven in all_vendors]
        return v


# 用户表
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))#
    location = db.Column(db.String(50))  #
    email = db.Column(db.String(24))
    password = db.Column(db.String(50))#

    @staticmethod
    def register_test(name,email,password,location):
        user = User()
        user.name = name
        user.password = password
        user.email = email
        user.location = location
        db.session.add(user)
        db.session.commit()