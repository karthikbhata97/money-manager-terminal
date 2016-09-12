from login import *
import pymysql


# Connect to mysql db
db = pymysql.connect(user="root", password="honor4c", host="localhost")
cursor = db.cursor()

# Create new database in case of first time!
mydatabase()
cursor.execute("USE user_login_data")
session = False                                                 # In case of login turn TRUE

var = sys.argv[1]

if var == '--new':                                              # '--new' arg to create a new user data and table
    login_signup()
else:
    session = login()                                           # log into database

while session:
    command = input(">>")
    if command == 'add':
