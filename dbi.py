import sqlite3 as sql
from sqlite3 import OperationalError

if __name__ == "__main__":
    conn = sql.connect('database.db')

    file = open('schema.sql','r')
    F = file.read()
    file.close()

    commands = F.split(';')

    for c in commands:
            try:
                conn.execute(c)
            except OperationalError:
                pass

    cur = conn.cursor()
    file = open('mons.txt','r')
    for line in file:
        mon,typ = line.split()
        cur.execute("INSERT INTO Pokemon(name,type) values(?,?)",(mon,typ))
        conn.commit()
    conn.close()