#-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        udp_class.py
# Purpose:     
#
# Author:      gongke
#
# Created:     2013/01/15
# RCS-ID:      $Id: udp_class.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------


import socket
import sys
import string
import os
import time
import re
from public import *
reload(sys)
sys.setdefaultencoding("utf-8")
class myudp:
    def __init__(self,HOST=None,PORT='9999',DEBUG_FLAG=True):
        #-----------------------------------------------------------------------------
        # Name:        init fuction
        # param:       HOST:host name PORT:PORT 
        # explain:     initialize the myudp class
        # Author:      gongke
        #
        # Created:     2013/01/15
        #-----------------------------------------------------------------------------
        self.host = HOST
        self.port = string.atoi(PORT)
        if string.atoi(DEBUG_FLAG)==1:
            self.debugflag = True
        else:
            self.debugflag = False
        #self.debugflag = DEBUG_FLAG
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(20)
    
    def client_connect(self):
        #-----------------------------------------------------------------------------
        # Name:        client_connect fuction
        # param:       None
        # explain:     the udp client connect
        # Author:      gongke
        #
        # Created:     2013/01/15
        #-----------------------------------------------------------------------------
        try:
            self.sock.connect((self.host,self.port))
        except:
            print_mes = "client connect " +self.host +" fail"
            print print_mes
            info_public(print_mes)
            self.sock.close()
            return False
        print_mes = "client connect " +self.host +" success"
        print print_mes 
        info_public(print_mes)
        return True
    
    def server_connect(self):
        #-----------------------------------------------------------------------------
        # Name:        server_connect fuction
        # param:       None
        # explain:     the udp server connect
        # Author:      gongke
        #
        # Created:     2013/01/15
        #-----------------------------------------------------------------------------
        try:
            #self.sock.bind((self.host,self.port))
            self.sock.bind(("",self.port))
        except:
            
            print_mes = "server bind " +self.host + " fail"
            print print_mes
            info_public(print_mes)
            self.sock.close()
            return False
        print_mes = "server bind " +self.host + " success"
        print print_mes
        info_public(print_mes)
        #self.sock.listen(10)
        return True
   
    def sleep_m(self,TIME):
        int_time = string.atoi(TIME)
        time.sleep(int_time)
        
    def command_find(self,REC,count,MSG,find_str,addresss):
        count_tmp=0
        #print "***\n"
        while True:
            #print "-----------------------\n"
            mre=re.compile(find_str)
            result = mre.search(REC)
            #print "-------------%s----------\n" %result
            if result:
                break
            else:
                count_tmp = count_tmp+1
                if count_tmp <= count:
                    print_mes = "send msg " + MSG
                    print print_mes
                    info_public(print_mes)
                    #print "send msg %s" %MSG
                    print_mes = "send the mes:" + str(count_tmp) 
                    print print_mes
                    info_public(print_mes)
                    #print "count %d send this mes" %count_tmp
                    self.sock.sendto(MSG,addresss)
                else:
                    #print "count %d  but not find" %count_tmp
                    print_mes = "send the mes:" + str(count_tmp) 
                    print print_mes
                    info_public(print_mes)
                    return False
        return True

    #def client_all(self,CLIENTIP,PORT_STR):
        
    
    def client_use_byserver(self,MSG,Address):
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_sock.connect(Address)
        temp_sock.sendall(MSG)
        
    def server_rec(self,MSG,REC1,CLIENTIP,PORT_STR,RECSTOP,find_str):
        PORT=string.atoi(PORT_STR)
        address2=(CLIENTIP,PORT)
        count_tmp=1 
        FirstFlag = False
        #print address2
        """
        print_mes = "Fisrt ping clientIp:",CLIENTIP
        print print_mes
        info_public(print_mes)
        cmd_str = 'ping  ' + CLIENTIP + '-n 1'
        cmd_find_str = 'Received = 1'
        cmd_command(cmd_str,cmd_find_str)
        """
        REC = None
        #self.sock.settimeout(20)
        
        while True:
            
            if count_tmp>3:
                print_mes = "this "+ find_str + " not find in the "
                print print_mes
                info_public(print_mes)
                return False
            try:
                REC,address2 = self.sock.recvfrom(2048)
                print_mes = "recv data from "  + address2[0] +"," + REC
                print print_mes
                info_public(print_mes)
            except:
                print_mes = "\nnot recv date"
                print print_mes
                info_public(print_mes)
                print_mes = "send msg "  + MSG
                print_mes = print_mes + "count :" + str(count_tmp)
                print print_mes
                info_public(print_mes)
                print "except  address2 :",address2
                """
                self.sock.connect(address2)
                self.sock.sendto(MSG,address2)
                """
                self.client_use_byserver(MSG,address2)
                
                count_tmp = count_tmp + 1
                time.sleep(4)
                continue
            if cmp(address2[0],CLIENTIP)<0:
                print "Lost recv data ip:" ,address2[0]
                print "I want to get the ip:",CLIENTIP
                #time.sleep(10)
                continue
            if REC:
                mre=re.compile(find_str)
                result = mre.search(REC)
                if result:
                    return True
            print_mes = "send msg "  + MSG
            print_mes = print_mes + "count :" + str(count_tmp)
            print print_mes
            info_public(print_mes)
            self.sock.sendto(MSG,address2)
            count_tmp = count_tmp + 1
        return True
        
    def server_send(self,MSG,REC1,CLIENTIP,PORT_STR,RECSTOP,find_str):
        
        
        #time.sleep(10)
        PORT=string.atoi(PORT_STR)
        address2=(CLIENTIP,PORT)
        count_tmp=0 
        FirstFlag = False
        while True:
            result=None
            print_mes = "waiting for message:"  
            print print_mes
            info_public(print_mes)
            try:
                REC,address2 = self.sock.recvfrom(2048)
                #print "I want ip:",CLIENTIP
                print_mes = "recv data from "  + address2[0] +"," + REC
                print print_mes
                #info_public(print_mes) 
                if cmp(address2[0],CLIENTIP)<0:
                    print "Lost recv data ip:" ,address2[0]
                    continue
                #while True:
                mre=re.compile(find_str)
                result = mre.search(REC)
                if result:
                    return True
                else:
                    count_tmp = count_tmp+1
                    if count_tmp <=3:
                        print_mes = "send msg "  + MSG
                        print print_mes
                        info_public(print_mes)     
                        #print "count %d send this mes" %count_tmp
                        print_mes = "count"  + str(count_tmp) + " send this mes"
                        print print_mes
                        info_public(print_mes) 
                        REC = None
                        self.sock.sendto(MSG,address2)
                        #time.sleep(10)
                    else :
                        REC = None
                        #print "count %d  but not find" %count_tmp
                        print_mes = "count"  + str(count_tmp) + " but not find"
                        print print_mes
                        info_public(print_mes)
                        return False
            except:
                print_mes = "\nnot recv date"
                print print_mes
                info_public(print_mes)
        return True
                
        
    
    def client_send(self,MSG,Rec,RECSTOP):
        #-----------------------------------------------------------------------------
        # Name:        udp_class.py
        # param:     
        # explain:
        # Author:      gongke
        #
        # Created:     2013/01/15
        #-----------------------------------------------------------------------------
        
        try:
            self.sock.sendall(MSG)
        except:
            #print "send %s fail" %MSG
            print_mes = "send" + MSG + " fail"
            print print_mes
            info_public(print_mes)
            self.sock.close()
            return False
        try:
            Rec = self.sock.recv(2048)
            print_mes = "receive data: " + Rec
            print print_mes
            info_public(print_mes)
        except:
            return False
        return True
        
        
    def client_rec(self,Rec,RECSTOP):
        while 1:
            #print "Wait mesg from server:"
            print_mes = "Wait mesg from server:"
            print print_mes
            info_public(print_mes)
            try:
                REC,address = self.sock.recvfrom(2048)
                #print "recv data from",address,REC
                print_mes = "recv data from:" + address[0] +"  "+ REC
                print print_mes
                info_public(print_mes)
                info=os.popen(REC).read()
                self.sock.sendall(info)
            except:
                #print "Recv fail exit"
                print_mes = "Recv fail exit"
                print print_mes
                info_public(print_mes)
                #print "recv data from",address,REC
                print_mes = "recv data from:" + address[0]+"  " + REC
                print print_mes
                info_public(print_mes)
                self.sock.close()
                return False
        return True
            
    
    def disconnect(self):
        self.sock.close()
        
"""
if __name__ == "__main__":  
    #-----------------------------------------------------------------------------
    # Name:        instantiation of the ftp class
    # param:       
    # explain:     test the ftp class and fuction 
    # Author:      gongke
    #
    # Created:     2013/01/13
    #-----------------------------------------------------------------------------
    myudp_test = myudp("192.168.4.202",9999,True)
    myudp_test.client_connect()
    myudp_test.client_send("CMD=AP_ONLINE CASEID=500 APNUM=1024 RATE=50","11",1)
    #myudp_test.server_connect()
    #myudp_test.server_send("CMD=APONLINE CASEID=40001 APNUM=1024 RATE=100","11",1)
    myudp_test.disconnect()
"""
        
        
        