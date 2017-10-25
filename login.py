import getpass
import datetime
# Create database and table on USERS
# user_login_data is the main database
# login_form maintains username and passwords
# respective users have their table on their username
'''
login_form:
usename
password
last login
'''

'''
user's table
id primary auto increments
transaction_date
money(debit/credit)
credit_debit (c or d)
balance (present balance)
message (a short message on present transaction)
'''




def mydatabase(db):
    cursor = db.cursor()
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
def login(db):
    cursor = db.cursor()
    username = input("Username: ")
    data = cursor.execute("SELECT password FROM login_form WHERE username= %s ", (username,))
    if data != 1:
        print("Invalid username!")
        return [False]
    else:
        password = getpass.getpass(prompt="Password: ")
        if (password,) == cursor.fetchone():
            print("Successful login!")
            data = cursor.execute("SELECT DATE(last_login) FROM login_form WHERE username=%s", (username,))
            lastlogin = cursor.fetchone()
            lastlogin = lastlogin[0]
            if lastlogin is not None:
                print("Your last login was on {}!".format(lastlogin))
            now = datetime.datetime.now()
            now = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
            cursor.execute("UPDATE login_form SET last_login=%s WHERE username=%s ", (now, username))
            db.commit()
            return [True, username]
        else:
            print("Wrong password!")
            return [False]


# SignUp and Create individual database
def login_signup(db):
    cursor = db.cursor()
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
                id int primary key auto_increment,
                transaction_date date,
                money int NOT NULL,
                credit_debit char NOT NULL,
                balance int,
                message varchar(50)
                )
                """ %(username))
                print("Successful creation of your database!")
            else:
                print("Passwords doesn't match!")


