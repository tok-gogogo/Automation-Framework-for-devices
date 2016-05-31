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
from win_exec import *
from public import *
from rw_Excel_FLOW import *
from wtResult import clsWtResult
from public import *
from file_replay_class  import * 
from rssid import *
from win_GUI import *
from ctrl_waveQoE import *

from ctrl_omnipeek import *
from ctrl_pingtest import *

import sys
sys.setdefaultencoding("utf-8")

DEFAULTTIMEOUT = 20 
KEY_TIME_FORMAT = "%Y%m%d_%H%M%S"
reload(sys)
sys.setdefaultencoding("utf-8")

class simu_udp:
    def __init__(self,HOST=None,PORT='9999',DEBUG_FLAG='1'):
        
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
        self.sock.settimeout(DEFAULTTIMEOUT)
        self.dic_client={"Ac_web_mode":1,"Ac_upgrade_mode":2,"cmd_mode":3,"exec_mode":4,"M500_result":5,"M500_over":6,"M500_CMD":12,"START OK":7,"rssid":8,'winGUI':9,'waveQoE':10,'omnipeek':11,'pingtest':14,'OLT_Update':16}
        self.dic_wingui ={"wireshark_Start":1}
        self.omnipeekDic ={'omnipeek_test':1}
        self.pingtestDic ={'ping_test':1}
        
        self.myACWeb = Class_RW_Excel()
        
        self.caseResult = clsWtResult()
        self.datafile = 'E:\\Simu_server\\performance\\result\\test_result.txt'
        self.file_result_path = 'E:\\Simu_server\\performance\\result'
        self_result_file  = ''
        self.Acversion = 'TEST_AC_V'
        self.test_result_path = ''
        self.all_result_filename=''
        self.dstRst_result_total = {"Result":"OK","TotalNum":"0","DoneNum":"0","NotDoneNum":"0","OKNum":"0","NGNum":"0","Rate":"0%"}
        self.dstReport_result_total = {"No":"","Result":"","ScriptName":"","ScriptRestName":""}
        self.result_file = ''
        self.First_Flag = True
        self.runline = 0 
        self.rssid = ssid()
        #self.wingui = win_gui()
        self.M500_IP=''
        self.M500_PATH='AC_TEST_1022'
        self.M500_Launch='ceshibu_1.lch'
        self.M500_Jiaob=''
        self.errorNG = ''
        self.test_omnipeek = omnipeek()
        self.wingui = win_gui()
        self.test_pingtest = pingtest()
        #self.total_case =0
        
    def server_connect(self):
        try:
            self.sock.connect((self.host,self.port))
        except:
            print_mes = "connect the sta: " +self.host +" fail"
            print 'udp_new server_connect ',print_mes
            info_public(print_mes)
            self.sock.close()
            return False
        
        self_result_file = self.caseResult.funWtResultHead(self.file_result_path,self.Acversion ,self.datafile)
        
        print_mes = "connect the sta :" +self.host +" success"
        print 'udp_new server_connect ' ,print_mes 
        info_public(print_mes)
        return True

    def sleep(self,TIME):
        int_time = string.atoi(TIME)
        #print "ftp sleep ",int_time
        time.sleep(int_time)
        return True
    
    def client_connect(self):
        try:
            #self.sock.bind((self.host,self.port))
            self.sock.bind(("",self.port))
        except:
            
            print_mes = "bind " +self.host + " fail"
            print 'udp_new client_connect ',print_mes
            info_public(print_mes)
            self.sock.close()
            return False
        print_mes = "bind " +self.host + " success"
        print 'udp_new client_connect ',print_mes
        info_public(print_mes)
        return True
    
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
    
    def server_send(self,MSG,Client_FLAG,CLIENTIP,PORT_STR='9999',RECSTOP='',find_str='',count_m = '3',time_sleep='10'):
        print 'find_str:',find_str
        count_total = string.atoi(count_m)
        sleep_m =  string.atoi(time_sleep)
        MSG = MSG + ',' + Client_FLAG
        PORT=string.atoi(PORT_STR)
        address2=(CLIENTIP,PORT)
        count_tmp=0 
        FirstFlag = False
        REC = None
        self.sock.settimeout(sleep_m + DEFAULTTIMEOUT)
        while True:
            if count_tmp>count_total:
                print_mes = "this "+ find_str + " not find in the "
                print print_mes
                info_public(print_mes)
                return False
            
            if count_tmp==0:
                self.sock.sendto(MSG,address2)
                count_tmp = count_tmp + 1
            time.sleep(2)
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
                time.sleep(5)
                count_tmp = count_tmp +1
                print "*********************"
                self.sock.sendto(MSG,address2)
                continue
            
            print 'CLIENTIP,address2',CLIENTIP,address2, 'find_str is :',find_str
            if cmp(address2[0],CLIENTIP)<0:
                print "Lost recv data ip:" ,address2[0]
                print "I want to get the ip:",CLIENTIP
                #time.sleep(10)
                continue
            
            if REC:
                
                mre=re.compile(find_str)
                result = mre.search(REC)
                print 'REC',REC, 'find_str :',find_str,'result :',result
                if result:
                    print '**************1return True***************'
                    self.sock.settimeout( DEFAULTTIMEOUT)
                    print '**************1return True***************'
                    return True
            print '**************1time***************'
            print_mes = "send msg "  + MSG
            print_mes = print_mes + "count :" + str(count_tmp)
            print print_mes
            info_public(print_mes)
            self.sock.sendto(MSG,address2)
            count_tmp = count_tmp + 1
        return True
    
    def cmd_mode(self,REC):
        info = os.popen(REC).read()
        print info
        return info
        
    def Ac_web_mode(self,REC):
        
        path1 = os.path.abspath(sys.argv[0])
        filepath = os.path.dirname(path1)
        filename = filepath + "\\WebPages_Flow.xls"
        #file_exec = filepath + "\\rw_Excel_FLOW.exe" + " " + filename
        #print filename
        
        #do_exec = do_win_exec(file_exec)
        #do_exec.sub_ac_upgrade_exec()
        #info = do_exec.result()
        print 'Ac_web_mode,fuction'
        re_flag = 1
        try:
            info = self.myACWeb.setWebPage(filename,"PORTAL","CAOFF")
        except Exception ,exc_str:
            log_print(exc_str)
            re_flag =0 
            kill_program('iexplore.exe','Explorer')
            return re_flag
        error ='True'
        if info ==False:
            try:
                error = self.myACWeb.GetErrorInfo()
                re_flag = 0
            except Exception ,exc_str:
                log_print(exc_str)
                re_flag = 0
        print 'Ac_web_mode,fuction error:',error,re_flag
        kill_program('iexplore.exe','Explorer')
        return re_flag
    
    def Getfindpath(self,path,findstr=''):
        list_path = path.split('\\')
        parentpath = ''
        for i in range(len(list_path)):
            if i==0:
                parentpath=list_path[i]
            else:
                parentpath = parentpath + '\\'+list_path[i]
            if len(findstr)==0:
                continue
            if list_path[i].find(findstr)>-1:
                break
        #print parentpath
        return parentpath   
        
        
    def Getpath(self,path,path_i=0):
        list_path = path.split('\\')
        parentpath = ''
        for i in range(len(list_path)):
            if i==0:
                parentpath=list_path[i]
            else:
                parentpath = parentpath + '\\'+list_path[i]
            if path_i==0:
                continue
            if i== (len(list_path) - path_i):
                break
        #print parentpath
        return parentpath   
    
    
    
    def Ac_upgrade_mode(self,REC):
        info = 'start fail'
        pid_testserver = 'Testcase_exec.exe'
        
        '''
        kill_program(pid_testserver,pid_testserver)
        '''
        self.write_file_serv_r(REC)
        if self.Read_conf_Bamboo()=='1':
            kill_program(pid_testserver,pid_testserver)
        else:
            REC_read= 'wmic process where caption="'+pid_testserver+'" get caption,commandline /value'
            print_mes = os.popen(REC_read).read()
            log_print(print_mes)
            if print_mes.find(pid_testserver)>-1:
                info =' start ok , but other version test  is running .please wait soon '
                log_print(info)
                return info
            
        AC_str = REC.split(',')[0]
        Ac_version =  AC_str.split(' ')[0]
        Ac_script = AC_str.split(' ')[-1]
        path1 = os.path.abspath(sys.argv[0])
        findstr = 'Simu_'
        path2 = self.Getfindpath(path1,findstr)
        filepath = path2 + '\\dist\\Testcase_exec.exe' + ' '  +  Ac_version +  ' ' +Ac_script 
        print "filepath",filepath
        try:
            do_exec = do_win_exec(filepath)
            do_exec.sub_ac_upgrade_exec()
            info =do_exec.result()
        except Exception ,exc_str:
            log_print(exc_str)
        return info
  
    def Olt_upgrade_mode(self,REC):
        info = 'start fail'
        info = 'start fail'
        pid_testserver = 'python.exe'
        
        '''
        kill_program(pid_testserver,pid_testserver)
        '''
        self.write_file_serv_r(REC)
        if self.Read_conf_Bamboo()=='1':
            kill_program(pid_testserver,pid_testserver)
        else:
            REC_read= 'wmic process where caption="'+pid_testserver+'" get caption,commandline /value'
            print_mes = os.popen(REC_read).read()
            log_print(print_mes)
            if print_mes.find(pid_testserver)>-1:
                info =' start ok , but other version test  is running .please wait soon '
                log_print(info)
                return info
        print 'Olt_upgrade_mode REC:',REC
        AC_str = REC.split(',')[0]
        Ac_version =  AC_str.split(' ')[0]
        Ac_script = AC_str.split(' ')[-1]
        path1 = os.path.abspath(sys.argv[0])
        findstr = 'Simu_'
        path2 = self.Getfindpath(path1,findstr)
        filepath = path2 + '\\Testcase_exec.py' + ' '  +  Ac_version +  ' ' +Ac_script 
        print "filepath",filepath
        try:
            do_exec = do_win_exec(filepath)
            do_exec.sub_ac_upgrade_exec()
            info =do_exec.result()
        except Exception ,exc_str:
            log_print(exc_str)
        return info
        
    def exec_mode(self,REC):
        exec_str = REC.split(',')[0]
        #print exec_str
        info = 'start fail'
        try:
            do_exec = do_win_exec(exec_str)
            do_exec.sub_do_exe()
            info =do_exec.result()
        except Exception ,exc_str:
            log_print(exc_str)
        return info
    
    
    def mod_send_email(self,version =''):
        Plugin_name =[{'subject' : self.result_file, 'content' : '1abc'}]
        path1 = os.path.abspath(sys.argv[0])
        lotus_send(version,Plugin_name)
        return True
    
    def mod_file_email(self,flag='1'):
        print '*********** mod_file_email  fuction *********** \n'
        path1 = os.path.abspath(sys.argv[0])
        findstr = 'Simu_'
        path2 = Getfindpath(path1,findstr)
        filename = path2 +'\\auto_conf\\lotus.conf'
        new_path = 'c:\\auto_test_note'
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        new_filename = new_path + '\\lotus.conf'
        if file_exist(new_filename):
            os.remove(new_filename)
            
        file_object = open(filename,"r")
        textlist = file_object.readlines()
        file_object.close()
        
        fp = open(new_filename, 'a')
        str = 'send_email_Flag'
        #print textlist
        for line in textlist:
            
            if line.find(str)>-1:
                print '############line:#########\n',line
                tmp = str +'$  '+flag
                fp.write(tmp)
                print '############tmp:#########\n',tmp
                continue
            else:
                fp.write(line)   
        fp.close()
        
        print '*********** mod_file_email  fuction ,path2 new_path*********** \n',path2,new_path
        file_Refresh(new_path,path2)
        file_object = open(new_filename,"r")
        textlist = file_object.readlines()
        file_object.close()
        print '*********** mod_file_email  fuction *********** \n',textlist
        return True
    
    def read_file(self,REC,filename):
        print 'read_file fuction REC ,filename',REC,filename
        file_object = open(filename,"r")
        textlist = file_object.readlines()
        file_object.close()
        line = ''
        #find_flag = False
        if self.runline> len(textlist):
            print 'find the end send email  ***********************************************************************\n'
            self.mod_file_email('1')
            time.sleep(10)
            self.mod_send_email()
            sys.exit(0) 
        total = 0
        for line in textlist:
            if total== self.runline :
                self.runline = self.runline +1
                print 'send performance :' ,line,REC,self.runline,len(textlist),filename
                return line
            total = total + 1 
            
    '''
    mod by gongke 2013.06.01
    read_file_old is the read_file mod befor 
   
    def read_file_old(self,REC,filename):
        print 'read_file fuction REC ,filename',REC,filename
        file_object = open(filename,"r")
        textlist = file_object.readlines()
        file_object.close()
        line = ''
        find_flag = False
        #total = self.runline 
       
        for line in textlist:
            print '***********************************************************************\n'
            print 'line,REC,total,len(textlist),filename:' ,line,REC,self.runline,len(textlist),filename
            if total == self.runline:
                self.runline = self.runline + 1 
                return line
            
            if self.runline> len(textlist):
                print 'here  ***********************************************************************\n'
                self.mod_file_email('1')
                time.sleep(10)
                self.mod_send_email()
                sys.exit(0) 
                    
            if find_flag ==True:
                print 'line,REC:', line,REC
                break
            if len(REC)>0:
                if REC in line:
                    print 'line,REC:', line,REC
                    find_flag = True
                    continue
                
            else:
                find_flag = True
                break
        if find_flag ==False:
            #self.mod_send_email()
            #sys.exit(0)
            line = ''
        return line
    '''
    
    
    
    def Read_conf_Bamboo_REC(self,path=''):
        path1 = os.path.abspath(sys.argv[0])
        findstr = 'Simu_'
        path2 = self.Getfindpath(path1,findstr)
        filename = path2  + '\\tmp_date\\tmp_Bamboo_rec.txt'
        
        return True
    
    def kill_pid_telnet(self):
        path1 = os.path.abspath(sys.argv[0])
        findstr = 'Simu_'
        path2 = self.Getfindpath(path1,findstr)
        pid_name ='telnet_M500.exe'
        kill_program(pid_name,pid_name)
        
    def Read_conf_Bamboo(self,filename=''):
        path1 =  os.path.abspath(sys.argv[0])
        findstr = 'Simu_'
        path2 = self.Getfindpath(path1,findstr)
        file_name  = path2  +  '\\auto_conf\\Bamboo.conf'
        value = readfile(file_name,'Bamboo_Run_now','$')
        return value
            
    
    def write_file_serv_r(self,REC=''):
        path1 =  os.path.abspath(sys.argv[0])
        findstr = 'Simu_'
        path2 = self.Getfindpath(path1,findstr)
        file_name  = path2  + '\\tmp_date\\tmp_Bamboo_rec.txt'
        while True:
            if os.path.isfile(file_name)==True:
                break
        fp = open(file_name, 'a') 
        msg = REC+ '\n'
        fp.write(msg)
        fp.close()
        return True
    
    def write_file(self,Flag = 'NG',REC='',filename='E:\\Simu_server\\performance\\result\\result.txt'):
        if len(REC) == 0 :
            return False
        #tmp_path = REC.
        #tmp_list  =  REC.split(',')
        path1 = os.path.abspath(sys.argv[0])
        findstr = 'Simu_'
        path2 = self.Getfindpath(path1,findstr)
        self.result_file = path2 + '\\performance\\result\\result.txt'
        filename = self.result_file
        fp = open(filename, 'a') 
        strTime = time.strftime(KEY_TIME_FORMAT)
        Flag =''
        if self.findpath_fromREC(REC,'fail') =='0':
            Flag =='OK'
        else:
            Flag='NG'
        tmp = '\n' +strTime + '      result:' +Flag + '     '+REC 
        fp.write(tmp)
        fp.close()
        return True
    
    def findpath_fromREC(self,REC,findstr):
        path_find=''
        list = REC.split(',')[0].split(' ')
        for i in  list:
            print i
            if findstr in i:
                path_find = i.split('=')[-1].strip()
        print path_find
        return path_find
    
    def send_next_performance(self,REC,M500_IP='192.168.21.131',M500_PORT='9999',RECSTOP ='1',find_strt='START OK',FLAG='OK',timeout= '180',path1_p='E:\\Simu_server\\performance\\ac_Test\\performance.txt'):
        self.write_file(FLAG,REC)
        if len(self.M500_IP)>0:
            M500_IP = self.M500_IP
        else:
            self.M500_IP = M500_IP
        print 'send_next_performance fuction'
        info =''
        path1 = os.path.abspath(sys.argv[0])
        findstr = 'Simu_'
        path2 = self.Getfindpath(path1,findstr)
        pid_name ='telnet_M500.exe'
        kill_program(pid_name,pid_name)
        #print '\n********** self.M500_Launch: **********\n',self.M500_Launch
        telnet_M500_path =  path2 +'\\Simu_server_client_ok\\dist\\telnet_M500.exe  ' +  M500_IP +'   ' + self.M500_PATH + '   '  +  self.M500_Launch
        print '\n********** self.M500_Launch: **********\n',telnet_M500_path
        log_print(telnet_M500_path) 
        self.do_exec_op(telnet_M500_path,0)
        time.sleep(string.atoi(timeout))
        performance_script = path2 + '\\performance\\ac_Test\\performance.txt'
        if len(REC)==0:
                performance_script = path1_p
        else:
            performance_script = self.findpath_fromREC(REC,'PATH1')
        print 'send_next_performance fuction send_next_performance111:',performance_script
        if file_exist(performance_script) ==False:
            print '**************performance_script, not find ***************'
            sys.exit(0)
        MSG = self.read_file(REC.split(',')[0].split(' ')[0].split('=')[-1].strip() ,performance_script)
        
        print '222222send find_str222222',find_strt
        if len(MSG):
            self.server_send(MSG,'M500',M500_IP,M500_PORT,RECSTOP,find_strt)
        return info
    
    def do_exec_op(self,filepath,flag_exec,M500_IP='192.168.21.130',M500_PORT='9999'):
        if len(self.M500_IP)>0:
            M500_IP = self.M500_IP
        else:
            self.M500_IP = M500_IP
        print 'do_exec_op fuction'
        do_exec = do_win_exec(filepath)
        if flag_exec==1:
            do_exec.sub_return_exec()
        else:
            do_exec.sub_do_exe()
        return True
        
    def telnet_ac(self,REC,FLAG='NG',Ac_version='Ac_version',Ac_script='E:\\Simu_server\\performance\\clear_ac'):
        #self.Ac_upgrade_mode(REC)
        
        #self.write_file(FLAG,REC)
        print 'telnet_ac  fuction'
        path1 = os.path.abspath(sys.argv[0])
        findstr = 'Simu_'
        Ac_version = 'performance_test'
        path2 = self.Getfindpath(path1,findstr)
        Ac_script = path2 + '\\performance\\clear_ac'
        if len(REC):
            Ac_script = self.findpath_fromREC(REC,'PATH2')
        print 'telnet_ac fuction Ac_script:',Ac_script
        
        
        if path_exist(Ac_script) ==False:
            print 'not find exist'
            sys.exit(0)
            
        filepath = path2 + '\\dist\\Testcase_exec.exe' + ' '  +  Ac_version +  ' ' +Ac_script + ' ' + '1'
        print "telnet_ac filepath:",filepath
        self.do_exec_op(filepath,1)
        info ='CLEAR=OK'
        return info
    
    
    def dic_rec_mes(self,REC):
        #key =REC.split(',')[1]
        print 'dic_rec_mes fuction ',REC
       
        key =REC.split(',')[-1].strip()
        portal_flag = 0
        print key 
        op_flag = 0
        info ='Flase'
        if self.dic_client.has_key(key):
            print 'dic_rec_mes  find',info
            op_flag = self.dic_client[key]
            print 'dic_rec_mes  find,op_flag',op_flag
        else:
            info = 'Flase'
            #print 'dic_rec_mes fail',info
            return info
        print 'dic_rec_mes here'
        if op_flag == 1:
            portal_flag = self.Ac_web_mode(REC.split(',')[0])
            if portal_flag ==1:
                info = 'True'
            else:
                info = 'Flase'
        elif op_flag == 2:
            info = self.Ac_upgrade_mode(REC)
        elif op_flag == 3:
            info= self.cmd_mode(REC.split(',')[0])  
        elif op_flag == 4 :
            info = self.exec_mode(REC)
        elif op_flag == 5 :
            self.mod_file_email('0')
            #info = self.telnet_ac(REC)
            info = ''
            self.write_file(FLAG,REC)
        elif op_flag == 6 :
            self.mod_file_email('0')
            info =self.send_next_performance(REC)
        elif op_flag == 7 :
            info =''
        elif op_flag == 8 :
            info =self.rssid_mode(REC)
        elif op_flag == 9 :
            info =self.winGui_mode(REC)
        elif op_flag == 10 :
            info =self.waveQOE_mode(REC)
        elif op_flag == 11 :
            info =self.omnipeek_mode(REC)
        elif op_flag==12:
            self.mod_file_email('0')
            info = self.telnet_ac(REC)
            info = REC.split(',')[0]
        elif op_flag ==13:
            info=''
        elif op_flag == 14 :
            info =self.pingtest_mode(REC)
        elif op_flag == 16 :
            info = self.Olt_upgrade_mode(REC)
        else:
            info = 'Flase'
        print 'dic_rec_mes info:',info
        return info
    
    
    def winGui_param_wiresharkstart(self,list):
        tmplist = []
        tmp = 0
        str = ''
        for i in list:
            if tmp <3:
                tmplist.append(i)
            else:
                str = str + i 
            tmp = tmp + 1 
        tmplist.append(str)
        return tmplist
    
    def winGui_param(self,key,param):
        tmplist = []
        if self.dic_wingui[key] == 1:
            tmplist = self.winGui_param_wiresharkstart(param)
        return tmplist
       
    def omnipeek_mode(self,REC):

        op_tuple=[]
        tmp_list=[]
        list_tmp=[]
        
        for x in REC.split(',')[0].split(' '):
            if len(x)==0:
                continue
            tmp_list.append(x)
            
        str_lin =''
        find_flag = False
        for i in range(len(tmp_list) ):
            if i ==0:
                continue
            if find_flag == False:
                if str_lin=='':
                    str_lin = tmp_list[i] 
                else:
                    str_lin = str_lin + ' '+tmp_list[i]
                if str_lin.find('.exe')>-1:
                    find_flag = True
            if find_flag == True:
                if len(list_tmp)==0:
                    list_tmp.append(str_lin)
                else:
                    list_tmp.append(tmp_list[i])
        
        op_tuple.append(tmp_list[0])
        op_tuple.append(list_tmp)
        key = op_tuple[0]
        mine_omnipeek ="self.test_omnipeek." + op_tuple[0]
        mine_tuple = tuple(op_tuple[1])
        try :
            result =apply(eval(mine_omnipeek),mine_tuple)
        except Exception ,exc_str:
            log_print(exc_str)
            result =False
        if result==True:
            return 'True'
        else:
            return 'False'
        
    def pingtest_mode(self,REC):
        result = False
        result = ''
        op_tuple=[]
        tmp_list=[]
        list_tmp=[]
        print '********fuction pingtest_mode ***********',REC
        for x in REC.split(',')[0].split(' '):
            if len(x)==0:
                continue
            tmp_list.append(x)
        
        for i in range(len(tmp_list) ):
            if i ==0:
                continue
            list_tmp.append(tmp_list[i])
         
        op_tuple.append(tmp_list[0])
        op_tuple.append(list_tmp)
        key = op_tuple[0]
        mine_pingtest ="self.test_pingtest." + op_tuple[0]
        mine_tuple = tuple(op_tuple[1])
        try :
            result =apply(eval(mine_pingtest),mine_tuple)
        except Exception ,exc_str:
            log_print(exc_str)
            result =False
        if result==True:
            return 'True'
        else:
            return 'False' 
    
    def waveQOE_mode(self,REC):
        result = False
        result = ''
        op_tuple=[]
        tmp_list=[]
        list_tmp=[]
        print '********fuction waveQOE_mode ***********',REC
        for x in REC.split(',')[0].split(' '):
            if len(x)==0:
                continue
            tmp_list.append(x)
        #print '********fuction waveQOE_mode  tmp_list***********',tmp_list
        for i in range(len(tmp_list) ):
            if i ==0:
                continue
            list_tmp.append(tmp_list[i])
        #print '********fuction waveQOE_mode  list_tmp***********',list_tmp   
        op_tuple.append(tmp_list[0])
        op_tuple.append(list_tmp)
        print '********fuction waveQOE_mode  op_tuple***********',op_tuple
        print op_tuple
        key = op_tuple[0]
        self.waveQoE = ctrl_waveQoE()
        mine_waveQoE ="self.waveQoE." + op_tuple[0]
        mine_tuple = tuple(op_tuple[1])
        try :
            result =apply(eval(mine_waveQoE),mine_tuple)
        except Exception ,exc_str:
            log_print(exc_str)
            result =False
        print 'rssid_mode result:',result
        if result==True:
            return 'True'
        else:
            return 'False'
        
    def winGui_mode(self,REC):
        print '********fuction winGui_mode ***********',REC
        op_tuple=[]
        tmp_list=[]
        list_tmp=[]
        for x in REC.split(',')[0].split(' '):
            if len(x)==0:
                continue
            tmp_list.append(x)
            
        str_lin =''
        find_flag = False
        for i in range(len(tmp_list) ):
            if i ==0:
                continue
            if find_flag == False:
                if str_lin=='':
                    str_lin = tmp_list[i] 
                else:
                    str_lin = str_lin + ' '+tmp_list[i]
                if str_lin.find('.exe')>-1:
                    find_flag = True
            if find_flag == True:
                if len(list_tmp)==0:
                    list_tmp.append(str_lin)
                else:
                    list_tmp.append(tmp_list[i])
        
        op_tuple.append(tmp_list[0])
        if self.dic_wingui.has_key(tmp_list[0]):
            list_param_gui=[]
            list_param_gui = self.winGui_param(tmp_list[0],list_tmp)
            op_tuple.append(list_param_gui)
        else:
            op_tuple.append(list_tmp)
        self.wingui = win_gui()
        print 'WinGui:',op_tuple
        mine_WinGui ="self.wingui." + op_tuple[0]
        mine_tuple = tuple(op_tuple[1])
        try :
            result =apply(eval(mine_WinGui),mine_tuple)
        except Exception ,exc_str:
            log_print(exc_str)
            msg = 'Error: ' + mine_WinGui  + ' is Exception'
            return msg
        '''
        if op_tuple[0].find('wireshark_stop')>-1:
            self.wingui = None
        '''
        if result==True:
            return 'True'
        else:
            return 'False'
        
    def rssid_mode(self,REC):
        print '********fuction rssid_mode ***********'
        result = ''
        op_tuple=[]
        tmp_list=[]
        list_tmp=[]
        print '********fuction rssid_mode ***********',REC
        for x in REC.split(',')[0].split(' '):
            if len(x)==0:
                continue
            tmp_list.append(x)
        print '********fuction rssid_mode  tmp_list***********',tmp_list
        for i in range(len(tmp_list) ):
            if i ==0:
                continue
            list_tmp.append(tmp_list[i])
        print '********fuction rssid_mode  list_tmp***********',list_tmp   
        op_tuple.append(tmp_list[0])
        op_tuple.append(list_tmp)
        print '********fuction rssid_mode  op_tuple***********',op_tuple
        print op_tuple
        key = op_tuple[0]
        mine_ssid ="self.rssid." + op_tuple[0]
        mine_tuple = tuple(op_tuple[1])
        result =apply(eval(mine_ssid),mine_tuple)
        
        print 'rssid_mode result:',result
        if result==True:
            return 'True'
        else:
            self.errorNG = ''
            self.errorNG = self.rssid.GetErrorInfo()
            msg = '######################ssid op_error start #############'
            log_print(msg)
            log_print(self.errorNG)
            msg = '######################ssid op_error end#############'
            log_print(msg)
            return self.rssid.GetErrorInfo()
    
    def disconnect(self):
        self.sock.close()
        return True
    
    def client_send(self,MSG,serverIP,find_str,count_tmp ='3',time_out='10'):
        
        sleep_m = string.atoi(time_out)
        count_total = string.atoi(count_tmp)
        address2=(serverIP,9999)
        self.sock.sendto(MSG,address2)
        print_mes = "send date"  + address2[0] +"," + MSG
        print print_mes
        info_public(print_mes)
        count_tmp = 1
        while True:
            if count_tmp>count_total:
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
                time.sleep(sleep_m)
                count_tmp = count_tmp +1
                print "*********************"
                self.sock.sendto(MSG,address2)
                continue
            if cmp(address2[0],serverIP)<0:
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
            #self.sock.sendto(MSG,address2)
            count_tmp = count_tmp + 1
        return True
            
        
    def client_rec(self,RECSTOP):
        REC = None
        self.sock.settimeout(DEFAULTTIMEOUT)
        address2=("127.0.0.1",9999)
        print "Wait mesg from server:"
        while True:
            try:
                REC,address2 = self.sock.recvfrom(2048)
                print_mes = "recv data from "  + address2[0] +"," + REC
                print print_mes
                info_public(print_mes)
            except:
                REC=None
                #print ".....receive fail ......."
                continue
            if not REC:
                continue
            #info = os.popen(REC).read()
            info= self.dic_rec_mes(REC)
            #print 'udp_new client_rec info:',info
            if len(info)>0:
                self.sock.sendto(info,address2)
            print info
            REC=None
        return True

