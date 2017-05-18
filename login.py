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

    print count
    return redirect('/')

app.run(debug = True)

    # if len(request.form['email']) < 1:
    #     flash("Email cannot be blank!")
    # elif not EMAIL_REGEX.match(request.form['email']):
    #     flash('Invalid Email Address')
    # # else if email doesn't match REGEX, display 'invalid email'
    # else:
    #     flash('Success')
