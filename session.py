import threading
import time   
import sys
import string
import telnetlib
import re
import socket
from public import *
import os,random
from global_parame import *
from file_cmp_class import *
from telnet_class import *

class session(threading.Thread):#The session class is derived from the class threading.Thread  
    def __init__(self,HOST=None,PORT=None,USER=None,PASSWD=None):#,DEBUG_FLAG='1',TIMEOUT=240)#num=1,time=10):
        #print 'intil session //////'
        #print HOST,PORT,USER,PASSWD
        threading.Thread.__init__(self)
        #self.tel=telnetlib.Telnet()
        self.tel= myTelnet(HOST,PORT,USER,PASSWD)
        self.host = HOST
        self.port = PORT
        self.user = USER
        self.password = PASSWD
        self.thread_stop = False
        
        
    def run(self):#Overwrite run() method, put what you want the thread do here  
        #print 'telnet begain .....'
        try:
            if not self.tel.open():
                #print 'telnet open failed ...'
                self.thread_stop = True
            else:
                #print 'telnet OK ....'
                self.tel.mycommand(self.user,"name:",'1')
                self.tel.mycommand(self.password,'word:','1')
                self.tel.mycommand("enable",">",'1')
                self.tel.mycommand("con ter",")#","1")
        except:
            log_print('telnet num is full ...')
            self.thread_stop = True
    
        while not self.thread_stop:
            self.tel.mycommand(' ',")#",'1')
            time.sleep(5)
        self.tel.close() 
        
    def stop(self):
        print 'thread stop ...'
        time.sleep(0.1)
        self.thread_stop = True


if __name__=='__main__':
    nt = myTelnet()
    print nt.session_multi('192.168.22.240','23','admin','admin','7','25')