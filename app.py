#!/usr/bin/python
#Winston Venderbush
import random
import csv
import hashlib
from flask import Flask, render_template, request


app = Flask(__name__) 


@app.route("/")
def root():
	return render_template('main.html', title = "Login")

@app.route("/registration/", methods=["POST", "GET"])
def register():
	return render_template('register.html', title = "Register")

@app.route("/regauth/", methods=["POST", "GET"])
def regauth():
	form = request.form;
	user = hashlib.sha256(form['user']).hexdigest()
	password = hashlib.sha256(form['password']).hexdigest()
	with open('data/accounts.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if (user == row[0]):
				return render_template('register.html', message = 'Username already registered!' , title = 'Register')
	f.close()

	fd = open('data/accounts.csv','a')
	fd.write(user + ',' + password)
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
				return render_template('auth.html', title = "Login Success!", flag = "success")
	f.close()
	return render_template('auth.html', title = "Login Failure!", flag = "fail")


if __name__ == "__main__":
    app.debug = True 
    app.run()