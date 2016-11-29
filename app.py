from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps
import models as dbHandler

app = Flask(__name__)

app.secret_key = 'my precious'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            #flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            #flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    error = None
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        dbHandler.addUser(username, password)
        users = dbHandler.retrieveUsers()
        print users
        return render_template('addUser.html', users=users)
    else:
        return render_template('addUser.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))
