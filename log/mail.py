import smtplib
from email.mime.text import MIMEText
import json

def Keyerror(msg=""):
    raise KeyError(msg)

def mail(subject="",body="",From="SOPmanagement@cheremimaka.com",To="",CC=""):
    if subject == "":
        Keyerror("제목을 입력하십시오")
    elif body == "":
        Keyerror("본문을 입력하십시오")
    elif To == "":
        Keyerror("수신자를 입력하십시오")
    
    subject = subject
    body = body
    From = From
    To = To
    CC = CC

    with open('/home/instinctus/Desktop/log/outlookIDPW.json','r',encoding='utf-8') as IDPW:
        IDPW = json.load(IDPW)
        ID = IDPW['ID']
        PW = IDPW['PW']

    smtp = smtplib.SMTP('smtp.outlook.com', 587)
    smtp.ehlo()      # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login(ID,PW)

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['To'] = To
    msg['CC'] = CC

    smtp.sendmail(From, To, msg.as_string())
    smtp.quit()

if __name__=='__main__':
    mail(subject="Test",body="Test",To="geonho.lim@cheremimaka.com")