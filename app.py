from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import mail
#import boto3
import os
conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
socketio = SocketIO(app)

#S3=boto3.resource("s3", aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY_ID"))

@app.route("/")
def index():
    return render_template("room.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        


        if not request.form.get("email") or not request.form.get("password"):
            return "Please fill out all fields"

        _=c.execute("SELECT * FROM users WHERE email=:email",{"email": request.form.get("email")}).fetchall()
        if len(_) != 0:
            return "User already exists"

        pwhash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        c.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {"email": request.form.get("email"), "password": pwhash})
        conn.commit()
        mail(request.form.get("email"), "Joining Our Community!", "<h1>Hello! Welcome to Classcord!</h1>")
        return "registered successfully! Enjoy our service!"

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method =="POST":
        email = request.form.get("email")
        password = request.form.get("password")
    
        user = c.execute("SELECT * FROM users where email=:email", {"email": email}).fetchall()
    
        if len(user) == 0:
            return "Incorrect credentials"
    
    
        if not check_password_hash(user[0][2], password):
            return "Incorrect credentials"
        
        session["user_id"] = user[0][0]
    
        return "Logged in successfully!"
    
    
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return "Successfully logged out"
    

@app.route("/create-room", methods=["GET", "POST"])
def create_room():
    if request.method == "POST":
        pass



@app.route("/verify")
def verify():
    pass



@socketio.on("broadcast message")
def message_display(data):
    print(data)
    c.execute("INSERT INTO messages (message) VALUES (:message)",{"message": data["message"]})
    conn.commit()
    emit("show message", {"message": data["message"]}, broadcast=True)


@app.route("/upload", methods =["GET", "POST"])
def upload():
    if request.method == "POST" :
        pass
    else:
        return render_template("upload.html")



if __name__ == "__main__":
    socketio.run(app, debug=True)

