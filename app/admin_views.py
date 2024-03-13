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
    cursor =  getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':

      #Get the user's current id where stored in the session
      user_id = session['user_id']
      cursor.execute("SELECT * FROM users  WHERE user_id = %s", (user_id,))
      
      user = cursor.fetchone()

      cursor.execute("SELECT * FROM staff WHERE user_id = %s", (user_id,))

      staff = cursor.fetchone()
   
      return render_template('dashboard-admin.html', user=user, staff=staff)
    else:
      return redirect(url_for('login'))


@app.route("/admin/profile")
def admin_profile():
    cursor =  getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':

      #Get the user's current id where stored in the session
      user_id = session['user_id']
      cursor.execute("SELECT * FROM users  WHERE user_id = %s", (user_id,))
      
      user = cursor.fetchone()

      cursor.execute("SELECT * FROM staff WHERE user_id = %s", (user_id,))

      staff = cursor.fetchone()
   
      return render_template('profile-admin.html', user=user, staff=staff)
    else:
      return redirect(url_for('login'))


@app.route("/admin/settings", methods=["GET", "POST"])
def admin_settings():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
        user_id = session['user_id']
        #get session id 
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
      
      #Get mariners info
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
      
      #Get guide details
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
    
 
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
      msg = ''
      #check if ocean type, present in nz, common name and scientific name, characteristics, description, threats, location in the form
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

    


@app.route("/admin/update-guide", methods=["GET", "POST"])
def admin_update_guide():
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
        cursor = getCursor()
        try:
            cursor.execute("SELECT ocean_id FROM ocean")
            oceanIds = cursor.fetchall()

            if request.method == "POST":
                # Fetch form data
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

        return render_template('update-guide-admin.html', msg=msg, guides=oceanIds)
    else:
        return redirect(url_for('login'))

@app.route("/admin/delete-guide", methods=["GET", "POST"])
def admin_delete_guide():
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
        cursor = getCursor()
        
        try:
            cursor.execute("SELECT ocean_id FROM ocean")
            oceanIds = cursor.fetchall()
            msg = ''

            if request.method == "POST":
                #Fetch data from form
                ocean_id = request.form['ocean_id']
                
                #Delete one guide in ocean table
                cursor.execute("DELETE FROM ocean WHERE ocean_id = %s", (ocean_id,))
                #Delete photo in oceanImages table
                cursor.execute("DELETE FROM oceanImages WHERE ocean_id = %s", (ocean_id,))
                
                # Commit the changes to the database
                connection.commit()
                
                msg = 'You have successfully deleted the guide'
        
        except mysql.connector.Error as err:
           
            connection.rollback()
            msg = f"Failed to delete the guide. Error: {err}"
        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()

        return render_template('delete-guide-admin.html', msg=msg, oceanIds=oceanIds)
  
    else:
        return redirect(url_for('login'))

@app.route("/admin/view-staff")
def admin_view_staff():
    cursor = getCursor()
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
      #Get staff data
      cursor.execute("SELECT * FROM staff ")
      staffs = cursor.fetchall()
      print(staffs)
   
      return render_template('view-staff.html', staffs=staffs)
    else:
      return redirect(url_for('login'))



