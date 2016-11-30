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
#remove pokemon, add pokemon, search (type),

def addPokemon():
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
