from app import db
from datetime import datetime
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    message = db.Column(db.String(200))
    role = db.Column(db.String(10))
    time = db.Column(db.DateTime)
    def __init__(self,username,message,role,time=None):
        if time is None:
            time=datetime.utcnow()
        self.username = username
        self.message = message
        self.role = role
        self.time = time
    def __repr__(self):
        return '<Message %r>' % self.message

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    def __init__(self,username,password):
        this.username = username
        this.password = password
    def __repr__(self):
        return '<User %r>' % self.username

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    money = db.Column(db.Float)
    def __init__(self,username,money):
        this.username = username
        this.money = money
    def __repr__(self):
        return '<User %r Bank %r>' %(self.username,self.money)

class Trans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    fromUser = db.Column(db.String(80))
    toUser = db.Column(db.String(80))
    amount = db.Column(db.Float)
    def __init__(self,time,fromUser,toUser,amount):
        this.time = time
        this.fromUser = fromUser
        this.toUser = toUser
        this.amount = amount
    def __repr__(self):
        return '<$%r from %r to %r >'%(this.amount,this.fromUser,this.toUser)
