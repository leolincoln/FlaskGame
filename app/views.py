from flask import Flask, render_template,redirect,url_for,request,session,flash
from functools import wraps
from flask.ext.socketio import SocketIO,emit
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app, socketio
#app = Flask(__name__)

#app.config.from_object('config')
#db = SQLAlchemy(app)
#socketio = SocketIO(app)

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
    return render_template('login.html')

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
                f = open('app/results.csv','r')
                lines = f.read()
                print lines
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
    from app import db,models
    try:
        tempM = models.Message(session['username'],msg['data'],session['role'])
    except KeyError:
        return redirect(url_for('login'))
    db.session.add(tempM)
    db.session.commit()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('new_message',{'data':msg['data'],'count':session['receive_count'],'role':session['role'],'time':str(datetime.now())[10:19]},callback=ack,broadcast=True)


if __name__=='__main__':
    #app.run(debug=True)i
    socketio.run(app,host='0.0.0.0')
