from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
# from forms import RegistrationForm, LoginForm, BookForm 
import datetime
import os
import sqlite3
db = 'Database/db.sqlite3'
#SAMPLE DATABASE
conn = sqlite3.connect(db)
app = Flask(__name__)
app.secret_key= ''

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
				amount integer NOT NULL,
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
		cur.execute("SELECT * FROM events ORDER BY event_data")
		events = cur.fetchall()
		# cur.execute("SELECT event_data FROM events")
		# eventdate = cur.fetchall()
		# status = 1
		# if str(eventdate) > str(datetime.datetime.now().date()):
		# 	status = 0
		# check_tables()
	return render_template('home.html',events = events)

# @app.route('/book',methods = ['GET','POST'])
# def bookseat():
# 	if request.method == 'POST':
# 		seatno = request.form["seatno"]
# 		name = request.form["name"]
# 		gender = request.form["gender"]
# 		dob = request.form["dob"]
# 		mobile = request.form["mobile"]

@app.route('/seats',methods = ['GET','POST'])
def seats():
	if request.method == 'POST':
		eventid = request.form["eventid"]
		print(eventid)
		with sqlite3.connect(db) as conn:
			cur = conn.cursor()
			cur.execute("SELECT * FROM seats,events WHERE events.event_id=? AND events.event_id = seats.event_id ORDER BY seats.amount DESC",[eventid])
			seats = cur.fetchall()
			
		return render_template('seats.html',seats = seats, eventid = eventid)

@app.route('/bookseat',methods = ['GET','POST'])
def bookseat():
	if request.method == 'POST':
		eventid = request.form["eventid"]
		seatno = request.form["seatno"]

		if(seatno[0]=='A'):
			seattype = "platinum"
		elif(seatno[0]=='B'):
			seattype = "gold"
		else:
			seattype = "silver"

		name = request.form["name"]
		gender = request.form["gender"]
		dob = request.form["dob"]
		mobile = request.form["mobile"]
		with sqlite3.connect(db) as conn:
			cur = conn.cursor()
			cur.execute("SELECT status FROM seats WHERE seat_no=? AND event_id=?",[seatno,eventid])
			state = cur.fetchall()
			if state[0][0]==0:
				cur.execute("INSERT INTO guests VALUES (?,?,?,?,?,?,?)",[eventid,name,gender,dob,mobile,seattype,seatno])
				cur.execute("UPDATE seats SET status = ? WHERE seat_no = ? AND event_id =?",[1,seatno,eventid])
				conn.commit()
				errorstatus = 0
			else:
				errorstatus = 1
		return render_template('bookingdone.html',errorstatus = errorstatus)

@app.route('/admin',methods=['GET','POST'])
def admin():
	if request.method == 'POST':
		eventid = request.form["eventid"]
		eventtitle = request.form["eventtitle"]
		eventtype = request.form["eventtype"]
		eventdate = request.form["eventdate"]
		eventtime = request.form["eventtime"]
		info = request.form["info"]
		location = request.form["location"]
		contact = request.form["contact"]
		performer = request.form["performer"]
		aboutperformer = request.form["aboutperformer"]
		with sqlite3.connect(db) as conn:
			cur = conn.cursor()
			cur.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?,?)",[eventid,eventtitle,eventtype,eventdate,eventtime,info,location,contact])
			cur.execute("INSERT INTO performers VALUES(?,?,?)",[eventid,performer,aboutperformer])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"platinum",5000,"A1",0])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"platinum",5000,"A2",0])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"platinum",5000,"A3",0])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"platinum",5000,"A4",0])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"gold",3000,"B1",0])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"gold",3000,"B2",0])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"gold",3000,"B3",0])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"gold",3000,"B4",0])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"silver",1500,"C1",0])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"silver",1500,"C2",0])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"silver",1500,"C3",0])
			cur.execute("INSERT INTO seats VALUES(?,?,?,?,?)",[eventid,"silver",1500,"C4",0])
			conn.commit()
	return render_template('admin.html')

@app.route('/performer',methods = ['GET','POST'])
def performer():
	if request.method == 'POST':
		eventid = request.form["eventid"]
		with sqlite3.connect(db) as conn:
				cur = conn.cursor()
				cur.execute("SELECT * FROM performers WHERE event_id = ?",[eventid])
				performer = cur.fetchall()
	return render_template('performer.html',performer = performer)

@app.route('/search',methods=['GET','POST'])
def search():
	if request.method == 'POST':
		eventtitle = request.form["searchbyname"]
		eventdate = request.form["searchbydate"]
		eventtype = request.form["searchbytype"]
		with sqlite3.connect(db) as conn:
			cur = conn.cursor()
			cur.execute("SELECT * FROM events WHERE event_title = ? OR event_data = ? OR event_type = ? ORDER BY event_data",[eventtitle,eventdate,eventtype])
			results = cur.fetchall()
	return render_template('search.html',results = results)

if __name__ == '__main__':
    app.run(port=5000,debug = True)
