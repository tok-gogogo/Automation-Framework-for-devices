#-*- coding: UTF-8 -*-  
import os
import re
import sys
from types import *
tmpr ='±¾µØÁ¬½Ó 3'
 
def get_mac(version_os ='English'):
    if os.name == 'nt':
        try:
            
            CmdLine = 'ipconfig /all'
            #CmdLine ='ÎïÀíµØÖ·.AA-BB-CC-DD-EE-AA'
            r = os.popen(CmdLine).read()
            print r
            print 'find:',re.findall('ÎÞÏßÍøÂçÁ¬½Ó',r)[0].decode('gbk')
            
            print '*******'
            if r:
                if version_os=='English':
                    L = re.findall('Physical Address.*?([0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2})', r)
                else:
                    #print 'tmpr:',tmpr 
                    #print r
                    #print 're:',re.findall(tmpr,r)
                    L = re.findall('ÎïÀíµØÖ·.*?([0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2})', r)
                    print L
                return L
        except:
            pass
        
    elif os.name == "posix":
        try:
            ret = ''
            CmdLine = 'ifconfig'
            r = os.popen(CmdLine).read()
            if r:
                L = re.findall('HWaddr.*?([0-9,A-F]{2}:[0-9,A-F]{2}:[0-9,A-F]{2}:[0-9,A-F]{2}:[0-9,A-F]{2}:[0-9,A-F]{2})', r)
                return L
        except:
            pass
    else:
        pass
    return None
if __name__=='__main__':
    get_mac('English')