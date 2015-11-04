from flask import Flask, render_template,redirect,url_for,request,session,flash
from functools import wraps
from flask.ext.socketio import SocketIO,emit
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app, socketio
import random
import json
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

#mimic the function in django on get_or_create. 
#input session, model and kwargs. 
def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        print 'found instance.', instance
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems())
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.commit()
        print 'did not found instance, created new object',instance
        return instance, True
#helps build a table
def table_builder(header=None,rows =None):
    '''

    :param header: list of strings matching column number
    :param rows:list of row. each row has its own list.
    :return:
    '''
    #start building a twitter bootstrap style table.
    result = ''
    result += '<table class="table table-striped">'
    if header is not None:
        result += '<thead>'
        result += '<tr>'
        for head in header:
            result+='<th>' + head + '</th>'
        result+='</tr>'
        result+='</thead>'
    result+='<tbody>'
    for row in rows:
        result +='<tr>'
        for item in row:
            result+= '<td>'+item+'</td>'
        result+='</tr>'
    result+='</tbody>'
    result+='</table>'
    return result


@app.route('/color_instruction')
@login_required
def color_instruction():
    '''
    Color_instruction page. Render html.
    :return:
    '''
    return render_template('color_instruction.html')
@app.route('/judge_instruction')
@login_required
def judge_instruction():
    '''

    :return:
    '''
    return render_template('judge_instruction.html')

@app.route('/message')
def message():
    from app import db,models
    messages = [message.toDict() for message in db.session.query(models.Message).all()]
    return json.dumps(messages)
   # return 'this is place holder for all messages'
@app.route('/trans')
def trans():

    from app import db,models
    messages = [message.toDict() for message in db.session.query(models.Trans).all()]
    return json.dumps(messages)

@app.route('/bank')
def bank():

    from app import db,models
    messages = [message.toDict() for message in db.session.query(models.Bank).all()]
    return json.dumps(messages)

#reset the money for all players
@app.route('/reset')
def reset_money():
    from app import db,models
    startMoney=200
    print '*'*80
    print 'in reset_money def, generating the initial banks. '
    for b in db.session.query(models.Bank).all():
        b.money = startMoney
        print 'process',b
    db.session.commit()
    print 'reset finished. '
    return redirect(url_for('bank'))    





@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/colors')
@login_required
def colors():
    return render_template('colors.html')
@app.route('/wait_judge')
@login_required
def wait_judge():
    return render_template('wait_judge.html')

@app.route('/chat')
@login_required
def chat():
    from app import db,models
    print '*'*80
    print 'in chat def, generating the initial banks. '
    userBank, status = get_or_create(db.session,models.Bank,role=session['role'],username=session['username'])
    if session['role']=='judge':
        with open('app/results.csv','r') as f:
            content = f.read()
        fakeResultList = get_rand_no_duplicate(content.split(',\r'),10)
        return render_template('chat.html',results = table_builder(['Color','p1_color','p2_color','p1_time','p2_time'],fakeResultList),money=userBank.money)
    else:
        return render_template('chat.html',money=userBank.money)
#this is for generating the false csv list of results. 
def get_rand_no_duplicate(sList,number=10,deli = None):
    '''
    read elements in sList
    :param sList: list of strings deliminated by deli specified.
    :param number:Integer How many no_duplicate random records
    :param deli:String The deliminator for string list slist
    :return:
    '''
    if deli is None:
        deli = ','
    print '*'*80
    print 'in get_rand_no_duplicate'
    print len(sList)
    resultList = []
    i=0
    while i<number:
        iTemp = random.randrange(0,len(sList))
        print iTemp
        if iTemp not in resultList:
            resultList.append(iTemp)
            i+=1
    #this reutrn assumes the deliminator is ','
    return [sList[i].split(deli) for i in resultList]

@login_required
@app.route('/wait_tester')
def wait_tester():
    return render_template('wait_tester.html')

