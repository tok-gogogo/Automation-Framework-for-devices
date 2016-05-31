#-----------------------------------------------------------------------------
# Name:        ftp_class.py
# Purpose:     
#
# Author:      gongke
#
# Created:     2013/01/13
# RCS-ID:      $Id: ftp_class.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------

import time   
import sys
import ftplib 
import os
import string
import socket
from public import *
reload(sys)
sys.setdefaultencoding("utf-8")

class myftp:
    def __init__(self,HOST=None,PORT='21',USER="root",PASSWD="fitap^_^",DEBUG_FLAG='1',TIMEOUT='99999'):
        #-----------------------------------------------------------------------------
        # Name:        init fuction
        # param:       HOST:host name PORT:PORT  
        # explain:     initialize the ftp class
        # Author:      gongke
        #
        # Created:     2013/01/13
        #-----------------------------------------------------------------------------
        self.host=HOST
        self.port=PORT
        self.user=USER
        self.passwd=PASSWD
        self.debugflag = string.atoi(DEBUG_FLAG)
        
        self.mftp=ftplib.FTP()
        
        self.timeout = string.atoi(TIMEOUT)
        socket.setdefaulttimeout(self.timeout)
        self.error_NG=''
        self.BUFFER_SIZE=1024
        
        
    def connect(self):
        #-----------------------------------------------------------------------------
        # Name:        connect fuction
        # param:       NONE 
        # explain:     connect ftp server
        # Author:      gongke
        #
        # Created:     2013/01/13
        #-----------------------------------------------------------------------------
        try:
            self.mftp.connect(self.host,self.port,self.timeout)
        except:
            #print "cann't ftp %s" %self.host
            print_mes = "cann't ftp  " +self.host 
            print print_mes
            info_public(print_mes)
            return False
        try:
            self.mftp.login(self.user,self.passwd)
        except ftplib.error_perm:
            #print "Cannot login this username :%s passwd:%s" %self.user %self.passwd
            print_mes = "Cannot login this username:  " +self.user   +" passwd:"+ self.passwd
            print print_mes
            info_public(print_mes)
            
            self.mftp.quit()
            return False
        self.mftp.set_pasv(1) 
        print_mes = self.mftp.getwelcome()
        print print_mes
        info_public(print_mes)
        #print self.mftp.getwelcome()
        return True
    
    def sleep(self,TIME):
        int_time = string.atoi(TIME)
        #print "ftp sleep ",int_time
        time.sleep(int_time)
        return True
        
    def cwd(self,path):
        #-----------------------------------------------------------------------------
        # Name:        cwd fuction
        # param:       path :cd to the path,please write absolute path
        # explain:     cd to this path
        # Author:      gongke
        #
        # Created:     2013/01/13
        #-----------------------------------------------------------------------------
        try:
            self.mftp.cwd(path)
        except ftplib.error_perm:
            #print "cannot cd to this path %s" %path
            print_mes = "cannot cd to this path  " +path 
            print print_mes
            info_public(print_mes)
            self.mftp.quit()
            return False
        #print "cd %s" %path
        print_mes = "cd  " +path 
        print print_mes
        info_public(print_mes)
        return True
    
    
    def find(self,filename,path):
        #-----------------------------------------------------------------------------
        # Name:        find fuction
        # param:       path :cd to the path,please write absolute path,filename:the filename when you want to find
        # explain:     find this filename in the path
        # Author:      gongke
        #
        # Created:     2013/01/13
        #-----------------------------------------------------------------------------
        if self.cwd(path) == False:
            #print "Cannot cd to this path"
            print_mes = "Cannot cd to this path" 
            print print_mes
            info_public(print_mes)
            self.mftp.quit()
            return False
        ftp_f_list=self.mftp.nlst()
        print ftp_f_list
        if filename in ftp_f_list:
            #print "find this filename:%s " %filename 
            print_mes = "find this filename "  + filename
            print print_mes
            info_public(print_mes)
            return True
        else:
            #print "cannot find this filename:%s " %filename 
            print_mes = "cannot find this filename "  + filename
            print print_mes
            info_public(print_mes)
            return False
        
    def upload_NoReplace(self,filepath):
        result = self.upload(filepath)
        return result
        
    def upload(self,filepath ):
        #-----------------------------------------------------------------------------
        # Name:        upload fuction
        # param:       filepath:the path and the filename the path please write absolute path
        # explain:     upload file to ftp server in the path whith the filename,upload by binary
        # Author:      gongke
        #
        # Created:     2013/01/13
        #-----------------------------------------------------------------------------
        if os.path.isfile(filepath) ==False:
            msg = filepath  + "not exists"
            print msg
            info_public(msg)
            return False
        os.chdir(os.path.dirname(filepath))
        f=open(filepath,"rb")
        file_name=os.path.split(filepath)[-1]
        try:
            self.mftp.storbinary("STOR %s"%file_name,f,self.BUFFER_SIZE)
            print_mes = "success upload the filename: "  + filepath
            print print_mes
            info_public(print_mes)
        except ftplib.error_perm:
            #print "upload the filename:%s fail" %filepath
            print_mes = "cannot upload the filename: "  + filepath
            print print_mes
            info_public(print_mes)
            return False
        #print "upload the filename:%s success" %filepath
        
        return True
    
    def download(self,localfile,remotefile):
        #-----------------------------------------------------------------------------
        # Name:        download fuction
        # param:       filename:download the filename,path:download the filename by this path please write absolute path
        # explain:     download file to ftp server in the path ,download by binary
        # Author:      gongke
        #
        # Created:     2013/01/13
        #-----------------------------------------------------------------------------
      
     
        
        
        
        filename = remotefile.split('/')[-1]
        path =''
        for i in  range( len (remotefile .split('/'))-1):
            path = path + remotefile .split('/')[i]+'/'
        print  '***************************************'
        print  'now pwd dir',filename,path
        print  '***************************************'
        
        if self.cwd(path)==False:
            #print "not find the path:%s"  %path
            print_mes = "not find the path: "  + path
            print print_mes
            info_public(print_mes)
            return False
        
        file_handler = open(localfile, 'wb')  
        
        try:
            self.mftp.retrbinary('RETR %s'%(filename), file_handler.write)  
        except ftplib.error_perm:
            #print "download the failename :%s fail " %filename
            print_mes = "fail download the failename: "  + remotefile
            print print_mes
            info_public(print_mes)
            return False
        file_handler.close()  
        print_mes = "success download the failename: "  + remotefile
        print print_mes
        info_public(print_mes)
        '''
        f=open(filename,"wb").write
        if self.cwd(path)==False:
            #print "not find the path:%s"  %path
            print_mes = "not find the path: "  + path
            print print_mes
            info_public(print_mes)
            return False
        if self.find(filename,path)==False:
            #print "not find this filename:%s in the path:%" %filename %path
            print_mes = "not find the path: "  + filename+"  ,"+path
            print print_mes
            info_public(print_mes)
        try:
            self.mftp.retrbinary("RETR %s"%filename,f,self.BUFFER_SIZE)
        except ftplib.error_perm:
            #print "download the failename :%s fail " %filename
            print_mes = "fail download the failename: "  + filename
            print print_mes
            info_public(print_mes)
            return False
        #print "download the failename :%s success " %filename
        print_mes = "success download the failename: "  + filename
        print print_mes
        info_public(print_mes)
        '''
        return True
    
    
    def disconnect(self):
        #-----------------------------------------------------------------------------
        # Name:        disconnect fuction
        # param:       NONE
        # explain:     diconnect ftp server
        # Author:      gongke
        #
        # Created:     2013/01/14
        #-----------------------------------------------------------------------------
        self.mftp.quit()
        return True
'''
if __name__ == "__main__":  
    #-----------------------------------------------------------------------------
    # Name:        instantiation of the ftp class
    # param:       
    # explain:     test the ftp class and fuction 
    # Author:      gongke
    #
    # Created:     2013/01/13
    #-----------------------------------------------------------------------------
    myftp_test = myftp("192.168.4.110",21,"root","fitap^_^",True,30)
    myftp_test.connect()
    #myftp_test.download("Patch_0111","/root")
    myftp_test.download("forward.conf","/icac/conf")
    #myftp_test.upload("E:\Simu_server\module1.py")
    myftp_test.disconnect()
'''

    
    
    
            
    
    