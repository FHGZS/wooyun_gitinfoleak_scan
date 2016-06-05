#!env python
#coding=utf-8
# 
# Author:       liaoxinxi@nsfocus.com
# 
# Created Time: Sun 05 Jun 2016 04:48:48 AM EDT
# 
# FileName:     dnsresolver.py
# 
# Description:  
# 
# ChangeLog:
import dns.resolver
import sys
import traceback
from multiprocessing.dummy import Pool as ThreadPool

MYRESOLVER= dns.resolver.Resolver()

def dns_resolver(filename, dst="mail.txt"):
    try:
        fd = open(filename, 'r')
    except:
        print 'can not open the file:', filename
        return

    try:
        fd_write = open(dst,'w')
    except:
        print 'error in open',dst
        return 

    thread_num = 2
    pool = ThreadPool(thread_num)
    results = pool.map(verify_domain,fd.readlines())
    pool.close()
    pool.join()
    results = list(set(results))
    results = [item for item in results if item]
    

    for line in results:
        fd_write(line)

    fd_write.close()

def verify_domain(line):
    domains = line.rsplit("www.",1)
    if len(domains)< 2:
        print 'error line:', line
        return None
    domain = domains[-1]
    name = domains[0]
    try:
        response = MYRESOLVER.query(domain,"MX")
        for rdata in response: 
            mail_server = rdata.exchange.to_text()
            print "line:",domain , mail_server
            mail_line ="{0} {1} {2}\n".format(domain, mail_server.rsplit(".",1)[0], name) 
            return mail_line
    except Exception,e:
        traceback.print_exc()
        print 'dns query error',domain
        return None
    
            
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'usage: python dnsreolver.py domainfile'
        #return
    dns_resolver(sys.argv[1])

    
