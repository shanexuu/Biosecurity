from flask import Flask
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)


from app import views, admin_views, staff_views, mariners_views

