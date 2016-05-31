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
import os,os.path
import time
import re
import filecmp
from public import *
import StringIO
import shutil 

class file_Compare():
    def __init__(self,PATH1=None,PATH2=None,DEBUG_FLAG=True):
        self.File1 = PATH1
        self.File2 = PATH2
        self.Debugflag = DEBUG_FLAG
        self.find_file = None
        

    
    def file_exist(self,file):
        if os.path.isfile(file) ==False:
            msg = file  + "not exists"
            print msg
            info_public(msg)
            return False
        else:
            return True
    
    def file_rm(self,file):
        if self.file_exist(file)==True:
            os.remove(file)
        return True
            
    def find_str(self,file,str1 = 'Only in',str2 = 'Differing files'):
        file_object = open(file,"r")
        textlist = file_object.readlines()
        file_object.close()
        result = True
        for line in textlist:
            print line
            info_public(line)
            if str1 in line :
                result = False
                continue
            if str2 in line:
                result = False
                continue
        return result
        
    def bak_file(self,file,path):
        if self.file_exist(file)==False:
            msg = file + '  is not exist'
            info_public(msg )
            return False
        if self.path_exist(path) ==False:
            msg = path + '  is not exist'
            info_public(msg)
            return False
        filepath = os.path.dirname(file)
        tmp_list = filepath.split('\\')
        del tmp_list[0]
        str_t ='__'.join(tmp_list)
        str_t=os.path.abspath(path) + '\\' + str_t
        if os.path.exists(str_t)==False:
            os.mkdir(str_t)  
        str_t1=str_t+'\\'+os.path.basename(file)+'__bak'
        shutil.copy(file,str_t1)
        
        
            
        
    def stdout_file(self,path1,path2):
        oldStdout = None
        logfile = None
        x = filecmp.dircmp(path1,path2)
        path1 = os.path.abspath(sys.argv[0])
        filepath = os.path.dirname(path1)
        self.find_file = filepath  + "\\find_file.log"
        try:  
            logfile = open( self.find_file,'w+')
            oldStdout = sys.stdout  
            sys.stdout = logfile
            x.report_full_closure()
        finally:  
            if logfile:  
                logfile.close()  
                if oldStdout:  
                    sys.stdout = oldStdout  
        result = self.find_str(self.find_file)
        return result
        
    def path_exist(self,path):
        if os.path.exists(path) ==False:
            msg = path  + "not exists"
            print msg
            info_public(msg)
            return False
        
    
    def path_cmp(self,PATH1,PATH2):
        self.File1 = PATH1
        self.File2 = PATH2
        if self.path_exist(self.File1)==False:
            return False
        if self.path_exist(self.File2)==False:
            return False
        #filecmp.dircmp(self.File1,self.File2)
        result = self.stdout_file(self.File1,self.File2)
        return result
        
    
    def mk_dir(self,path):
        result = True
        path_p = os.path.dirname(path)
        title = path.split('\\')[-1]
        result = self.path_exist(path_p)
        if result ==False:
            return result
        new_path = os.path.join(path_p, title)
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
            os.chdir(path)
        return result
        
    def file_cmp_print(self,file1,file2):
        self.File1 = file1
        self.File2 = file2
        if self.file_exist(self.File1)==False:
            return False
        if self.file_exist(self.File2)==False:
            return False
        result = filecmp.cmp(self.File1,self.File2)
        if result ==False:
            msg = self.File1 + ' ,' + self.File2 + ': Differing'
            print msg
            info_public(msg)
        return result
    
    def file_cmp(self,file1,file2):
        self.File1 = file1
        self.File2 = file2
        if self.file_exist(self.File1)==False:
            return False
        if self.file_exist(self.File2)==False:
            return False
        result = filecmp.cmp(self.File1,self.File2)
        if result:
            msg = self.File1 + ' ,' + self.File2 + ': Identical'
            print msg
            info_public(msg)
        else:
            msg = self.File1 + ' ,' + self.File2 + ': Differing'
            print msg
            info_public(msg)
        return result
'''
if __name__ == "__main__":  
    f1 = 'E:\\Simu_server\\all_ac\\sta_26'
    f2 = 'E:\\sta_26'
    test = file_cmpo()
    test.path_cmp(f1,f2)
'''
        