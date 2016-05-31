# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
# Name:        ctrVugen.py
# Purpose:     operate web page of "AC" by using Vugen of Loadrunner.
#   Vugen can execute script automate.
# Author:      <chensc>
#
# Created:     2013/01/22
# RCS-ID:      $Id: ctrVugen.py $
# Copyright:   zoom (c) 2006
# Licence:     <None>
#-----------------------------------------------------------------------------
#<1.0.1> add a parameter-TIMEOUTMAX_COVERPAGE wait time for wait HP COVER PAGE.
import win32api
import os
import win32gui
import win32con
import win32process
import time
import string

#error massage
ERROR_MSG_FILE_CHECK ='Error-AutoTestScenario.log file not exist.'
ERROR_MSG_VUGEN_CHECK ='Error-Vugen run error.Check Vugen whether exist,check script wheter exist.'
 

 

class LchVugen:
            
    def __init__(self):
        pass
            
    #-----------------------------------------------------------------------------
    # Name:        LaunchVugen
    # Purpose:     To launch Vugen. to ruan script. to close it when it fininsh.
    # Param:CommandLine-for launch Vugen.exe and script to execute setting for "AC"
    #       eg:ExePath='C:\\Program Files\\HP\\LoadRunner\\bin\\vugen.exe'
    #         ScriptPath='-TestPath C:\MyTest\MyTest.usr'
    #       FlagFileName-it is file path,for check the flag that writted by Vugen's script.
    #       eg:'c:\\AutoTestScenario.ini'
    #       TIMEOUTMAX,if vugen norespond,wait TIMEOUTMAX,default is 300 seconds.you can set it by use this param.
    # Author:      <chensc>
    # return value: (1,run vugen success; -1,run Vugen failed)
    # Created:     2013/01/22
    # RCS-ID:      $Id: ctrVugen.py $
    # Copyright:   (c) 2006
    # Licence:     <none>
    #-----------------------------------------------------------------------------
    def LaunchVugen(self,ExePath,ScriptPath,FlagFileName,my_TIMEOUTMAX_COVERPAGE = "10",my_TIMEOUTMAX = "8"):
        TIMEOUTMAX_COVERPAGE = string.atoi(my_TIMEOUTMAX_COVERPAGE)
        TIMEOUTMAX = string.atoi(my_TIMEOUTMAX)
        try:
            #launch          
            win32process.CreateProcess(ExePath,ScriptPath,None,None,0,win32process.CREATE_NO_WINDOW,None,None,win32process.STARTUPINFO())
          
            #wait 6 seconds for Vugen opened.
            time.sleep(10)
      
            #run
            #get windows class
            clss = 'VugenMainWindowClass'

            #find handle for the windows
            hwnd = win32gui.FindWindow(clss,None)
            print hwnd
            
            time.sleep(TIMEOUTMAX_COVERPAGE)
            #post VK_F5,to do run script
            print win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F5, 0)
            
            
            #loop to check Flag
            timeout =1
            ret = 0      
            while ret == 0:
                #check flag every 10 seconds            
                time.sleep(10)
                ret = self.CheckFlag(FlagFileName)
                #judge timeout
                if timeout == TIMEOUTMAX:#
                    ret = -1
                timeout = timeout + 1
                print  timeout                  
            time.sleep(1)   
            #ret is 1,means operate success,else failed.
            if ret == 1:
                win32api.SendMessage(hwnd,win32con.WM_CLOSE,0,0)
                print "ok"
                return 1
            else:
                win32api.SendMessage(hwnd,win32con.WM_CLOSE,0,0)
                print "ng"
                return -1
            
            print "NG"    
        except:
            print ERROR_MSG_VUGEN_CHECK

            
    #-----------------------------------------------------------------------------
    # Name:        CheckFlag
    # Purpose:     check flag that recoad at file. this flag be written by Vugen.
    # Param: FlagFileName-,it is file path,for check the flag that writted by Vugen's script.
    # Author:      <chensc>
    # return value:(-1,happen error.;1,script run finished.0 not finished.)
    # Created:     2013/01/22
    # RCS-ID:      $Id: ctrVugen.py $
    # Copyright:   (c) 2006
    # Licence:     <none>
    #-----------------------------------------------------------------------------
    def CheckFlag(self,FlagFileName):
        #key word
        KEY_Name1 = 'STATUS'
        KEY_Name2 = '='

        try:
            #read file
            f = open(FlagFileName)
              
            #read flag
            line = f.readline()
            
            #check KEY
            if line.find(KEY_Name1) == -1:
                f.close()
                return -1
            #check KEY
            if line.find(KEY_Name2) == -1:
                f.close()
                return -1
            
            #check Value,STATUS=1,means finished.
            if line[len(line)-1] == '1':
                f.close()
                return 1
            
            #check Value,STATUS=0,means not finished.
            if line[len(line)-1] == '0':
                f.close()
                return 0      
        #open file failed.
        except:
            f.close()
            return -1
        

    

        