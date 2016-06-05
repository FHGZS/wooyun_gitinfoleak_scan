#!/usr/bin/python
# -*- coding: utf-8 -*-
#author:ago
import re
import urllib
import string
import argparse
import os
import sys
import threading, time
import MySQLdb
import time

reload(sys)
sys.setdefaultencoding('utf-8')

conn = MySQLdb.Connection(host="127.0.0.1", port=3306, user="gitscan", passwd="gitscan", charset="UTF8")
conn.select_db('gitscan')

cursor = conn.cursor(MySQLdb.cursors.DictCursor)



def getHtmlSummary(url):
    page = urllib.urlopen(url)
    content = page.read()
    return content

def getHtmlurl(html):
    reg = r'href="(.*?)" title'
    urlre = re.compile(reg)
    urllist = re.findall(urlre,html)
    return urllist


#q = raw_input ("pelase input the keyword(eg:username+password+mail):")
import urllib
import urllib2
import bs4

def search_github(query):
    query = urllib.quote(query)
    github_url = "https://github.com/search?o=desc&p=%s&q=%s&s=indexed&type=Code&utf8="%(str(0),query)        
    header = {}
    request = urllib2.Request(github_url,header=header)
    response = urllib2.urlopen(request, timeout=30)
    if response and response.getcode() == 200:
        data = response.read()
        soup = bs4.BeautifulSoup(data)




def emails():    
        mails=[]
        htmls=[]
        x = range (1,6)
        for i in x:
            page = str(i)
            try :
				htmlSummary = getHtmlSummary("https://github.com/search?o=desc&p="+str(i)+"&q=mail+password&s=indexed&type=Code&utf8=✓")        
				urllist = getHtmlurl(htmlSummary)
            except:
				pass
            #test = urllist[2:12]
            #if len(urllist) > 2:
            print "searching on the page "+page+",please wait..."
            for url in urllist[2:12]:
                try:
                    htmlDetail = getHtmlSummary("https://github.com"+url)
                    reg_emails1 = re.compile('[\w!#$%&\'*+/=?^_`{|}~-]+(?:\.[\w!#$%&\'*+/=?^_`{|}~-]+)*'+'@(?:[\w](?:[\w-]*[\w])?\.)'+'[\w](?:[\w-]*[\w])?')
                    reg_emails2 = re.compile('[\w!#$%&\'*+/=?^_`{|}~-]+(?:\.[\w!#$%&\'*+/=?^_`{|}~-]+)*'+'@(?:[\w](?:[\w-]*[\w])?\.)'+'(?:[\w](?:[\w-]*[\w])?\.)'+'[\w](?:[\w-]*[\w])?')
                    mail1 = reg_emails1.findall(htmlDetail)
                    mail2 = reg_emails2.findall(htmlDetail)
                    mail = mail1+mail2					
                    mails.extend(mail)
                except:
				    pass
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            #with open('recent_mails.txt', 'wb+') as domain_file:
        for item in mails:
            domain = item.split('@',1)[1]
                #domain_file.write(item + '\n')
            if domain in domains:
			    cursor.executemany("insert into persons (mail) values (%s)", [item])
                #print item

c = range (1,100000)
for a in c:    
    emails()
    time.sleep(1000)


print "I need you,boss~~"
cursor.close()
conn.close()
