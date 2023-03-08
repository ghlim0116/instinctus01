import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import os
import json

def Keyerror(msg=""):
    raise KeyError(msg)

def mail(subject="",body="",From="SOPmanagement@cheremimaka.com",To=[],CC=[],attachments=[]):
    if subject == "":
        Keyerror("제목을 입력하십시오")
    elif body == "":
        Keyerror("본문을 입력하십시오")
    elif To == "":
        Keyerror("수신자를 입력하십시오")
    
    msg = MIMEMultipart()
    msg['Subject'] = Header(s=subject,charset='utf-8')
    attach_msg = MIMEText(body,_charset='utf-8')
    msg.attach(attach_msg)
    msg['From'] = From
    msg['To'] = ",".join(To)
    msg['CC'] = ",".join(CC)
    if CC != []:
        To = To + CC
    if attachments != "":
        files = attachments
        for f in files:
            part = MIMEBase('application',"octet-stream")
            part.set_payload(open(f,"rb").read())
            encode_base64(part)
            part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

    with open('/home/instinctus/Desktop/log/outlookIDPW.json','r',encoding='utf-8') as IDPW:
        IDPW = json.load(IDPW)
        ID = IDPW['ID']
        PW = IDPW['PW']

    smtp = smtplib.SMTP('smtp.outlook.com', 587)
    smtp.ehlo()      # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login(ID,PW)

    smtp.sendmail(From, To, msg.as_string())
    smtp.quit()

if __name__=='__main__':
    mail(subject="Test",body="Test",To=["temp.lim@cheremimaka.com"],CC=["geonho.lim@cheremimaka.com"],attachments=[])