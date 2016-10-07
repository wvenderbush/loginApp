#!/usr/bin/python
#Winston Venderbush
#Note: This is very dirty. I really should clean it up... but I'm still experimenting with all that Flask has to offer.

import random
import csv
import hashlib
import os
from flask import Flask, render_template, request, session, url_for


app = Flask(__name__)
app.secret_key = '\xe9$=P\nr\xbc\xcd\xa5\xe5I\xba\x86\xeb\x81L+%,\xcb\xcb\xf46d\xf9\x99\x1704\xcd(\xfc'


@app.route("/", methods = ["POST", "GET"])
def root():
	form = request.form
	if ("logval" in form):
		print session
		user = session["username"]
		session.pop(hashlib.sha256(user).hexdigest())
		session.pop("username")
		return render_template('main.html', title = "Login", message = "You have been logged out!", flag = "logout")
	if ("username" in session):
		print session
		return render_template('main.html', title = "Landing", message = "Welcome, " + session["username"], flag = "login")
	return render_template('main.html', title = "Login", message = "Enter your username and password:", flag = "logout")

@app.route("/registration/", methods=["POST", "GET"])
def register():
	return render_template('register.html', title = "Register")

@app.route("/regauth/", methods=["POST", "GET"])
def regauth():
	form = request.form
	user = hashlib.sha256(form['user']).hexdigest()
	password = hashlib.sha256(form['password']).hexdigest()
	with open('data/accounts.csv', 'rb') as f:
		reader = csv.reader(f)
		if os.path.getsize('data/accounts.csv') > 0:
			for row in reader:
				if (user == row[0] or form['user'] == "" or form['password'] == ""):
					return render_template('register.html', message = 'Cannot register that username and password!' , title = 'Register')
	f.close()

	fd = open('data/accounts.csv','a')
	fd.write(user + ',' + password+'\n')
	fd.close()
	return render_template('register.html', message = 'Account Registered!' , title = 'Register')
	

@app.route("/authenticate/", methods=["POST", "GET"])
def authenticate():
	form = request.form;
	user = hashlib.sha256(form['user']).hexdigest()
	password = hashlib.sha256(form['password']).hexdigest()
	with open('data/accounts.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if (user == row[0] and password == row[1]):
				f.close()
				session[user] = password
				session["username"] = form['user']
				return render_template('auth.html', title = "Login Success!", flag = "success", username = form['user'])
	f.close()
	return render_template('auth.html', title = "Login Failure!", flag = "fail", username = "")


if __name__ == "__main__":
    app.debug = True 
    app.run()