@app.route("/admin/add-staff", methods=["GET", "POST"])
def admin_add_staff():
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
        if request.method == "POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'first_name' in request.form and 'last_name' in request.form and 'staff_number' in request.form and 'hire_date' in request.form and 'position' in request.form and 'department' in request.form and 'work_phone_number' in request.form:
            # Fetch data from admin
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            staff_number = request.form['staff_number']
            hire_date = request.form['hire_date']
            position = request.form['position']
            department = request.form['department']
            work_phone_number = request.form['work_phone_number']

            cursor = getCursor()
            msg = ''

            try:
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
                elif not username or not password or not email or not first_name or not last_name or not staff_number or not hire_date or not position or not department or not work_phone_number:
                   msg = 'Please fill out the form!'
                else:
                   hashed = hashing.hash_value(password, salt='abcd')
                   now = datetime.now()
                   current_date = now.strftime('%Y-%m-%d')
                   #Insert staff data
                   cursor.execute("""INSERT INTO users (username, password, email, first_name, last_name, status, role, date_joined) VALUES (%s, %s, %s, %s, %s, 'Active', 'staff', %s )""", (username, hashed, email, first_name, last_name, current_date))


                   #Get user_id after inserting the staff
                   user_id = cursor.lastrowid

                   #Insert staff details into staff table
    
                   cursor.execute("""INSERT INTO staff (user_id, staff_number, hire_date, position, department, work_phone_number) VALUES (%s, %s, %s, %s, %s, %s)""", (user_id, staff_number, hire_date, position, department, work_phone_number))
                   
                   connection.commit()
                   msg = 'Staff member added successfully.'

                   
            except mysql.connector.Error as err:
                connection.rollback()
                msg = f'Failed to add staff member: {err}'
            
                
            return render_template('add-staff.html', msg=msg)
        elif request.method == 'POST':
            msg ='Please complete the form!'

        return render_template('add-staff.html')
    else:
        return redirect(url_for('login'))

    
@app.route("/admin/update-staff", methods=["GET", "POST"])
def admin_update_staff():
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
        cursor = getCursor()  

        if request.method == "POST":
            # Fetch data from the form
            staff_number = request.form['staff_number'] 
            hire_date = request.form['hire_date']
            position = request.form['position']
            department = request.form['department']
            work_phone_number = request.form['work_phone_number']

            #Update the staff's details in the database
            try:
                cursor.execute("""
                    UPDATE staff
                    SET hire_date = %s, position = %s, department = %s, work_phone_number = %s
                    WHERE staff_number = %s
                """, (hire_date, position, department, work_phone_number, staff_number))
                connection.commit()
                msg = "Staff details updated successfully."
            except Exception as err:
                connection.rollback()
                msg = f"Failed to update staff details: {err}"
            finally:
                cursor.close()
                connection.close()

            # Fetch staff numbers for the form selection again to refresh the list
            cursor = getCursor()
            cursor.execute("SELECT staff_number FROM staff")
            staffs = cursor.fetchall()
            cursor.close()
            connection.close()

            return render_template('update-staff.html', msg=msg, staffs=staffs)
        else:
           
            cursor.execute("SELECT staff_number FROM staff")
            staffs = cursor.fetchall()
            cursor.close()
            connection.close()

            return render_template('update-staff.html', staffs=staffs)
    else:
        return redirect(url_for('login'))



@app.route("/admin/delete-staff", methods=["GET", "POST"])
def admin_delete_staff():
    if 'user_id' in session and 'role' in session and session['role'] == 'admin':
        staffIds = []
        msg=''
        cursor = getCursor()
        try:
            cursor.execute("SELECT staff_number, user_id FROM staff") 
            staffIds = cursor.fetchall()

            if request.method == "POST":
                staff_number = request.form['staff_id']
                
                # Fetch user_id related to staff_id
                cursor.execute("SELECT user_id FROM staff WHERE staff_number = %s", (staff_number,))
                user_info = cursor.fetchone()  # Fetch the user_id of the staff
                if user_info:
                    user_id = user_info[0]
                    
                    # Delete staff entry from the staff table
                    cursor.execute("DELETE FROM staff WHERE staff_number = %s", (staff_number,))
                    
                    # Update the user's role to 'mariners' in the users table
                    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                    
                    connection.commit()
                    msg = 'You have successfully deleted the staff member and updated their role.'
                else:
                    msg = 'Staff not found or already deleted.'

        
        finally:
            cursor.close()
            connection.close()

        return render_template('delete-staff.html', msg=msg, staffIds=staffIds)
    else:
        return redirect(url_for('login'))
