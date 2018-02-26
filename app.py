from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from tabledef2 import *
import stream
import datetime

engine1 = create_engine('sqlite:///socialmedia.db', echo=True)
postengine = create_engine('sqlite:///socialmediaposts.db', echo=True)

app = Flask(__name__)
POST_USERNAME = ''
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('homepage.html')
     
@app.route('/login', methods=['POST'])
def login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    
    Session = sessionmaker(bind=engine1)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


@app.route('/postprocess', methods=['POST'])
def homepage():
    title = str(request.form['titleofpost'])
    text = str(request.form['textofpost'])

    postengine = create_engine('sqlite:///socialmediaposts.db', echo=True)

    # create a Session
    Session = sessionmaker(bind=postengine)
    session = Session()


    post = Posts(title,text)
    session.add(post)
    session.commit()
    
    return home()

    
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route('/feed', methods=['POST', 'GET'])
def feed():
    Session1 = sessionmaker(bind=postengine)
    s1 = Session1()
    Session2 = sessionmaker(bind=engine1)
    s2 = Session2()
    postresult = s1.query(Posts)
    userresult = s2.query(User)
        
    return render_template('feed.html', postresult = postresult, userresult=userresult)



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
