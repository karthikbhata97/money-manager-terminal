import datetime
import openpyxl
import os

def add(db, username):
    cursor = db.cursor()
    now = datetime.datetime.now()
    today = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    money = int(input("Amount of money: "))
    credit_debit = input("Credit or Debit? (c or d): ")
    message = input("A short message on transaction: ")
    cursor.execute("""INSERT INTO """+ username +""" (transaction_date, money, credit_debit, message)
    VALUES
    (%s, %s, %s, %s)
    """, (today, money, credit_debit, message))
    db.commit()
    cursor.execute("SELECT MAX(id) FROM %s" %(username))
    id = cursor.fetchone()
    id = id[0]
    if id == 1:
        balance = input("Your wallet balance: ")
    else:
        id = id - 1
        cursor.execute("SELECT balance FROM %s WHERE id=%s" %(username, id))
        id = id + 1
        balance = cursor.fetchone()
        balance = balance[0]
        if credit_debit == 'c':
            balance = balance + money
        else:
            balance = balance - money
    cursor.execute("UPDATE %s SET balance=%s WHERE id=%s" %(username, balance, id))
    db.commit()

def balance(db, username):
    cursor = db.cursor()
    cursor.execute("SELECT MAX(id) FROM %s" %(username))
    id = cursor.fetchone()
    cursor.execute("SELECT balance FROM %s WHERE id=%s" %(username, id[0]))
    present_balance = cursor.fetchone()
    present_balance = present_balance[0]
    print("Dear", username+"!")
    print("Your present balance is ", present_balance)

def help():
    with open('commands', 'r') as my_file:
        for line in my_file:
            print(line)


def mstat(db, username):
    cursor = db.cursor()
    spent = 0
    credit = 0
    cursor.execute("SELECT money FROM %s WHERE credit_debit='d'" %(username))
    values = cursor.fetchall()
    for item in values:
        spent = spent + item[0]
    cursor.execute("SELECT money FROM %s WHERE credit_debit='c'" %(username))
    values = cursor.fetchall()
    for item in values:
        credit = credit + item[0]
    cursor.execute("SELECT balance FROM %s WHERE id=(SELECT MAX(id) FROM %s)" %(username, username))
    final_balance = cursor.fetchone()
    final_balance = final_balance[0]
    print("Money spent:", spent)
    print("Money withdrawn:", credit)
    print("Final balance:", final_balance)


def stat(db, username):
    filename = username + ".xlsx"
    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            pass
    wb = openpyxl.Workbook()


