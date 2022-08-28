from flask import Flask,render_template,redirect,url_for,request,session,flash
import mysql.connector
import sys
from datetime import timedelta

app=Flask(__name__)

passwd=None
key='a'
with open("det.txt") as f:
	paswd,key=[i[:len(i)-2] for i in f.readlines()]

	

db=mysql.connector.connect(	host="localhost",
	user="root",
	passwd=paswd,
	database="admindashboard",
	auth_plugin="mysql_native_password")

cursor=db.cursor(buffered=True)
app.secret_key=key
app.permanent_session_lifetime= timedelta(minutes=5)



@app.route("/login",methods=["POST","GET"])
def login():
	if request.method=="GET":
		return render_template("login_app.html")
	else:
		upas=request.form["passwd"]
		uname="adminXYZ"
		cursor.execute("SELECT * FROM password")
		pas=None
		name=None
		for i in cursor:
			pas=i[0]
			name=i[1]
			break
		if upas==pas and uname==name:
			session["admin"]="adminXYZ"
			return redirect(url_for("welcome_page"))
		else:
			flash("Invalid credentials!")
			return render_template("login_app.html")


@app.route("/welcome",methods=["POST","GET"])
def welcome_page():
	if "admin" in session:
		return render_template("welcomepage_app.html")
	else:
		flash("You need to LogIn first!")
		return redirect(url_for("login"))

@app.route("/useradd.html",methods=["POST","GET"])
def add_user():
	if request.method=="POST":
		name=request.form["name"]
		mail=request.form["mail"]
		phone=request.form["phone"]
		address=request.form["addr"]
		image=request.files["file"]
		print(type(image.read()))
		bin_image=image.read()
		cursor.execute("INSERT INTO user(name,email,phone,address,image) VALUES (%s,%s,%s,%s,%s)",(name,mail,phone,address,bin_image))
		db.commit()
		return redirect(url_for("welcome_page"))
	else:
		return render_template("useradd.html")

@app.route("/viewuser.html")
def view_user():
	cursor.execute("SELECT * FROM user")



if __name__=="__main__":
	app.run(debug=True)