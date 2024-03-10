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


@app.route('/mariners/dashboard')
def mariners_dashboard():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'mariners':

      #Get the user's current id where stored in the session
      user_id = session['user_id']
      cursor.execute("SELECT * FROM users  WHERE user_id = %s", (user_id,))
      
      user = cursor.fetchone()
   
      return render_template('dashboard-mariners.html', user=user)
    else:
      return redirect(url_for('login'))


@app.route('/mariners/profile')
def mariners_profile():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'mariners':

      #Get the user's current id where stored in the session
      user_id = session['user_id']
      cursor.execute("SELECT * FROM users  WHERE user_id = %s", (user_id,))
      
      user = cursor.fetchone()
   
      return render_template('profile-mariners.html', user=user)
    else:
      return redirect(url_for('login'))

@app.route('/mariners/settings', methods=["GET", "POST"])
def mariners_settings():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'mariners':
        user_id = session['user_id']
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,)) 
        user = cursor.fetchone()

        msg = ''
        if request.method == "POST":
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            phone_number = request.form.get('phone_number')
            address = request.form.get('address')
            status = request.form.get('status')
            hashed = hashing.hash_value(password, salt='abcd')

            try:
                cursor.execute("""
                UPDATE users 
                SET first_name = %s, last_name = %s, email = %s, password = %s, phone_number = %s, address = %s, status = %s 
                WHERE user_id = %s
                """, (first_name, last_name, email, hashed, phone_number, address, status, user_id))

                connection.commit()
                msg = 'You have successfully updated your profile!'
            except mysql.connector.Error:
                connection.rollback()
                msg = 'Failed to update profile.'
            finally:
                cursor.close()
                connection.close()

            
            return render_template('settings-mariners.html', user=user, msg=msg)
        
       
        return render_template('settings-mariners.html', user=user, msg=msg)
    else:
        return redirect(url_for('login'))