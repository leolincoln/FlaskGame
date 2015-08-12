from app import db
from datetime import datetime
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fromRole = db.Column(db.String(80))
    message = db.Column(db.String(200))
    toRole = db.Column(db.String(10))
    time = db.Column(db.DateTime)
    def __init__(self,fromRole,message,toRole,time=None):
        if time is None:
            time=datetime.utcnow()
        self.fromRole = fromRole
        self.message = message
        self.toRole = toRole
        self.time = time
    def __repr__(self):
        return '<Message %r, from %r, to %r>' % (self.message,self.fromRole,self.toRole)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.username

class Bank(db.Model):
    startMoney = 200
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),primary_key=True)
    role = db.Column(db.String(80),primary_key=True)
    money = db.Column(db.Float)
    def __init__(self,role,money=None,username=None):
        if username is None:
            username = admin
        self.username = username
        self.role = role
        if money is None:
            money = self.startMoney
        self.money = money
    def __repr__(self):
        return '<role %r User %r Bank %r>' %(self.role,self.username,self.money)

class Trans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    fromRole = db.Column(db.String(80))
    toRole = db.Column(db.String(80))
    amount = db.Column(db.Float)
    def __init__(self,fromRole,toRole,amount,time=None):
        if time is None:
            time=datetime.utcnow()
        self.time = time
        self.fromRole = fromRole
        self.toRole = toRole
        self.amount = amount
    def __repr__(self):
        return '<$%r from %r to %r >'%(self.amount,self.fromRole,self.toRole)
