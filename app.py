#!/usr/bin/python
#Winston Venderbush
import random
from flask import Flask, render_template, request


app = Flask(__name__) 


@app.route("/")
def root():
	print request.headers
	return render_template('main.html', title = "Login")

@app.route("/authenticate/", methods=["POST", "GET"])
def authenticate():
	user = "wvenderbush"
	pword = "winston1"
	d = request.form
	if (d["user"] == "wvenderbush" and d["password"] == "winston1"):
		return render_template('auth.html', title = "Success!", flag = "success")
	else:
		return render_template('auth.html', title = "Failure!", flag = "fail")

if __name__ == "__main__":
    app.debug = True 
    app.run()