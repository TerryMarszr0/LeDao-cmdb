# -*- coding:utf-8 -*-
import smtplib
from cmdb import configs

from email.mime.text import MIMEText
from email.MIMEImage import MIMEImage
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail

def sendHtmlEmail(msgTo, content, subject, file_list=[]):
    html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><title>Demystifying Email Design</title><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head><body style="width:apx; margin:auto">'+str(content)+'</body></html>'
    return sendEmail(msgTo, ("html", html), subject, file_list)


def sendEmail(msgTo, content, subject, file_list):
    (attachment, html) = content
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'cmdb@service.mwee.cn'
    msg['To'] = msgTo
    html_att = MIMEText(html, 'html', 'utf-8')
    att = MIMEText(attachment, 'plain', 'utf-8')
    msg.attach(html_att)
    for file in file_list:
        try:
            fp = open("/home/blackhole/"+file[0], 'rb')
            img = MIMEImage(fp.read(), _subtype="png")
            img.add_header('Content-ID', file[1].replace('.png', ''))
            msg.attach(img)
        except Exception, e:
            return False
    try:
        smtp = smtplib.SMTP()
        smtp.connect(configs.EMAIL_HOST)
        smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
    except:
        return False
    return True



