from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
# from forms import RegistrationForm, LoginForm, BookForm 
import os
import sqlite3
db = 'Database/db.sqlite3'
#SAMPLE DATABASE
conn = sqlite3.connect(db)
app = Flask(__name__)
app.secret_key= '04c816ee38ea4ee1843c22a6e67d8406'

# import secrets in python3 
# secrets.token_hex(16)
cur = conn.cursor()

#INITIAL QUERIES GO HERE
cur.execute('''CREATE TABLE IF NOT EXISTS events (event_id integer NOT NULL UNIQUE,
				event_title varchar(20) NOT NULL,
				event_type varchar(20) NOT NULL,
				event_data date NOT NULL,
				event_time time NOT NULL,
				info varchar(200),
				location varchar(50) NOT NULL,
				contact integer NOT NULL,
				PRIMARY KEY(event_id)	
				);''')

cur.execute('''CREATE TABLE IF NOT EXISTS guests (event_id integer NOT NULL,
				name varchar(30) NOT NULL,
				gender varchar(7) NOT NULL,
				birthdate date NOT NULL,
				mobile integer NOT NULL,
				seat_type varchar(9) NOT NULL,
				seat_no varchar(2) NOT NULL
				);''')

cur.execute('''CREATE TABLE IF NOT EXISTS performers (event_id integer NOT NULL,
				name varchar(30) NOT NULL,
				about text
			);''')

cur.execute('''CREATE TABLE IF NOT EXISTS seats ( event_id integer NOT NULL,
				seat_type varchar(9) NOT NULL,
				seat_no varchar(2) NOT NULL,
				status integer NOT NULL DEFAULT 0
			);''')
conn.commit()
conn.close()

def check_tables():		#PRINTS ALL TABLES
	with sqlite3.connect(db) as conn:
		cur = conn.cursor()
		cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
		var = cur.fetchall()
		print(var)

@app.route('/')
def home():
	with sqlite3.connect(db) as conn:
		cur = conn.cursor()
		cur.execute("SELECT * FROM events")
		events = cur.fetchall()
		# check_tables()
	return render_template('home.html',events = events)


if __name__ == '__main__':
    app.run(port=5000,debug = True)