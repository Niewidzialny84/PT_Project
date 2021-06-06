import smtplib,ssl ,os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendRecoveryMail(reciever: str,token: str):
    try:
        gmail_user = os.environ['pt_email']
        gmail_password = os.environ['pt_email_password']

        context = ssl.create_default_context()

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Password reset (PT project)'
        message['From'] = gmail_user
        message['To'] = reciever

        addr = 'https://molly.ovh:5050/reset/'+token

        text = """\
            This is a recovery password email
            If you did not set use recovery function ignore this mail
            Link : %s
            """ % (addr)

        html = """\
            <html>
                <body>
                <p>
                    This is a recovery password email
                    If you did not set use recovery function ignore this mail
                    <a href= "%s" > %s </a>
                </p>
                </body>
            </html>
            """ % (addr,addr)

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        server.sendmail(gmail_user,reciever,message.as_string())
        server.close()
    except Exception as ex:
        print(ex)
        pass