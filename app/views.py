from app import app
import re
from flask import request, session
from flask import render_template, redirect, url_for
import mysql.connector
from mysql.connector import FieldType
from collections import defaultdict
from datetime import datetime
from flask_hashing import Hashing
import connect
import os


hashing = Hashing(app)  #create an instance of hashing
app.secret_key = 'hello'

dbconn = None
connection = None


def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn



@app.route('/')
@app.route('/home')
def homepage():
    #check if user is loggedin
    if 'loggedin' in session:
        #user is loggedin, go the home page
        return render_template('index.html', username=session['username'])
    
    return render_template('accounts/login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    #output message if something goes wrong
    msg = ''
    #check if username and password POST requests exists
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #create variables for access
        username = request.form['username']
        user_psw = request.form['password']
        #check id account exists 
        cursor = getCursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        #fetch record and return result 
        account = cursor.fetchone()
        if account is not None:
            password = account[2]
            if hashing.check_value(password, user_psw, salt='abcd'):
            #if account exists in accounts table, create session data, 
                session['loggedin'] = True
                session['user_id'] = account[0]
                session['username'] = account[1]
                session['role'] = account[9]
                #redirect to home page
                return redirect(url_for('homepage'))
            else:
                #password incorrect
                msg = 'Incorrect Password. Please try again!'
        else:
            
            #account doesnot exist or username incorrect
            msg = 'Username is not valid. Please check your username!'
    else:
        if "user_id" in session:
            return redirect(url_for('homepage'))
        
    return render_template('accounts/login.html', msg=msg)
              
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    #print the error message
    msg = ''
    #check if username, password and email exist
    if request.method == "POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'first_name' in request.form and 'last_name' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        #check if account exists 
        cursor = getCursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        #account validation
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password):
            msg = 'Password should be at least 8 characters long and have a mix of character types!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            #account doesn't exist and all information is valid 
            hashed = hashing.hash_value(password, salt='abcd')
            cursor.execute("INSERT INTO users (username, password, email, first_name, last_name, status, role, date_joined) VALUES (%s, %s, %s, %s, %s, 'Active', 'mariners', %s )", (username, hashed, email, first_name, last_name, current_date))
            
            connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        #form is empty
        msg = 'Please complete the form!'        
    return render_template('accounts/register.html', msg=msg)

#logout page
@app.route('/logout')
def logout():
    #remove session data
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    #redict to login page
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'role' in session:
        if session['role'] == 'mariners':
            return redirect(url_for('mariners_dashboard'))
        elif session['role'] == 'staff':
            return redirect(url_for('staff_dashboard'))
        elif session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
    
    else:
        return redirect(url_for('login')) 
    
@app.route('/settings')
def settings():
    if 'role' in session:
        if session['role'] == 'mariners':
            return redirect(url_for('mariners_settings'))
        elif session['role'] == 'staff':
            return redirect(url_for('staff_settings'))
        elif session['role'] == 'admin':
            return redirect(url_for('admin_settings'))
    
    else:
        return redirect(url_for('login')) 
    
@app.route('/profile')
def profile():
    if 'role' in session:
        if session['role'] == 'mariners':
            return redirect(url_for('mariners_profile'))
        elif session['role'] == 'staff':
            return redirect(url_for('staff_profile'))
        elif session['role'] == 'admin':
            return redirect(url_for('admin_profile'))
            
    
    else:
        return redirect(url_for('login')) 
    

@app.route('/mariners')
def mariners():
    if 'role' in session:
        if session['role'] == 'mariners':
            return redirect(url_for('mariners_profile'))
        elif session['role'] == 'staff':
            return redirect(url_for('staff_profile'))
        elif session['role'] == 'admin':
            return redirect(url_for('admin_profile'))              
    else:
        return redirect(url_for('login')) 

@app.route('/staff')
def staff():
    if 'role' in session:
        if session['role'] == 'mariners':
            return redirect(url_for('mariners_profile'))
        elif session['role'] == 'staff':
            return redirect(url_for('staff_profile'))
        elif session['role'] == 'admin':
            return redirect(url_for('admin_profile'))              
    else:
        return redirect(url_for('login')) 
    
@app.route('/admin')
def admin():
    if 'role' in session:
        if session['role'] == 'mariners':
            return redirect(url_for('mariners_profile'))
        elif session['role'] == 'staff':
            return redirect(url_for('staff_profile'))
        elif session['role'] == 'admin':
            return redirect(url_for('admin_profile'))              
    else:
        return redirect(url_for('login')) 


@app.route('/oceanpests')
def pests():
    return render_template('pests.html')

@app.route('/oceandiseases')
def diseases():
    return render_template('diseases.html')

@app.route('/sources')
def sources():
    return render_template('sources.html')






