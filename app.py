from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g
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

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    currentOwner = session['currentuser']

    if request.method=='POST':
        pname = request.form.get('pname')
        plevel = request.form.get('plevel')
        ptype = request.form.get('ptype')
        #print(pname,plevel,ptype,currentOwner)
        LIST = dbHandler.getPokeList()
        UP = dbHandler.userPokemon(currentOwner)

        # CHECK IF POKEMON IS REAL
        output = dbHandler.userPokemon(currentOwner);
        for i in range(len(output)):
            output[i]=list(output[i])
            output[i][0]=str(output[i][0])
            output[i][1]=str(output[i][1])
        output = ToStr(output)
        if (ptype,pname) not in LIST:
            flash("That is not a real Pokemon!")
            return render_template('index.html', output=output)
        # END - CHECK IF POKEMON IS REAL

        for i in UP:
            print i
        x = False
        for i in UP:
            if pname in i:
                flash("Pokemon already exists. Please enter a different Pokemon name.")
                x = True
        if not x:
            dbHandler.addPokemon(pname,ptype,currentOwner,plevel)
            flash("Pokemon added successfully!")

        output = dbHandler.userPokemon(currentOwner);
        for i in range(len(output)):
            output[i]=list(output[i])
            output[i][0]=str(output[i][0])
            output[i][1]=str(output[i][1])
        output = ToStr(output)
        return render_template('index.html', output=output)
    else:
        output = dbHandler.userPokemon(currentOwner);
        for i in range(len(output)):
            output[i]=list(output[i])
            output[i][0]=str(output[i][0])
            output[i][1]=str(output[i][1])
        output = ToStr(output)
        return render_template('index.html', output=output)


@app.route('/removePokemon', methods=['GET', 'POST'])
@login_required
def removePokemon():
    currentOwner = session['currentuser']

    output = dbHandler.userPokemon(currentOwner);
    for i in range(len(output)):
        output[i]=list(output[i])
        output[i][0]=str(output[i][0])
        output[i][1]=str(output[i][1])

    output = ToStr(output)

    if request.method=='POST':
        pname = request.form.get('pname')

        print(currentOwner,pname)

        UP = dbHandler.userPokemon(currentOwner)
        for i in UP:
            print i
        x = False
        for i in UP:
            if pname in i:
                dbHandler.eraseUserPokemon(currentOwner,pname)
                flash("Pokemon Removed")
                x = True
        if not x:
            flash("Pokemon Does Not Exist")

    output = dbHandler.userPokemon(currentOwner);
    for i in range(len(output)):
        output[i]=list(output[i])
        output[i][0]=str(output[i][0])
        output[i][1]=str(output[i][1])

    output = ToStr(output)
    return render_template('removepoke.html', output=output)

@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        users = dbHandler.retrieveUsers()
        thisuser = request.form['username']
        x = (request.form['username'], request.form['password'])
        if x not in users:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            session['currentuser'] = thisuser
            flash('You have logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    error = None
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        thisuser = request.form['username']

        users = dbHandler.retrieveUsers()

        x = (request.form['username'], request.form['password'])
        print users
        print x
        if x in users:
            print "error"
            error = 'Username already exists. Please try again.'

            return render_template('addUser.html', error=error)
        else:
            dbHandler.addUser(username, password)
            session['logged_in'] = True
            session['currentuser'] = thisuser
            g.user = username
            return redirect(url_for('home'))
    else:

        return render_template('addUser.html',error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))

@app.route('/battle', methods=['GET', 'POST'])
@login_required
def battle():
    currentOwner = session['currentuser']
    output = dbHandler.getPokeList();
    newList = []
    for i in range(len(output)):
        output[i]=list(output[i])
        output[i][0]=str(output[i][1])
    for i in output:
        newList.append(' | ' + str(i[0]))

    if request.method=='POST':
        pname = request.form.get('pname')
        print(pname)
        #plevel = rand()

    return render_template('battle.html',output=newList)

def ToStr(output):
    newList = []
    for i in output:
        newList.append('{0:<15} | {1:<15} | {2:<5}'.format(i[0],i[1],i[2]))
    return newList

if __name__ == "__main__":
    
    app.run(debug = True)
