#!/usr/bin/env python
# -*- coding: utf-8 -*-
#print u"Content-type: text/html; charset=utf-8\n\n"
#mycomment=get new messages and send it

import re
import subprocess
import MySQLdb

DEBUG = 1
def sendWap(phoneNum,userText):
    attempts = 0
    while attempts < 3:
        resultStatus = 0
        try:
    	    #python yowsup-cli -c config.example -w -s 79196967748 "мое сообщение"
    	    sendResult = subprocess.Popen(["/usr/bin/python",
				"/home/pi/Soft/yowsupOld/yowsup/src/yowsup-cli",
				"-c",
				"/home/pi/Soft/yowsupOld/yowsup/src/config.example",
				"-w",
				"-s",
				phoneNum,
				userText], stdout=subprocess.PIPE).stdout.read()
    	    #'Authed 79375298473\nSent message\nGot sent receipt\n'
            if DEBUG: print "Attempts={2} PhoneNum={0} sendResult={1}".format(phoneNum,sendResult,attempts)
            sendResultArray=re.split("\n", sendResult)
            #['Authed 79375298473', 'Sent message', 'Got sent receipt', '']
            sendResultArrayOK = ['Authed 79375298473', 'Sent message', 'Got sent receipt', '']
    	    for i in xrange(len(sendResultArray)):
		if sendResultArray[i]==sendResultArrayOK[i]: 
	     	    resultStatus+=2**i
	    break
	except IndexError:
            attempts += 1
    return resultStatus

def textPrepare(time, name, text):
    modText = ""
    modText = """{1} отправил вам сообщение в {0}\r\nчерез сервис py.elnote.ru:\r\n\r\n{2}""".format(time,name,text)
    return modText

db = MySQLdb.connect(host="92.53.98.158",user="azat385_rpi",passwd="zaq1xsw2",db="azat385_rpi")
cur = db.cursor()
getSQL = "SELECT * FROM whatsapp WHERE send IS NULL"
updateAllNULL = 'update whatsapp set send = "SENDED" where send is null limit 3'
cur.execute(getSQL)
data = cur.fetchall()#get all the data
#1 row of data
#0	1	2	3	4	5	6
#id	time	name	phone	text	robot	send
for row in data:
    sendText = ""
    sendText = textPrepare(row[1], row[2], row[4])
    sendStatus = sendWap(row[3],sendText)
    #sendStatus = sendWap(row[3],row[4])
    if DEBUG: print "The sendStatus = {0} for id = {1} phone = {2}".format(sendStatus,row[0],row[3]);
    if sendStatus == 15:
	updateNULLbyID = 'UPDATE whatsapp SET send = "SENDED" WHERE id={0}'.format(row[0])
	cur.execute(updateNULLbyID)
# commit your changes
db.commit()

