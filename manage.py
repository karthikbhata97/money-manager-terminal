from login import *
from functions import *
import pymysql
import sys

# Connect to mysql db
db = pymysql.connect(user="root", password="honor4c", host="localhost")
cursor = db.cursor()

# Create new database in case of first time!
mydatabase(db)
cursor.execute("USE user_login_data")
session = []                                                 # In case of login turn TRUE

if len(sys.argv) > 1:
    var = sys.argv[1]
else:
    var = 'nothing'

session = [False]

if var == '-n':                                              # '--new' arg to create a new user data and table
    login_signup(db)
elif var == '-l':
    session = login(db)                                           # log into database
else:
    pass

while session[0]:
    command = input(">> ")
    if command == 'add':
        add(db, session[1])
    elif command == 'balance':
        balance(db, session[1])
    elif command == 'logout':
        session[0] = False
    elif command == 'help':
        help()
    else:
        pass
