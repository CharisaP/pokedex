import sqlite3 as sql

def addUser(username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()


def retrieveUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    users = cur.fetchall()
    con.close()
    return users

def removeAllUsers():
    pass
#remove pokemon, add pokemon, search (type),

def addPokemon(pname):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO pokemon (pname) VALUES (?)", (pname))
    con.commit()
    con.close()

def searchByType(typename):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM pokemon WHERE type = typename")
    pokemon = cur.fetchall()
    con.close()
    return pokemon

def eraseUsers():
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE * FROM users")
        con.commit()
        con.close()
