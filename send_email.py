import smtplib
EMAIL = ''

recv = ''

recv2 = ''

PASS =''

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('')
        server.ehlo()
        server.starttls()
        server.login(EMAIL, PASS)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(EMAIL,recv, message)
        server.quit()
        print("Success: Email sent!")
    except Exception as e :
        print("Email failed to send.--",e)

def send_email_2(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL, PASS)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(EMAIL,recv2, message)
        server.quit()
        print("Success: Email sent!")
    except Exception as e :
        print("Email failed to send.--",e)


subject = "Test subject"
msg = "Hello there, how are you today?"
