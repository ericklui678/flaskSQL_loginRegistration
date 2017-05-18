from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import md5
import re
import os, binascii
app = Flask(__name__)
mysql = MySQLConnector(app,'login_registration') #database name
app.secret_key = 'ThisIsSecret'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile('^[A-z]+$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm']
    # count correct fields
    count = 0

    # Validate first_name
    if len(first_name) <= 2:
        flash('First name must be at least 2 letters')
    elif not NAME_REGEX.match(first_name):
        flash('First name must only contain alphabet')
    else:
        print 'SUCCESS FIRST NAME'
        count += 1

    # Validate last_name
    if len(last_name) <= 2:
        flash('Last name must be at least 2 letters')
    elif not NAME_REGEX.match(last_name):
        flash('Last name must only contain alphabet')
    else:
        print 'SUCCESS LAST NAME'
        count += 1

    # Validate email
    if len(request.form['email']) < 1:
        flash("Email cannot be blank")
    elif not EMAIL_REGEX.match(email):
        flash('Invalid email format')
    else:
        print 'SUCCESS EMAIL'
        count += 1

    # Validate password
    if len(password) < 8:
        flash('Password must be at least 8 characters')
    else:
        print 'SUCCESS PASSWORD'
        count += 1

    # Validate confirm password
    if password != confirm:
        flash('Passwords do not match')
    else:
        print 'SUCCESS CONFIRM'
        count += 1

    # if all fields have correct input
    if count == 5:
        # SELECT EXISTS returns boolean whether email already exists in db
        query = "SELECT EXISTS (SELECT * FROM users WHERE email = '" + email + "')"
        output = mysql.query_db(query)
        for dict in output:
            for key in dict:
                if dict[key] == 1:   # if email exists in database
                    flash('Email already exists in database')
                    return redirect('/')
        # create random salt value
        salt = binascii.b2a_hex(os.urandom(15))
        # hash password with salt
        hashed_pw = md5.new(password + salt).hexdigest()
        # query to insert
        query = "INSERT INTO users(first_name, last_name, email, salt, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :salt, :password, NOW(), NOW())"
        # data will consists of whatever the user typed in
        data = {'first_name': first_name, 'last_name': last_name, 'email': email, 'salt': salt, 'password': hashed_pw}
        # run the query with data
        mysql.query_db(query, data)
        flash('You have now been registered!')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    print email, password

    return redirect('/')

app.run(debug = True)

#  INSERT INTO users(first_name, last_name, email, salt, password, created_at, updated_at)
#  VALUES ('victor', 'lui', 'victor.lui@gmail.com', '54321', 'passwordtest', NOW(), NOW())
