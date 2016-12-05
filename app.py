from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g
from functools import wraps
import models as dbHandler
from Battle import *
from random import randint

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
        plevel = int(request.form.get('plevel'))
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
            flash("That is not a real Pokemon-Type combination!")
            return render_template('index.html', output=output)

        if(plevel > 25 or plevel < 1):
            flash("Pokemon level must be between 1 and 25!")
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
            dbHandler.stillWild()
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
    currentPokes = dbHandler.userPokemon(currentOwner)
    output = dbHandler.stillWild();
    newList = []
    BattleTxt = []
    newCurrentPokes = []
    notOwned = 0
    for i in range(len(currentPokes)):
        currentPokes[i]=list(currentPokes[i])
        currentPokes[i][0]=str(currentPokes[i][0])
    for i in currentPokes:
        newCurrentPokes.append(' | ' + str(i[0]))

    for i in range(len(output)):
        output[i]=list(output[i])
        output[i][0]=str(output[i][0])
    for i in output:
        newList.append(' | ' + str(i[0]))

    if request.method=='POST':
        battlewith = request.form.get('battlewith')
        Mons = dbHandler.userPokemon(currentOwner)
        owned = False
        Mon = None
        for i in Mons:
            if battlewith in i:
                owned = True
                Mon = i
        if not owned:
            #flash("You don't own that Pokemon!")
            return render_template('battle.html',output=newList,pokes=newCurrentPokes,notOwned=1)
        else:
            pname,ptype,plevel = [str(e) for e in Mon]
            plevel = int(plevel)
            OwnedMon = Pokemon(pname,ptype,plevel)
        battleagainst = request.form.get('battleagainst')
        WildType = dbHandler.getType(battleagainst)
        Type = str(WildType[0][0])
        RandLevel = randint(1,plevel+10)
        WildMon = Pokemon(battleagainst,Type,RandLevel)
        BattleTxt,winner = PokemonBattle(OwnedMon,WildMon)
        print winner 
        if winner == pname:
            #flash("You Won! {} has leveled up!".format(pname))
            BattleTxt.append("{} has leveled up!".format(pname))
            BattleTxt.append("{} has been added to your team!".format(battleagainst))
            dbHandler.updateLevel(plevel+1,pname,currentOwner)
            dbHandler.addPokemon(battleagainst,Type,currentOwner,RandLevel)
            output = dbHandler.stillWild();
            newCurrentPokes.append(' | ' + battleagainst)
        else:
            dbHandler.updateLevel(plevel-1,pname,currentOwner)
            BattleTxt.append("{} has lost a level.".format(pname))
        for i in BattleTxt:
            print i
        #print(battlewith,battleagainst,)
        #plevel = rand()

    return render_template('battle.html',output=newList,output2=BattleTxt,pokes=newCurrentPokes)

@app.route('/tracker', methods=['GET', 'POST'])
@login_required
def pokemonTracker():
    output = dbHandler.stillWild();
    newList = []
    for i in range(len(output)):
        output[i]=list(output[i])
        output[i][0]=str(output[i][0])

    for i in output:
        newList.append(str(i[0]))

    return render_template('tracker.html',output=newList)

def ToStr(output):
    newList = []
    for i in output:
        newList.append('{0:<15} | {1:<15} | {2:<5}'.format(i[0],i[1],i[2]))
    return newList

if __name__ == "__main__":
    
    app.run(debug = True)
