from flask import Flask
from flask import render_template, redirect, request, Response, session
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__,template_folder='template')

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'login'
app.config['MYSQL_CURSORCLASS']= 'DictCursor'
mysql=MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

#FUNCION DE LOGIN
@app.route('/acceso-login', methods=["GET","POST"])
def login():
    
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword':
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']
        
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM käyttäjiä WHERE correo = %s AND password = %s',(_correo, _password,))
        account = cur.fetchone()
        
        if account: 
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']
            
            if session['id_rol'] ==1:
                return render_template("admin2.html")
            elif session['id_rol'] ==2:
                 return render_template("admin.html")
        else: 
            return render_template('index.html', menssage="Väärä käyttäjä")
            
    
    
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

#REGISTER
@app.route('/create-register', methods=["GET","POST"])
def create_register():
    
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO käyttäjiä (correo, password, id_rol) VALUES (%s, %s, '2')",(correo,password))
    mysql.connection.commit()
    
    return render_template("index.html", menssage2="Successfully registered user")

#ADMIN-PROFILE--------------------------------------------
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/create-admin', methods=["GET","POST"])
def create_admin():
    
    name = request.form['txtName']
    lastname = request.form['txtLastname']
    mobile = request.form['txtMobile']
    contry = request.form['txtContry']
    province = request.form['txtProvince']
    address = request.form['txtAddress']
    postcode = request.form['txtPostcode']
    education = request.form['txtEducation']
    work = request.form['txtWork']
    company = request.form['txtCompany']
    workseg = request.form['txtWorkseg']
    companyseg = request.form['txtCompanyseg']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO profile (name, lastname, mobile, contry, province, address, postcode, education, work, workseg, company, companyseg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(name,lastname,mobile,contry,province,address,postcode,education,work,workseg,company,companyseg))
    mysql.connection.commit()
    
    return render_template('admin3.html')
    
#----------------------------------------------------------


if __name__=='__main__':
    app.secret_key="betty123"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

