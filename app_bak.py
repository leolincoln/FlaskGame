from flask import Flask, render_template,redirect,url_for,request,session,flash
from functools import wraps
from flask.ext.socketio import SocketIO,emit
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app,socketio,db

class Message(db.Model):
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
    username = db.Column(db.String(80))
    password = db.Column(sb.String(80))
    def __init__(self,username,password):
        this.username = username
        this.password = password
    def __repr__(self):
        return '<User %r>' % self.username

class Bank(db.Model):
    username = db.Column(db.String(80))
    money = db.Column(db.Float)
    def __init__(self,username,money):
        this.username = username
        this.money = money
    def __repr__(self):
        return '<User %r Bank %r>' %(self.username,self.money)

class Trans(db.Model):
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

#login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('you need to login first.')
            print 'redirecting to login'
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def home():
    return "hello, World!"

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/colors')
@login_required
def colors():
    return render_template('colors.html')

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/login',methods=['GET','POST'])
def login():
    
    error = None
    if request.method == 'POST':
        if request.form['username']!='admin' or request.form['password']!='admin':
            error = 'Invalid credentials'
        else:
            session['logged_in']=True
            session['username']=request.form['username']
            session['password']=request.form['password']
            session['role']=request.form['role']
            flash('you were just logged in!')
            if session['role']!='judge':
                return redirect(url_for('colors'))
            else:
                return redirect(url_for('chat'))
            #return render_template('colors.html',session=session )
    return render_template('login.html',error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    session.pop('username',None) 
    session.pop('password',None)
    flash('you were just logged out!')
    return redirect(url_for('login'))
def ack():
    print 'message was received'


@socketio.on('connect')
def test_connect():
    emit('new_message', {'data': 'Connected', 'count': 0})
    print 'connected'

@socketio.on('usr_message')
def handle_my_event(msg):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('new_message',{'data':msg['data'],'count':session['receive_count']},callback=ack,broadcast=True)

