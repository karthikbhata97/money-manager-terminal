import datetime
import openpyxl
import calendar

# add function adds a new transaction to the user's table
# balance function checks the balance at that moment
# help function will output the command file
# mstat function will give a mini statement on total money spent, withdrawn and balance at this moment
# stat will produce a xlsx file of user which has user's transactions month wise on each sheet



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
    cursor.execute("SELECT balance FROM %s WHERE id=(SELECT MAX(id) FROM %s)" %(username, username))
    balance_now = cursor.fetchone()
    print("Your balance is: {}".format(balance_now[0]))

def balance(db, username):
    cursor = db.cursor()
    cursor.execute("SELECT MAX(id) FROM %s" %(username))
    id = cursor.fetchone()
    if id[0] != None:
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
    now = datetime.datetime.now()
    cursor.execute("""SELECT money FROM %s
    WHERE credit_debit='d'""" %(username))
    values = cursor.fetchall()
    for item in values:
        spent = spent + item[0]
    cursor.execute("""SELECT money FROM %s
    WHERE credit_debit='c'""" % (username))
    values = cursor.fetchall()
    for item in values:
        credit = credit + item[0]
    cursor.execute("SELECT balance FROM %s WHERE id=(SELECT MAX(id) FROM %s)" %(username, username))
    final_balance = cursor.fetchone()
    if final_balance != None:
        final_balance = final_balance[0]
        print("Money spent:", spent)
        print("Money withdrawn:", credit)
        print("Final balance:", final_balance)


def stat(db, username):
    cursor = db.cursor()
    wb = openpyxl.Workbook()
    cursor.execute("""SELECT * FROM %s""" %(username))
    tuple = cursor.fetchall()
    month = 0
    active_sheet = wb.active
    # print(month)
    for item in tuple:
        this_month = item[1].month
        if month != this_month:
            month_name = calendar.month_name[this_month]
            wb.create_sheet(title=month_name)
            active_sheet = wb[month_name]
            active_sheet['A1'] = 'ID'
            active_sheet['B1'] = 'DATE'
            active_sheet['C1'] = 'MONEY'
            active_sheet['D1'] = 'CREDIT/DEBIT'
            active_sheet['E1'] = 'BALANCE'
            active_sheet['F1'] = 'MESSAGE'
        month = this_month
        idcell = 'A' + str(item[0]+1)
        monthcell = 'B' + str(item[0]+1)
        moneycell = 'C' + str(item[0]+1)
        credit_debitcell = 'D' + str(item[0]+1)
        balancecell = 'E' + str(item[0]+1)
        messagecell = 'F' + str(item[0]+1)
        active_sheet[idcell] = str(item[0])
        active_sheet[monthcell] = item[1]
        active_sheet[moneycell] = item[2]
        active_sheet[credit_debitcell] = item[3]
        active_sheet[balancecell] = item[4]
        active_sheet[messagecell] = item[5]
    all_sheets = wb.get_sheet_names()
    total_sheets = len(all_sheets)
    if total_sheets > 1:
        wb.remove_sheet(wb.get_sheet_by_name('Sheet'))
        name = username + ".xlsx"
        wb.save(name)
        print("Successful! Check for the file {}.xlsx to read the data!".format(username))



