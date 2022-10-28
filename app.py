import imaplib
import imp
import importlib
import email
from mail import Mail
from flask import Flask, render_template, request

import smtplib
import ssl
from email.message import EmailMessage
import json

app = Flask(__name__)
SERVER = 'imap.gmail.com'
connection = imaplib.IMAP4_SSL(SERVER)
mailList=[]
mail_ids = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin",methods=["POST"])
def signin():
    email = request.form.get("email","")
    password = request.form.get("password","")
    # try:
    #     global connection
    #     connection.login(email, password)
    #     return render_template("mailfilter.html")

    # except imaplib.IMAP4.error:
    #     return render_template("error.html",reason=imaplib.IMAP4.error.)
    global connection
    connection.login(email, password)
    return render_template("mailfilter.html")

@app.route("/mailFilter",methods=["POST"])
def mailFilter():
    global connection
    global mailList
    mailList.clear()
    global mail_ids
    mailFilter = request.form.get("mailFilter","")
    connection.select('inbox')
    status, data = connection.search(None,'(SUBJECT "'+mailFilter+'" UNSEEN)')
    unread_msg_nums = data[0].split()


    
   
    for block in data:
      
        mail_ids += block.decode('utf-8').split()

    for i in mail_ids:
        
        status, data = connection.fetch(i, '(RFC822)')

        for response_part in data:
            
            if isinstance(response_part, tuple):
                
                message = email.message_from_bytes(response_part[1])
                
                mail_from = message['from']
                mail_subject = message['subject']
                message_id = message['Message-ID']
                print("data_"+message_id)
                if message.is_multipart():
                    mail_content = ''

                    for part in message.get_payload():
                       
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

                if(("Request Yang commit".lower() in mail_subject.lower()) ):
                    mailInstance = Mail(mail_from,mail_subject,mail_content,message)
                    mailList.append(mailInstance)


    # for e_id in unread_msg_nums:
    #     connection.store(e_id, '-FLAGS', '\Seen')  
    
    for mail in mailList:
        print(mail)
    
    return render_template("mailfilter.html",mailList=mailList)

@app.route("/triggerReplyMail",methods=["POST"])
def triggerReplyMail():

    email_sender = 'rohithsuri3@gmail.com'
    email_password = 'tosrylvadzpigtbm'
    if(len(request.form.get("customResponseInput"))!=0):
        body = request.form.get("customResponseInput")
    else:
        body = "Hi Team,\n It's allowed"
    print("entered reply function")
    global mailList
    global mail_ids
    global connection
    message=mailList[int(request.form.get("index",""))-1].message
    email_receiver = message["from"]

    em = EmailMessage()
    em["Subject"] = "RE: "+message["Subject"].replace("Re: ", "").replace("RE: ", "")
    em['In-Reply-To'] = message["Message-ID"]
    em['References'] = message["Message-ID"]
    em['Thread-Topic'] = message["Thread-Topic"]
    em['Thread-Index'] = message["Thread-Index"]
    em['Cc'] = message['cc']

    em.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender,email_receiver , em.as_string())

        return render_template("mailfilter.html")
    except Exception as e:
        return render_template("error.html")

if(__name__=="__main__"):
    app.run(debug=True)

