import pymysql
import getpass
import sys

# Create database and table on USERS
def mydatabase():
    try:
        cursor.execute("CREATE DATABASE user_login_data")
        cursor.execute("USE user_login_data")
        cursor.execute("""CREATE TABLE login_form
        (
        username varchar(15),
        password varchar(15),
        last_login date)
        """)
    except:
        pass

# Login for this current session
def login():
    username = input("Username: ")
    data = cursor.execute("SELECT password FROM login_form WHERE username= %s ", (username,))
    if data != 1:
        print("Invalid username!")
        return False
    else:
        password = getpass.getpass(prompt="Password: ")
        if (password,) == cursor.fetchone():
            print("Successful login!")
            return True
        else:
            print("Wrong password!")
            return False


# SignUp and Create individual database
def login_signup():
    data = 1
    while data != 0:
        username = input("Username: ")
        data = cursor.execute("SELECT password FROM login_form WHERE username=%s", (username,))
        if data != 0:
            print("Try a different username!")
            continue
        else:
            password = getpass.getpass(prompt="Enter password: ")
            verify = getpass.getpass(prompt="Re-enter password: ")
            if password == verify:
                cursor.execute("""INSERT INTO login_form (username, password) VALUES
                (%s, %s)
                """, (username, password))
                db.commit()
                cursor.execute("""CREATE TABLE %s
                (
                money int NOT NULL,
                credit_debit char NOT NULL,
                message varchar(50)
                )
                """ %(username))
                print("Successful creation of your database!")
            else:
                print("Passwords doesn't match!")



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

