# Function to Send Email 
import smtplib
from email.message import EmailMessage  

def email_sender(receiver_id, name , mobile):
    sender_id = "abc@gmail.com"
    sender_password =  "XXXX"
    msg = EmailMessage()
    body = f"Hey {name} !! \n\nSomething amazing happened few seconds ago !! you have registered to our Website \n\nCongratulations !! \nWe will try to give you best and fast service\n\nBelow are the information you have provided to us\n\nName : {name} \nMobile No. : {mobile} \nEmail : {receiver_id}\n\nThank you."
    msg.set_content(body)
    msg['subject'] = "Confirmation Mail"
    msg["to"] = receiver_id
    msg['from'] = sender_id
    s = smtplib.SMTP('smtp.gmail.com' , 587 )
    s.starttls()
    s.login(sender_id , sender_password)
    s.send_message(msg)
    s.quit()
