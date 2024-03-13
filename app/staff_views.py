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

UPLOAD_FOLDER = 'app/static/assets/img'


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

      cursor.execute("SELECT * FROM staff WHERE user_id = %s", (user_id,))

      staff = cursor.fetchone()
   
      return render_template('dashboard-staff.html', user=user, staff=staff)
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

      cursor.execute("SELECT * FROM staff WHERE user_id = %s", (user_id,))

      staff = cursor.fetchone()
   
      return render_template('profile-staff.html', user=user, staff=staff)
    else:
      return redirect(url_for('login'))
   

@app.route("/staff/settings", methods=["GET", "POST"])
def staff_settings():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'staff':
        user_id = session['user_id']
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,)) 
        user = cursor.fetchone()

        #Fetch data from form
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
      
      cursor.execute("""
            SELECT o.*, ol.image_url
            FROM ocean o
            INNER JOIN oceanImages ol on ol.ocean_id = o.ocean_id;
        """)
      guides = cursor.fetchall()
     
      
      return render_template('view-guide-staff.html', guides= guides)
    else:
      return redirect(url_for('login'))
  
  

@app.route("/staff/add-guide", methods = ["GET", "POST"])
def staff_add_guide():
    
 
    if 'user_id' in session and 'role' in session and session['role'] == 'staff':
      msg = ''
      #check if ocean type, present in nz, common name and scientific name, scientific_name, characteristics, description,threats, location in the form
      if request.method == "POST" and 'ocean_type' in request.form and 'present_in_nz' in request.form and 'common_name' in request.form and 'scientific_name' in request.form and 'characteristics' in request.form and 'description' in request.form and 'threats' in request.form and 'location' in request.form:
      
        ocean_type = request.form['ocean_type']
        present_in_nz = request.form['present_in_nz']
        common_name = request.form['common_name']
        scientific_name = request.form['scientific_name']
        characteristics = request.form['characteristics']
        description = request.form['description']
        threats = request.form['threats']
        location = request.form['location']
        

        cursor = getCursor()

        #Insert guide information into the ocean table
        cursor.execute('INSERT INTO ocean (ocean_type, present_in_nz, common_name, scientific_name, characteristics, description, threats, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',(ocean_type, present_in_nz, common_name, scientific_name, characteristics, description, threats, location))
        ocean_id = cursor.lastrowid

        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                #Insert image information into the oceanImages table
                cursor.execute('INSERT INTO oceanImages (ocean_id, image_url) VALUES (%s, %s)',(ocean_id, filepath))

                connection.commit()
                msg = "You've successfully added one guide and uploaded images!"     

      elif request.method == 'POST':
        #form is empty
        msg = 'Please complete the form!' 
      return render_template('add-guide-staff.html', msg=msg)
    else:
        return redirect(url_for('login'))



@app.route("/staff/update-guide", methods = ["GET", "POST"])
def staff_update_guide():
    if 'user_id' in session and 'role' in session and session['role'] == 'staff':
        cursor = getCursor()
        try:
            cursor.execute("SELECT ocean_id FROM ocean")
            oceanIds = cursor.fetchall()

            if request.method == "POST":
                #Fetch data from form
                ocean_id = request.form.get('ocean_id')
                ocean_type = request.form.get('ocean_type')
                present_in_nz = request.form.get('present_in_nz')
                common_name = request.form.get('common_name')
                scientific_name = request.form.get('scientific_name')
                characteristics = request.form.get('characteristics')
                description = request.form.get('description')
                threats = request.form.get('threats')
                location = request.form.get('location')
                
                # Update the ocean guide information
                cursor.execute("""UPDATE ocean
                                  SET ocean_type = %s, present_in_nz = %s, common_name = %s, scientific_name = %s,
                                      characteristics = %s, description = %s, threats = %s, location = %s
                                  WHERE ocean_id = %s""",
                               (ocean_type, present_in_nz, common_name, scientific_name, characteristics, description, threats, location, ocean_id))
                
                # Handle file uploads
                for file in request.files.getlist('images'):
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        
                        
                        cursor.execute("UPDATE oceanImages SET image_url = %s WHERE ocean_id = %s", (filepath, ocean_id))

                connection.commit()
                msg = 'You have successfully updated the guide and uploaded images!'
            else:
                msg = ''
        except Exception as e:
            connection.rollback()
            msg = f'Error updating guide: {str(e)}'
        finally:
            cursor.close()
            connection.close()

        return render_template('update-guide-staff.html', msg=msg, guides=oceanIds)
    else:
        return redirect(url_for('login'))

@app.route("/staff/delete-guide", methods = ["GET", "POST"])
def staff_delete_guide():
    if 'user_id' in session and 'role' in session and session['role'] == 'staff':
        cursor = getCursor()
        
        try:
            cursor.execute("SELECT ocean_id FROM ocean")
            oceanIds = cursor.fetchall()
            msg = ''

            if request.method == "POST":
                #Fetch form data
                ocean_id = request.form['ocean_id']
                
                #Delete ocean details
                cursor.execute("DELETE FROM ocean WHERE ocean_id = %s", (ocean_id,))
                #Delete oncean photo
                cursor.execute("DELETE FROM oceanImages WHERE ocean_id = %s", (ocean_id,))
                
                #Commit the changes to the database
                connection.commit()
                
                msg = 'You have successfully deleted the guide'
        
        except mysql.connector.Error as err:
         
            connection.rollback()
            msg = f"Failed to delete the guide. Error: {err}"
        finally:
            #Close the cursor and connection
            cursor.close()
            connection.close()

        return render_template('delete-guide-staff.html', msg=msg, oceanIds=oceanIds)
  
    else:
        return redirect(url_for('login'))