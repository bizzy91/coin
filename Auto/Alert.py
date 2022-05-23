#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 10:48:07 2021

@author: bizzy

SMTL library 를 이용하여 메일 보내기
"""

import smtplib 
from email.mime.text import MIMEText 



def SENDtoME(title, content):
    smtp = smtplib.SMTP('smtp.gmail.com', 587) 
    smtp.ehlo() 
    smtp.starttls() # TLS 사용시 필요 
    smtp.login('bizzybak@gmail.com', 'aetymposhshsswws')
    msg = MIMEText(content) 
    msg['Subject'] = title 
    # msg['To'] = 'bizzybak@gmail.com'
    smtp.sendmail('bizzybak@gmail.com', 'bizzybak@gmail.com', msg.as_string())
    # smtp.sendmail('bizzybak@gmail.com', 'sinh9112@gmail.com', msg.as_string())
    smtp.quit()

