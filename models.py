import sqlite3 as sql
from sqlite3 import OperationalError

def addUser(username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
        con.commit()
        
    except OperationalError:
        pass
    con.close()

def retrieveUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    users = []
    try:
        cur.execute("SELECT username, password FROM users")
        users = cur.fetchall()
        
    except OperationalError:
        pass
    con.close()
    return users

def addPokemon(pname,ptype,owner,plevel):
    con = sql.connect("database.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO OwnedPokemon (name,type,owner,level) VALUES (?,?,?,?)", (pname,ptype,owner,plevel))
        con.commit()
    except OperationalError:
        pass
    con.close()

def getPokeList():
    con = sql.connect("database.db")
    cur = con.cursor()
    pokemon = []
    try:
        cur.execute('SELECT * FROM Pokemon')
        pokemon = cur.fetchall()
    except OperationalError:
        pass
    con.close()
    return pokemon
    
def eraseUserPokemon(user,mon):
    con = sql.connect("database.db")
    cur = con.cursor()
    try:
        cur.execute('DELETE FROM OwnedPokemon WHERE owner = ? and name = ?',(user,mon))
        con.commit()
    except OperationalError:
        pass
    con.close()

def stillWild():
    #select all pokemon in OwnedPokemon that have level
    con = sql.connect("database.db")
    cur = con.cursor()
    try:
        cur.execute('SELECT Pokemon.name FROM Pokemon LEFT JOIN OwnedPokemon ON OwnedPokemon.name = Pokemon.name WHERE OwnedPokemon.name IS NULL')
        pokemon = cur.fetchall()
        #con.commit()
    except OperationalError:
        pass
    con.close()
    return pokemon

def searchByType(typename):
    con = sql.connect("database.db")
    cur = con.cursor()
    pokemon = []
    try:
        cur.execute("SELECT name FROM Pokemon WHERE  type = ?",(typename,))
        pokemon = cur.fetchall()
    except OperationalError:
        pass
    con.close()
    return pokemon

def eraseUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    try:
        cur.execute("DELETE * FROM users")
        con.commit()
    except OperationalError:
        pass
    con.close()

def userPokemon(user):
    con = sql.connect("database.db")
    cur = con.cursor()
    mons =  []
    try:
        cur.execute('SELECT name,type,level FROM OwnedPokemon Where owner=?',(user,))
        mons = cur.fetchall()
    except OperationalError:
        pass
    con.close()
    return mons

def updateLevel(newLevel,name,owner):
    con = sql.connect("database.db")
    cur = con.cursor()
    try:
        cur.execute('UPDATE OwnedPokemon SET level = ? WHERE name = ? and owner = ?',(newLevel,name,owner))
        con.commit()
    except OperationalError:
        pass
    con.close()

def getType(mon):
    con = sql.connect("database.db")
    cur = con.cursor()
    typ = None
    try:
        cur.execute('SELECT type From Pokemon Where name = ?',(mon,))
        typ = cur.fetchall()
    except:
        pass
    return typ
    