@app.route('/login',methods=['GET','POST'])
def login():
    
    error = None
    if session.get('logged_in') == True:
        #if already logged in:
        if session['role'] == 'judge':
            return redirect(url_for('chat'))
        else:
            return redirect(url_for('colors'))
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
                return redirect(url_for('color_instruction'))
            else:
                return redirect(url_for('judge_instruction'))
    return render_template('login.html',error = error)

@app.route('/logout')
def logout():
    #reset money if judge log out. 
    session.pop('logged_in',None)
    session.pop('username',None) 
    session.pop('password',None)
    flash('you were just logged out!')
    return redirect(url_for('login'))
def ack():
    print 'message was received'


#There are only 4 types of messages 
#tester1 -> judge      t1
#tester2 -> judge      t2
#judge -> tester1      j1
#judge -> tester2      j2
#connect message. 
@socketio.on('connect_message')
def connected(msg):
    print 'in connnect_message'
    emit('connect_message',{'data':msg['data'],'fromRole':msg['fromRole'],'time':str(datetime.now())[10:19]},broadcast=True)
@socketio.on('disconnect_message')
def disconnected(msg):
    print 'in disconnnect_message'
    emit('disconnect_message',{'data':msg['data'],'fromRole':msg['fromRole'],'time':str(datetime.now())[10:19]},broadcast=True)

#usr_money is handled here
@socketio.on('money_message')
def transfer_money(msg):
    from app import db,models
    print 'msg in money_message',msg
    #with our initial money model judge, tester1, tester2 should all have intial money already. 
    #now what we need to think about is how to check if the user input money is higher than actually whatthey have. 

    #now if its on the judge side, then we will need ot update our money banks
    #and we will need to show the message as new message 
    
    fromRole = msg['fromRole']
    toRole = msg['toRole']
    money = float(msg['data'])
    print fromRole,'to',msg['toRole'],float(msg['data'])
    fromBank, status = get_or_create(db.session,models.Bank,role=fromRole,username=session['username'])
    toBank, status = get_or_create(db.session,models.Bank,role=toRole,username=session['username'])
    if fromBank.money<money:
        emit('err_message',{'money':'$'+msg['data']+ ' has not been sent to '+msg['toRole']+' :NOT ENOUGH MONEY IN BANK','fromRole':msg['fromRole'],'time':str(datetime.now())[10:19],'toRole':msg['toRole']},callback=ack,broadcast=True)
        return
    tempTrans = models.Trans(fromRole,toRole,money)
    db.session.add(tempTrans)
    #now logic: if the money doe not exceeds frombank, then do operation. Otherwise dont do anything.
    fromBank.money-=money
    toBank.money+=money
    db.session.commit()

    #then if you are the other people, we will need to update the money count 
    #and we will show the message as new message. 
    #gertting user's bank. 
    userBank, status = get_or_create(db.session,models.Bank,role=session['role'],username=session['username'])
    session['money'] = userBank.money
    emit('money_message',{'money':msg['data'],'fromRole':msg['fromRole'],'time':str(datetime.now())[10:19],'toRole':msg['toRole']},callback=ack,broadcast=True)

@socketio.on('winner_message')
@login_required
def winner(msg):
    #if a winner is declared, return each player and judge to result page. 
    emit('new_message',{'data':'Winner is:'+msg['toRole'],'role':session['role'],'time':str(datetime.now())[10:19],'toRole':msg['toRole']},callback=ack,broadcast=True)

@app.route('/result')
@login_required
def result():
    msg = request.args['messages']
    print 'in result', 'msg is:',msg
    return render_template('result.html')

#usr_message is handle here. 
@socketio.on('usr_message')
def send_message(msg):
    from app import db,models
    try:
        if session['role']!='judge':
            tempM = models.Message(session['role'],msg['data'],'judge')
        else:
            tempM = models.Message(session['role'],msg['data'],msg['toRole'])
    except KeyError:
        return redirect(url_for('login'))
    db.session.add(tempM)
    db.session.commit()
    emit('new_message',{'data':msg['data'],'role':session['role'],'time':str(datetime.now())[10:19],'toRole':msg['toRole']},callback=ack,broadcast=True)


if __name__=='__main__':
    #app.run(debug=True)i
    socketio.run(app,host='0.0.0.0')
