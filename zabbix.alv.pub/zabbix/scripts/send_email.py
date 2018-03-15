#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
import sys

#mailto_list = ['alvin.wan@shenmintech.com']
mailto_list=[]
mailto_list=sys.argv[1].split(';')
mailsubject=sys.argv[2]
mailcontent=sys.argv[3]
mail_host = "smtp.exmail.qq.com"  # 设置服务器
mail_user = "notify@sophiroth.com"  # 用户名
#mail_pass = sys.argv[1]  # 口令
mail_pass = 'yourpassword'
mail_postfix = "sophiroth.com"  # 发件箱的后缀


def send_mail(to_list, sub, content):
    me = "Notify" + "<" + mail_user + "@" + mail_postfix + ">"
    #msg = MIMEText(content, _subtype='plain', _charset='gb2312')
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        print(msg)
        server.close()
        return True
    except Exception as e:
        print (str(e))
        return False


if __name__ == '__main__':
    if send_mail(mailto_list, mailsubject, mailcontent):
        print ("发送成功")
    else:
        print ("发送失败")