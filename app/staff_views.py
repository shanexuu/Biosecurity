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
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn


@app.route("/staff/dashboard")
def staff_dashboard():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'staff':

      #Get the user's current id where stored in the session
      user_id = session['user_id']
      cursor.execute("SELECT * FROM users  WHERE user_id = %s", (user_id,))
      
      user = cursor.fetchone()
   
      return render_template('dashboard-staff.html', user=user)
    else:
      return redirect(url_for('login'))
    


@app.route("/staff/profile")
def staff_profile():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'staff':

      #Get the user's current id where stored in the session
      user_id = session['user_id']
      cursor.execute("SELECT * FROM users  WHERE user_id = %s", (user_id,))
      
      user = cursor.fetchone()
   
      return render_template('profile-staff.html', user=user)
    else:
      return redirect(url_for('login'))
   

@app.route("/staff/settings", methods=["GET", "POST"])
def staff_settings():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'staff':
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

            
            return render_template('settings-staff.html', user=user, msg=msg)
        
       
        return render_template('settings-staff.html', user=user, msg=msg)
    else:
        return redirect(url_for('login'))

@app.route("/staff/view-mariners")
def staff_view_mariners():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'staff':

      
      cursor.execute("SELECT * FROM users  WHERE role = 'mariners'")
      
      users = cursor.fetchall()
      print(users)
   
      return render_template('view-mariners-staff.html', users=users)
    else:
      return redirect(url_for('login'))
  

@app.route("/staff/view-guide")
def staff_view_guide():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'staff':     
      cursor.execute("SELECT * FROM ocean")     
      guides = cursor.fetchall()
      return render_template('view-guide-staff.html', guides=guides)
    else:
      return redirect(url_for('login'))
  
  

@app.route("/staff/add-guide", methods = ["GET", "POST"])
def staff_add_guide():
    
    try:
     if 'user_id' in session and 'role' in session and session['role'] == 'staff':
      msg = ''
      #check if ocean type, present in nz, common name and scientific name exist
      if request.method == "POST" and 'ocean_type' in request.form and 'present_in_nz' in request.form and 'common_name' in request.form and 'scientific_name' in request.form:
      
        ocean_type = request.form['ocean_type']
        present_in_nz = request.form['present_in_nz']
        common_name = request.form['common_name']
        scientific_name = request.form['scientific_name']
        characteristics = request.form['characteristics']
        description = request.form['description']
        threats = request.form['threats']
        location = request.form['location']

        cursor = getCursor()

        cursor.execute('INSERT INTO ocean (ocean_type, present_in_nz, common_name, scientific_name, characteristics, description, threats, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (ocean_type, present_in_nz, common_name, scientific_name, characteristics, description, threats, location,))

        connection.commit()
        msg = "You've successfully added one guide!"
      elif request.method == 'POST':
        #form is empty
        msg = 'Please complete the form!' 


      return render_template('add-guide-staff.html', msg=msg)


    except Exception as e:
     error_message = f"An error occurred: {str(e)}"
     return render_template("error.html", error_message=error_message)



@app.route("/staff/update-guide")
def staff_update_guide():
    return render_template('update-guide-staff.html')


@app.route("/staff/delete-guide")
def staff_delete_guide():
    return render_template('delete-guide-staff.html')