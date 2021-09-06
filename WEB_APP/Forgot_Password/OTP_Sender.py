import random
import smtplib
import colorama
from email.message import EmailMessage
def otp_sender(email, name):
    sender_id = "abc@gmail.com"
    sender_password =  "XXXXX"
    msg = EmailMessage()
    otp = random.randint(1000, 10000)
    body = f"Hey {name} !! \n\nYou have asked for forgot password \nThis is the OTP to change the password : {otp} \n\nBelow are the information you have provided to us\n\nName : {name} \nEmail : {email}\n\nIf you have not asked for this then ignore this message\n\nThank you."
    msg.set_content(body)
    msg['subject'] = "Forgot Password"
    msg["to"] = email
    msg['from'] = sender_id
    s = smtplib.SMTP('smtp.gmail.com' , 587 )
    s.starttls()
    s.login(sender_id , sender_password)
    s.send_message(msg)
    s.quit()
    return otp

# print(otp_sender("nmmn"))
