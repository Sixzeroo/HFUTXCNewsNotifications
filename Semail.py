# -*- coding:utf-8 -*-

from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP

from value import EMAIL_CONFIG,RECEIVERS



class Email(object):

    def __init__(self):
        '''
        SMTP服务器SSL发送的初识设置
        '''
        self.smtp=SMTP(EMAIL_CONFIG['host_server'],EMAIL_CONFIG['port'])
        self.smtp.set_debuglevel(1)
        self.smtp.login(EMAIL_CONFIG['sender_mail'],EMAIL_CONFIG['passwd'])
        self.sender=EMAIL_CONFIG['sender']

    def send_email(self,reces,content,title):
        '''
        向指定接受列表发送邮件，邮件发送的SMTP服务器设置通过析构函数设置好
        :param reces: 接受方列表
        :param content: 发送内容
        :param title: 发送标题
        :return: 
        '''
        #纯文本邮件
        msg=MIMEText(content,"plain","utf-8")
        msg["Subject"]=Header(title,'utf-8')
        msg["From"]=self.sender
        if(isinstance(reces,list)):
            for rece in reces:
                msg["To"]=rece
                self.smtp.sendmail(self.sender,rece,msg.as_string())
        else:
            msg["To"] = reces
            self.smtp.sendmail(self.sender, rece, msg.as_string())

