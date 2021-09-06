from flask import Flask , render_template , request , session , redirect , url_for
from pymongo import MongoClient
import bcrypt
from datetime import datetime 
import pytz
from Email import email_sender
from Email import Check_Email
from Forgot_Password import OTP_Sender
import os

IST = pytz.timezone('Asia/Kolkata')
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
app = Flask("Mail App")

db = client.users
port = "5050"
hostname = "0.0.0.0"

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/register' , methods = ['POST' , "GET"])
def register():
    if request.method == 'POST':
        name = request.form.get("name")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        passwd = request.form.get("password")
        existing_mail = db.users.find_one({"email":email})
        SignUptime = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')
        if existing_mail:
            return render_template("exist.html")

        isValid = Check_Email.is_validEmail(email)
        if isValid == True:
            hashpass = bcrypt.hashpw(passwd.encode('utf-8') , bcrypt.gensalt())
            db.users.insert_one({"name" : name , "mobile" : mobile , "email" : email , "password": hashpass,"SignUptime" : SignUptime})
            email_sender.email_sender(email , name, mobile)
            print("email send")
            return render_template("login.html")
        else:
            return "Wrong email or email does not exist"
    return render_template("index.html")

@app.route("/login" , methods = ['POST' , 'GET'])
def login():
    if request.method == "POST":
        global email
        email = request.form.get("email") 
        global login_email 
        login_email = client[db][collection].find_one({"email":email})
        if login_email:
            if bcrypt.hashpw(request.form['password'].encode('utf-8') , login_email['password']) == login_email['password']:
                global name
                name = login_email['name']
                phone = login_email['mobile']
                lastLoginTime = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')
                loginTime = datetime.now(IST).strftime('%H:%M:%S')
                db.users.update_one({"email" : email} ,{ "$set":{"lastLoginTime": lastLoginTime}})

                try:
                    lastLoginTime = login_email['lastLoginTime']
                    return render_template("Service.html" , email = email, name = name , lastLoginTime = lastLoginTime, phone = phone, loginTime = loginTime )
                except:
                    return render_template("Service.html" , email = email, name = name , lastLoginTime = ": you are new user", phone = phone, loginTime = loginTime ) 

            return render_template("error.html")
        else:
            return render_template("error.html")
    return render_template("login.html")


@app.route("/forgot_passwd", methods = ["POST", "GET"])
def forgot_passwd():
    if request.method == "POST" or request.method == "GET":
        return render_template("forgot_passwd.html")


@app.route("/otp", methods = ["POST", "GET"])
def OTP():
    if request.method == "POST" or request.method == "GET":
        global email
        email = request.form.get("email")
        passwd_email = client[db][collection].find_one({"email":email})
        if passwd_email: 
            name = passwd_email['name']
            global otp
            otp = OTP_Sender.otp_sender(email, name)
            print(otp)
            return render_template("otp.html")
        else:
            return "Email doesn't exist!!"
    else:
        return render_template("forgot_passwd.html")

    
@app.route('/Reset_passwd', methods = ["POST","GET"])
def Reset_passwd():
    if request.method == "POST" or request.method == "GET":
        otp_get = request.form.get("otp")
        if int(otp_get) == otp:
            return render_template("reset_passwd.html")
        else:
            return "Incorrect OTP"


@app.route('/update_passwd', methods = ["GET","POST"])
def update_passwd():
    if request.method == "POST":
        new_passwd = request.form.get("password")
        print(new_passwd)
        hashpass = bcrypt.hashpw(new_passwd.encode('utf-8') , bcrypt.gensalt())
        db.users.update_one({"email" : email} ,{ "$set":{"password": hashpass},"$currentDate":{"lastModified":True}
})
        return render_template("login.html")


app.run(debug= True , port= port, host= hostname)
