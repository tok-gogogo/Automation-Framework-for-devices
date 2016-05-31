##-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        apply_alc .py
# Purpose:     apply_alc of users
#
# Author:      gongke
#
# Created:     2014/06/19
# RCS-ID:      $Id: apply_acl.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
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
from stc_load_op import *
import telnet_class 
from telnet_class import *

class acl_apply():
    def get_return(self,SENDSTR,WAITSTR,FINDSTR_str_T,A_TIMEOUT='1',Multi_FLAG='1',NUM='3',RESENDFLAG='True'):
        tmp_num = 1
        TIMEOUT = string.atoi(A_TIMEOUT)
        num = string.atoi(NUM)
        FINDSTR = self.tn1.Mult_find_str(FINDSTR_str_T)
        info_all = self.tn1.send_keys_reinfo_new(SENDSTR,WAITSTR,TIMEOUT,num,FINDSTR,Multi_FLAG)
        
        return info_all

    def apply_profile(self,filename,ftp_ip,user_name,user_password,config_file,olt_ip):
    #-----------------------------------------------------------------------------
    # Name:        apply_acl
    # param:      
    # explain:     
    # Author:      gongke
    #
    # Created:     2014/06/19
    #-----------------------------------------------------------------------------

        #t_stc=StcloadOP()
        #t_stc.SetTestcenterRun(filepath,sheetname,FlowName)
        
    
    #read_ini()
    
        #t_stc=StcloadOP()          
        #t_stc.SetTestcenterRun("D:\ACL_TEST\load_testcenter.xls","Load_Test1","Load_Test1")
    #abs_config_file = os.path.abspath(config_file)
    #read_ini()
 
         
        telnet_ip = olt_ip
        self.tn1= myTelnet(telnet_ip,'23',"catapult","catapult",'1') 
        self.tn1.open()
        self.tn1.mycommand("admin",":",'1')
        self.tn1.mycommand("admin",":",'1')
        self.tn1.mycommand("enable",">",'1')
        self.tn1.mycommand("conf ma","#",'1')
        i = 0
       
        file_list = filename.split(' ')

        while i <len(file_list):
            command = "ftp" +' '+ ftp_ip +' '+ "get" +' '+ user_name +' '+ user_password+' ' + "flash:/" + file_list[i] + ' ' + file_list[i]
            self.tn1.mycommand(command,")#",'1')  
            i=i+1
        self.tn1.sleep('3')
        self.tn1.mycommand("exit",")#",'1')
        self.tn1.mycommand("conf ter",")#",'1')
        
        #print file_list[3]
        self.tn1.sleep('3')
        j = 0
        #print "i = .....",i
        while j < i:
            im_command = "import flash:/" + file_list[j] + " to profile " +str(j+1) 
            self.tn1.mycommand(im_command,")#",'1')
            
            self.tn1.mycommand("y",')','1')
            j = j+1
            self.tn1.sleep('3')
        
    
        res=self.get_return("show chassis",")#","GEM4A",'10','0','2')
        print res

        t = res.split('\r\n')
        i = 0
        m = len(file_list)
        
        a=[]
        while i <len(t):
            s = t[i]
            re_result=re.findall("GEM4A",s)
            if re_result:
                k_list = s.split(' ')
                a.append(k_list[0])
            i=i+1
        profile_num = []
       
        for z in range(m):
            profile_num.append(str(z+1))

        for j in range(len(a)):
            for k in ['1','2','3','4']:
                port = a[j]+'/'+ k
                command = "int g "+port
                self.tn1.mycommand(command,")#",'1')
                for count in profile_num:
                    app = "apply-acl-profile " + count
                    self.tn1.mycommand(app,")#",'1')
                    find_com = "ge" + str(port)
                    self.tn1.find_command_Multi("show acl-applied-interface",")#",find_com,'10','0','1')
                    self.tn1.sleep('5')
                    for line in open(config_file):
                        line=line.strip('\n')
                        key = line.split(' ')
                        if port == key[0]:
                            if count == key[1]:
                                t_stc=StcloadOP()          
                                t_stc.SetTestcenterRun(key[2],key[3],key[4])

                            else:
                                continue
                        else:
                            continue
                self.tn1.mycommand("exit",")#",'1')
      
        ret=self.get_return("show inter epon onu su",")#","",'10','0','1')
        print ret

        g = ret.split('\r\n')
        i = 0
        b=[]
        while i <len(g):
            s = g[i]
            re_result=re.findall("Enable",s)
            if re_result:
                b_list = s.split(' ')
                b.append(b_list[0])
            i=i+1
        for j in range(len(b)):
            command = "int g "+b[j]
            self.tn1.mycommand(command,")#",'1')
            for count in profile_num:
                app = "apply-acl-profile " + count
                self.tn1.mycommand(app,")#",'1')
                find_com = "ge" + b[j]
                self.tn1.find_command_Multi("show acl-applied-interface",")#",find_com,'10','0','3')
                self.tn1.sleep('5')
                for line in open(config_file):
                    key = line.split(' ')
                    if b[j] == key[0]:
                        if count == key[1]:
                            t_stc=StcloadOP()          
                            t_stc.SetTestcenterRun(key[2],key[3],key[4])
                        else:
                            continue
                    else:
                        continue
            self.tn1.mycommand("exit","#",'1')
        self.tn1.mycommand("exit","#",'1')
                     

if __name__=='__main__':
    tn = acl_apply()
    tn.apply_profile("a.txt b.txt c.txt d.txt",'192.168.22.58',"admin","123456","D:\\ACL_TEST\\test.txt",'192.168.22.206')

    
    
    
   
