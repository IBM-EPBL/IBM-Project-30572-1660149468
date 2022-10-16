from flask import Flask,render_template,redirect,url_for,request
app = Flask(__name__)

@app.route('/')
def html_page():
    return render_template('registration.html')

@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        mail = request.form['mail']
        number = request.form['number']
        return render_template('details.html',name = user,mailid=mail,no=number) 

if __name__ == '__main__':
    app.run(debug=True)