import sqlite3
import subprocess, os
from random import randint

def create_db_connect(database):
    def decorator(function):
        def wrapper(*args, **kwargs):
            connect = sqlite3.connect(database)
            cursor = connect.cursor()
            args += (cursor,)
            result = function(*args, **kwargs)
            connect.commit()
            connect.close()
            return result
        return wrapper
    return decorator

@create_db_connect("sqli.db")
def make_task_sqli(cursor):
    cursor.execute("DROP TABLE IF EXISTS Users;")
    cursor.execute('CREATE TABLE Users (username TEXT NOT NULL,password TEXT NOT NULL);')
    cursor.execute('INSERT INTO Users VALUES (\'admin\', \'hard\')')
    cursor.execute('INSERT INTO Users VALUES (\'jayse\', \'1337\')')
    cursor.execute('INSERT INTO Users VALUES (\'flag\', \'flag{0rm_r3ct_th1s_slq1}\')')

@create_db_connect("sqli.db")
def check_user_sqli(user, pswd, cursor):
    cursor.execute("SELECT username, password FROM Users WHERE username = \"{}\" AND password = \"{}\"".format(user, pswd))
    return cursor.fetchall()

@create_db_connect("note.db")
def make_task_xss_stor(cursor):
    cursor.execute("DROP TABLE IF EXISTS Note;")
    cursor.execute('CREATE TABLE Note (username TEXT NOT NULL, note TEXT NOT NULL);')
    cursor.execute('INSERT INTO Note VALUES (\'Rabbit\', \'Rly like markovka\')')
    cursor.execute('INSERT INTO Note VALUES (\'Wolf\', \'I want rabbit and maybe Red Hat\')')
    cursor.execute('INSERT INTO Note VALUES (\'Red Hat\', \'Go home through the forest? Great idea!\')')

def notes_to_dict(sqlfetch):
    return [{"username": x[0], "note": x[1]} for x in sqlfetch ]

@create_db_connect("note.db")
def get_notes_xss_stor(cursor):
    cursor.execute('SELECT * FROM Note;')
    return notes_to_dict(cursor.fetchall())

@create_db_connect("note.db")
def add_note_xss_stor(username, note, cursor):
    cursor.execute('INSERT INTO Note VALUES (\'{}\', \'{}\')'.format(username, note))

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)
    return iter(p.stdout.readline, b'')

def write_message_rce(note):
    command = 'echo "' + str(note) + '" > ' + os.path.join(os.path.abspath("."),'data_rce/')+ str(randint(0,100)) + '.txt'
    result = ''
    for line in run_command(command):
        result += line.decode()
    return result