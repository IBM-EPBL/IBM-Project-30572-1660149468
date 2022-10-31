from flask import Flask, render_template, request, session
import ibm_db
import re
app=Flask(__name__)

app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cgn26120;PWD=KmAieIXO0PyEnTKy;", "", "")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg = " "
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        sql = "SELECT * FROM reg_detail WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
        else:
            msg = 'Incorrect username / password !'
            return render_template('index.html',msg=msg)
    return render_template('welcome_login.html',msg=msg)

@app.route('/registration_page')
def reg():
    return render_template('registration.html')

@app.route('/register',methods=['GET','POST'])
def register():
    msg = " "
    username=request.form['username']
    emailid= request.form['email']
    rollno = request.form['rollno']
    password= request.form['password']
        
    if (request.method =='POST') and (username=='' or emailid==''or rollno=='' or password=='' ):
        msg = "Please fill out the form !!!"
        return render_template('registration.html',msg = msg) 


    elif request.method == 'POST':
        sql = "SELECT * FROM reg_detail WHERE username=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',emailid):
            msg = "Invalid Email Address"
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg = "name must contain only character and numbers"
        else:
            insert_sql ="INSERT INTO reg_detail VALUES(?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,emailid)
            ibm_db.bind_param(prep_stmt,2,username)
            ibm_db.bind_param(prep_stmt,3,rollno)
            ibm_db.bind_param(prep_stmt,4,password)
            ibm_db.execute(prep_stmt)

            msg = "Successfully registered!!"

        return render_template('welcome.html',msg=msg)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

