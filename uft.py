#!/usr/bin/python 
#coding=gbk
import time
import win32gui
import win32ui
import win32api
import win32con
import os
import shutil
import sys
from pywinauto import application
from pywinauto.controls import HwndWrapper

import win32com.client
import winGuiAuto
from win_GUI import *
key = {'a': 65,'b': 66,'c': 67,'d': 68 ,'e':69,'f':70,'g':71, 'h':72,'i':73,'j':74,'k':75,'l':76,'m':77,\
        'n':78,'o':79,'p':80,'q':81,'r':82,'s':83,'t':84,'u':85, 'v':86,'w':87, 'x':88, 'y':89,'z':90,\
        '0':48,'1':49,'2':50,'3':51,'4':52,'5':53,'6':53,'7':54,'8':56,'9':57,\
        'f1':112,'f2':113,'f3':114,'f4':115,'f5':116,'f6':117,'f7':118,'f8':119,'f9':120,'f10':121,'f11':122,'f12':123,\
        'enter':13}
class UFT:
    def __init__(self,path=''):
        self.progam_path = path
        
    def init_uftpath(self,path):
        self.progam_path = path
        return True
        
    def start_UFT(self,test_case = r"E:\UFTTestCase\EMS_Test\EMS_FUN_000012\DemoTest\DemoTest",path=''):
        self.progam_path = path
        self.app = application.Application.start(self.progam_path)
        
        WINDOW_TITLE = u'HP Unified Functional Testing'
        cnt = 0
        while cnt<60:
            try:
                hwnd = 0
                hwnd = winGuiAuto.findTopWindow('Unified Functional Testing')
                if hwnd>0:
                    break
            except Exception,e:
                cnt = cnt + 1
                time.sleep(1)
                pass  
        self.app[u'Unified Functional Testing'][u'&Continue'].Click()
        self.app[u'Unified Functional Testing - Add-in Manager'][u'OK'].Click()
        
        WINDOW_TITLE = u'HP Unified Functional Testing'

        result = False
        cnt = 0
        while cnt<60:
            try:
                hwnd = 0
                hwnd = winGuiAuto.findTopWindow('HP Unified Functional Testing')
                if hwnd > 0:
                    result = True
                    break
            except Exception,e:
                cnt = cnt + 1
                time.sleep(1)
                pass  
        return result
    
    def first_test_case(self,test_case = r"E:\UFTTestCase\EMS_Test\EMS_FUN_000012\DemoTest\DemoTest"):
        
        WINDOW_TITLE = u'HP Unified Functional Testing'
        self.app[WINDOW_TITLE].TypeKeys(u'^O')
        time.sleep(2)
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys(test_case)
        except Exception,e:
            print e
        time.sleep(2)
        self.app[u'Open Test'][u'Open'].Click()
        test_win = win_gui()
        cnt = 0
        while cnt<60:
            try:
                hwnd = 0
                hwnd = test_win.find_main_window_end(test_case)
                #print '12 = ',hwnd 
                if hwnd>0:
                    break
            except Exception,e:
                cnt = cnt + 1
                time.sleep(1)
                pass       
        win32api.keybd_event(116,0,0,0)
        win32api.Sleep(2)
        win32api.keybd_event(116,0,win32con.KEYEVENTF_KEYUP,0)
        time.sleep(2)
        win32api.keybd_event(13,0,0,0)
        win32api.Sleep(2)
        win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
        cnt = 0
        result = False
        while cnt<60:
            try:

                hwnd = 0
                hwnd = test_win.find_main_window_end('HP Run Results Viewer')
                if hwnd>0:
                    result = True
                    break
            except Exception,e:
                print e
                cnt = cnt + 1
                time.sleep(1)                                    
                pass
        return result
    
    def test_case(self,test_case = r"E:\UFTTestCase\EMS_Test\EMS_FUN_000012\DemoTest\DemoTest"):
        
        time.sleep(5)
        WINDOW_TITLE = r"HP Unified Functional Testing"
        app=application.Application().connect_(title_re="HP Unified Functional Testing" )
        er = win_gui()
        er.shortcut_keys(['Ctrl','O'])
        time.sleep(2)
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
        
            shell.SendKeys(test_case)
        except Exception,e:
            print e
        time.sleep(2)
        app[u'Open Test'][u'Open'].Click()
        win32api.keybd_event(13,0,0,0)
        win32api.Sleep(2)
        win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
        test_win = win_gui()
        cnt = 0
        while cnt<60:
            try:
                hwnd = 0
                hwnd = test_win.find_main_window_end(test_case)
                if hwnd>0:
                    break
            except Exception,e:
                cnt = cnt + 1
                time.sleep(1)
                pass 
        
        win32api.keybd_event(116,0,0,0)
        win32api.Sleep(2)
        win32api.keybd_event(116,0,win32con.KEYEVENTF_KEYUP,0)
        time.sleep(2)
        win32api.keybd_event(13,0,0,0)
        win32api.Sleep(2)
        win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
        cnt = 0
        test_win1 = win_gui()
        while cnt<60:
            try:
                hwnd = None
                hwnd = test_win1.find_main_window_end('HP Run Results Viewer')
                if hwnd>0:
                    break
            except Exception,e:
                cnt = cnt + 1
                time.sleep(1)
                pass
        time.sleep(2) 
        
    def kill_UFT(self, pidname = 'reportviewer.exe'):
        REC_read = 'wmic process where caption="'+pidname+'" get caption,commandline /value'
        REC_kill =  'TASKKILL /F /IM ' + pidname
        info = os.popen(REC_read).read()
        info = os.popen(REC_kill).read()
        
if __name__ == "__main__":
	path = u"C:\\Program Files\\Hp\\Unified Functional Testing\\bin\\UFT.exe"

	test = UFT(path)
	print test.start_UFT()

	print test.first_test_case()
	print "OK"
	pidname = 'UFT.exe'
	pidname1 = ur"reportviewer.exe"
	test.kill_UFT()
	time.sleep(5)
	test.test_case(r"E:\UFTTestCase\EMS_Test\EMS_FUN_000012\DemoTest\DemoTest")

	test.kill_UFT(pidname1)
	test.kill_UFT(pidname)