if __name__ == "__main__":
    
    HOST='192.168.22.169'
    #HOST = '192.168.11.28'
    PORT = '9999'
    version='AC_TEST'
    Testpath='E:\\test\\sta_26'
    #sendflag='Ac_upgrade_mode'
    sendflag='OLT_Update'
    find_str ='start ok'
    RECSTOP = '1'
    myudp_client = simu_udp(HOST,PORT,'1')
    #myudp_client.client_connect()
    send_str = 'D:\\version\\opm8000_03.00.00.12.stz@@CYC8000_03.00.00.12 E:\\test_case_auto\\Debug1'
    myudp_client.server_send(send_str,sendflag,HOST,PORT,'2',find_str,'1')
    myudp_client.disconnect()
    #client_send
    '''
    #send_str = version + '  ' + Testpath
    send_str  =  'CMD=AP_ONLINE  NODE=1 RATE=100 SCALE=5 PATH1=E:\Simu_server\performance\ac_Test\ÄãºÃperformance.txt PATH2=E:\Simu_server\performance\clear_sta_ac'
    
    myudp_client.server_send(send_str,sendflag,HOST,PORT,'2',find_str,'1')
    find_str = 'Simu_'
    #myudp_client.send_next_performance('',HOST,PORT,RECSTOP )
    '''
    