from app import app
import re
from werkzeug.utils import secure_filename
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

UPLOAD_FOLDER = 'app/static/assets/img'


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

@app.route("/admin/dashboard")
def admin_dashboard():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':

      #Get the user's current id where stored in the session
      user_id = session['user_id']
      cursor.execute("SELECT * FROM users  WHERE user_id = %s", (user_id,))
      
      user = cursor.fetchone()
   
      return render_template('dashboard-admin.html', user=user)
    else:
      return redirect(url_for('login'))


@app.route("/admin/profile")
def admin_profile():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':

      #Get the user's current id where stored in the session
      user_id = session['user_id']
      cursor.execute("SELECT * FROM users  WHERE user_id = %s", (user_id,))
      
      user = cursor.fetchone()
   
      return render_template('profile-admin.html', user=user)
    else:
      return redirect(url_for('login'))


@app.route("/admin/settings", methods=["GET", "POST"])
def admin_settings():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
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

            
            return render_template('settings-admin.html', user=user, msg=msg)
        
       
        return render_template('settings-admin.html', user=user, msg=msg)
    else:
        return redirect(url_for('login'))

@app.route("/admin/view-mariners")
def admin_view_mariners():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':

      
      cursor.execute("SELECT * FROM users  WHERE role = 'mariners'")
      
      users = cursor.fetchall()
      print(users)
   
      return render_template('view-mariners-admin.html', users=users)
    else:
      return redirect(url_for('login'))
 

@app.route("/admin/view-guide")
def admin_view_guide():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
      
      cursor.execute("""
            SELECT o.*, ol.image_url
            FROM ocean o
            INNER JOIN oceanImages ol on ol.ocean_id = o.ocean_id;
        """)
      guides = cursor.fetchall()
     
      
      return render_template('view-guide-admin.html', guides= guides)
    else:
      return redirect(url_for('login'))


@app.route("/admin/add-guide", methods = ["GET", "POST"])
def admin_add_guide():
    
    # try:
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
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

        # Insert guide information into the ocean table
        cursor.execute('INSERT INTO ocean (ocean_type, present_in_nz, common_name, scientific_name, characteristics, description, threats, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',(ocean_type, present_in_nz, common_name, scientific_name, characteristics, description, threats, location))
        ocean_id = cursor.lastrowid

        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Insert image information into the oceanImages table
                cursor.execute('INSERT INTO oceanImages (ocean_id, image_url) VALUES (%s, %s)',(ocean_id, filepath))

                connection.commit()
                msg = "You've successfully added one guide and uploaded images!"     

      elif request.method == 'POST':
        #form is empty
        msg = 'Please complete the form!' 
      return render_template('add-guide-admin.html', msg=msg)
    else:
        return redirect(url_for('login'))

    # except Exception as e:
    #  error_message = f"An error occurred: {str(e)}"
    #  return render_template("error.html", error_message=error_message)


@app.route("/admin/update-guide", methods=["GET", "POST"])
def admin_update_guide():

    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
      
       msg = ''
       names=[]

       cursor = getCursor()
       cursor.execute("SELECT ocean_id FROM ocean")
       names = cursor.fetchall()
       print(names[0])
      
       if request.method == "POST":
      
         ocean_type = request.form['ocean_type']
         present_in_nz = request.form['present_in_nz']
         common_name = request.form['common_name']
         scientific_name = request.form['scientific_name']
         characteristics = request.form['characteristics']
         description = request.form['description']
         threats = request.form['threats']
         location = request.form['location']
    
         try:
            
            user_id = session['user_id']
            cursor.execute("""
            UPDATE ocean
            SET ocean_type = %s, present_in_nz = %s, common_name = %s, scientific_name = %s, characteristics = %s, description = %s, threats  = %s, location = %s
            WHERE user_id = %s""", (ocean_type, present_in_nz, common_name, scientific_name, characteristics, description, threats, location, user_id))

            connection.commit()
            msg = 'You have successfully updated the guide'
         except mysql.connector.Error:
            connection.rollback()
            msg = 'Failed to update the guide.'
         finally:
            cursor.close()
            connection.close()


       return render_template('update-guide-admin.html', msg=msg, guides=names)
    

    else:
      return redirect(url_for('login'))


@app.route("/admin/delete-guide")
def admin_delete_guide():
    return render_template('delete-guide-admin.html')

@app.route("/admin/view-staff")
def admin_view_staff():
    return render_template('view-staff.html')

@app.route("/admin/add-staff")
def admin_add_staff():
    return render_template('add-staff.html')

@app.route("/admin/update-staff")
def admin_update_staff():
    return render_template('update-staff.html')

@app.route("/admin/delete-staff")
def admin_delete_staff():
    return render_template('delete-staff.html')