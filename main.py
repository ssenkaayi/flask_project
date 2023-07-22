from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'hello'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)


@app.route('/')
def home():

    return render_template('index.html')

@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/user')
def user():
    my_cursor = mysql.connection.cursor()
    my_cursor.execute('SELECT * FROM USERS')
    data = my_cursor.fetchall()
    my_cursor.close()

    return render_template('user.html',users = data)

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')



@app.route('/insert', methods = ['POST'])
def insert():
    flash('account created successfully')
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        my_cursor = mysql.connection.cursor()
        my_cursor.execute('INSERT INTO USERS (user_name , user_password) VALUES(%s,%s)', (name, password))
        mysql.connection.commit()
        return redirect(url_for('login'))

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name
        password = request.form['password']
        my_cursor = mysql.connection.cursor()
        my_cursor.execute('SELECT * FROM USERS WHERE user_name =  "' +name+ '"  and user_password = "'+ password +'" ')
        user_data = my_cursor.fetchone()
        if user_data is None:
            flash('login with correct name and password')

            return redirect(url_for('login'))


        else:
            flash('logged in successfully')
            return redirect(url_for('products'))

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/logout')
def logout():
    session.pop('name',None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

