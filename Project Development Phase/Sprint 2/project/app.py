import re
import sqlite3 as sql

import ibm_db
from flask import Flask, flash, render_template, request, session ,redirect,url_for

conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cgn26120;PWD=Ihi4yBvkSmcN0liY",'','')

app = Flask(__name__)
app.secret_key="muthuraja"

@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    msg = ''
    if 'loggedin' in session.keys():
       return render_template("dashboard.html") 

    elif request.method == 'POST' :
        username = request.form['username']
        pd = request.form['password']
        sql = "SELECT * FROM people WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,pd)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            return render_template('dashboard.html')
        else:
            if username=="" and pd=="" :
                msg = 'Fill the required details!!'
            else:
                msg='Incorrect Username/Password'
    return render_template('login.html', msg = msg)
    

@app.route('/registration_page', methods=['GET', 'POST'])
def signup():
    msg=''
    if request.method == "POST":
        username=request.form['name']
        email=request.form['email']
        pw=request.form['password'] 
        address=request.form['address']
        phone=request.form['phone']
        sql='SELECT * FROM people WHERE email =?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)
            
        if acnt:
            msg='Account already exits!!'
            return render_template("registration_page.html",msg=msg)
        
        elif username=="" and email=="" and pw=="" and address=="" and phone=="":
            msg='Fill the form first!!'
            return render_template("registration_page.html",msg=msg)
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg='Please enter the a valid email address'
            return render_template("registration_page.html",msg=msg)

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg='name must contain only character and number'
            return render_template("registration_page.html",msg=msg)

        else:
            create_table = 'CREATE TABLE {}(prodname VARCHAR(20),quantity integer,warehouse_location varchar(20))'.format(str(username))
            query = ibm_db.prepare(conn, create_table)
            ibm_db.execute(query)
            insert_sql='INSERT INTO people VALUES (?,?,?,?,?)'
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,username)
            ibm_db.bind_param(pstmt,4,address)
            ibm_db.bind_param(pstmt,5,phone)
            ibm_db.bind_param(pstmt,3,email)
            ibm_db.bind_param(pstmt,2,pw)
            ibm_db.execute(pstmt)
            mg='You have successfully registered click signin!!'
            return render_template("login.html")
    else:
        #msg="fill out the form first!"
        return render_template("registration_page.html",msg=msg)

@app.route('/logout')
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return render_template("home.html")

@app.route('/add_stock',methods=['GET','POST'])
def add_stock():
    msg='' 
    if request.method == "POST":
        prodname=request.form['prodname']
        quantity=request.form['quantity']
        warehouse_location=request.form['warehouse_location'] 
        sql='SELECT * FROM {} WHERE prodname =?'.format(session['username'])
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,prodname)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)
            

        if prodname=="" or quantity=="":
            msg="Fill all the stock detail!!"
            return render_template('add_stock.html',msg=msg)    

        elif acnt:
            msg='Product already exits!!'
            return render_template('add_stock.html',msg=msg)

        else:
            insert_sql='INSERT INTO {} VALUES (?,?,?)'.format(session['username'])
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,prodname)
            ibm_db.bind_param(pstmt,2,quantity)
            ibm_db.bind_param(pstmt,3,warehouse_location)
            ibm_db.execute(pstmt)
            msg='You have successfully added the products!!'
            return render_template("dashboard.html")      

    else:
        if 'loggedin' in session.keys():
            return render_template('add_stock.html',msg=msg)
        else:
            return redirect('/login')
        

@app.route('/delete_stock',methods=['GET','POST'])
def delete_stock():
    if(request.method=="POST"):
        prodname=request.form['prodname']
        sql2="DELETE FROM {} WHERE prodname=?".format(session['username'])
        stmt2 = ibm_db.prepare(conn, sql2)    
        ibm_db.bind_param(stmt2,1,prodname)
        ibm_db.execute(stmt2)
        print(stmt2)

        flash("Product Deleted", "success")

        return render_template("dashboard.html")
    else:
        if 'loggedin' in session.keys():
            return render_template('delete_stock.html')
        else:
            return redirect('/login')        

@app.route('/update_stock',methods=['GET','POST'])
def update_stock():
    msg=''
    if request.method == "POST":
        prodname=request.form['prodname']
        quantity=request.form['quantity']
        warehouse_location=request.form['warehouse_location'] 
        sql='SELECT * FROM {} WHERE prodname =?'.format(session['username'])
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,prodname)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)

        if prodname=="" or quantity=="":
            msg="Fill all the stock details"
            return render_template('update_stock.html',msg=msg)

        elif acnt:
            insert_sql='UPDATE {} SET  quantity=?,warehouse_location=? WHERE prodname=? '.format(session['username'])
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,quantity)
            ibm_db.bind_param(pstmt,2,warehouse_location)
            ibm_db.bind_param(pstmt,3,prodname)
            ibm_db.execute(pstmt)
            msg='You have successfully updated the products!!'
            return render_template("dashboard.html",msg=msg)   
            
        else:
             msg='Product not found!!'
             return render_template('update_stock.html',msg=msg)
               

    else:
        if 'loggedin' in session.keys():
            return render_template('update_stock.html')
        else:
            return redirect('/login')


@app.route('/view_stock',methods=['GET','POST'])
def view_stock():
    if request.method == "POST":
        sql = "SELECT * FROM {}".format(session['username'])
        stmt = ibm_db.prepare(conn, sql)
        result=ibm_db.execute(stmt)
        print(result)

        products=[]
        row = ibm_db.fetch_assoc(stmt)
        print(row)
        while(row):
            products.append(row)
            row = ibm_db.fetch_assoc(stmt)
            print(row)
        products=tuple(products)
        print(products)

        if result>0:
            return render_template('view.html', products = products)
        else:
            msg='No products found'
            return render_template('view.html', msg=msg)
    else:
        if 'loggedin' in session.keys():
            return render_template('dashboard.html')
        else:
            return redirect('/login')



if __name__ == "__main__":
    app.run(debug=True,threaded=True)