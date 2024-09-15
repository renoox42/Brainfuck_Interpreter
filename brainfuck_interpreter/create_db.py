import sqlite3


def create_db():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE programs (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, program TEXT)")
    connection.commit()
    connection.close()


create_db()