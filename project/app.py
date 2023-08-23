from flask import Flask, render_template, request, redirect
import mysql.connector
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'demo'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/purchase', methods=['POST', 'GET'])
def purchase():
    msg = ''
    if request.method == 'POST':

        item = request.form.get('name')
        qty = int(request.form.get('qty'))
        rate = request.form.get('rate')
        
        amount = int(rate) * qty
        msg=amount
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT cash FROM compay WHERE campanyname = "Namma Kaddai"')
        amt = 1000
        cash=amt-amount
        if cash >= 0:
            cursor.execute('update item set qty=qty+%s where item=%s',(qty,item,))
            mysql.connection.commit()
            cursor.execute('insert into purchase(item,qty,rate,amount) values(%s,%s,%s,%s)',(item,qty,rate,amount,))
            mysql.connection.commit()
            cursor.execute('UPDATE compay SET cash = %s WHERE campanyname = "namma kaddai"', (cash,))
            mysql.connection.commit()
            return redirect("/purchase1")
            
        
                    
    return render_template('users.html', msg=msg)
@app.route('/sales',methods=['POST','GET'])
def sales():
    if request.method == 'POST':

        item = request.form.get('name')
        qty = int(request.form.get('qty'))
        rate = request.form.get('rate')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT qty FROM item WHERE item = %s',(item))
    ite=cursor.fetchone()[0]

    if(int(ite)>=qty):
        qty1=int(ite)-qty
        amount=qty*rate
        cursor.execute('update item set qty=qty+%s where item=%s',(qty1,item,))
        mysql.connection.commit()
        cursor.execute('insert into sales(item,qty,rate,amount) values(%s,%s,%s,%s)',(item,qty,rate,amount,))
        mysql.connection.commit()
        cursor.execute('UPDATE compay SET cash = cash+%s WHERE campanyname = "namma kaddai"', (amount,))
        msg=amount

    else:
        msg="error"
    return render_template('sales.html',msg=msg)

@app.route('/purchase1')
def users():
    cursor = mysql.connection.cursor()
    users=cursor.execute("SELECT * FROM purchase")
    user_details = cursor.fetchall()
    return render_template('users.html', purchase=user_details)

@app.route('/companybalance')
def balance():
    cursor = mysql.connection.cursor()
    users=cursor.execute("SELECT * FROM compay")
    balance_details = cursor.fetchall()
    return render_template('companybal.html',compay=balance_details)

@app.route('/itemdetail')
def itemdetails():
    cursor = mysql.connection.cursor()
    users=cursor.execute("SELECT * FROM item")
    itemdet_details = cursor.fetchall()
    return render_template('itemdetails.html',item=itemdet_details)


if __name__ == '__main__':
    app.run(debug=True)
