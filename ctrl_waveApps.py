#-*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
# Name:        ctrl_waveApps.py
# Purpose:     control veriwave waveApps to execute test case.
#
# Author:      gongke
#
# Created:     2013/05/20
# RCS-ID:      $Id: ctrl_waveApps.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------

import os,os.path
import ctypes
import win32api,win32gui,win32con,win32com.client
import win32process,subprocess
import time,datetime
import pywintypes
from win_GUI import *  
import shutil
from WtLog import log_public

#----------------------------------------------------------------------------
WAVEApps_EXE_PATH = r'C:\Program Files\VeriWave\waveapps.exe'
WAVEApps_RESULT_DIR = r'C:\Documents and Settings\liugang\VeriWave\WaveApps\Results'
WAVEApps_CLASS = 'QWidget'
PDF_CLASS = 'AdobeAcrobat'

#----------------------------------------------------------------------------
#ERROR LIST
ERR_NO_0001 = 'error_no_1:you have pywintypes errors when you try to get hwnd of waveApps window for first time.'
ERR_NO_0002 = 'error_no_2:you have pywintypes errors when you try to get hwnd of waveApps window.'
ERR_NO_0003 = 'error_no_3:you have pywintypes errors when you try to get hwnd of PDF window for first time.'
ERR_NO_0004 = 'error_no_4:you have pywintypes errors when you try to get hwnd of PDF window.'
ERR_NO_0005 = 'error_no_5:you can not open waveApps.'
ERR_NO_0006 = 'error_no_6:you have inputted wrong config file.'
ERR_NO_0007 = 'error_no_7:you have pywintypes errors when you try to get hwnd of PDF window.'
ERR_NO_0008 = 'error_no_8:you have pywintypes errors when you try to get hwnd of PDF window.'
ERR_NO_0009 = 'error_no_9:you can not control waveApps window and close it.'
    

def findControls(topHwnd,
                 wantedText=None,
                 wantedClass=None,
                 selectionFunction=None):
    '''Find controls.
    You can identify controls using captions, classes, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    topHwnd             The window handle of the top level window in which the
                        required controls reside.
    wantedText          Text which the required controls' captions must contain.
    wantedClass         Class to which the required controls must belong.
    selectionFunction   Control selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of a desired control.

    Returns:            The window handles of the controls matching the
                        supplied selection criteria.    

    Usage example:      optDialog = findTopWindow(wantedText="Options")
                        def findButtons(hwnd, windowText, windowClass):
                            return windowClass == "Button"
                        buttons = findControl(optDialog, wantedText="Button")
                        '''
    def searchChildWindows(currentHwnd):
        results = []
        childWindows = []
        try:
            win32gui.EnumChildWindows(currentHwnd,
                                      _windowEnumerationHandler,
                                      childWindows)
        except win32gui.error:
            # This seems to mean that the control *cannot* have child windows,
            # i.e. not a container.
            return
        for childHwnd, windowText, windowClass in childWindows:
            descendentMatchingHwnds = searchChildWindows(childHwnd)
            if descendentMatchingHwnds:
                results += descendentMatchingHwnds

            if wantedText and \
               not _normaliseText(wantedText) in _normaliseText(windowText):
                continue
            if wantedClass and \
               not windowClass == wantedClass:
                continue
            if selectionFunction and \
               not selectionFunction(childHwnd):
                continue
            results.append(childHwnd)
        return results
        
    return searchChildWindows(topHwnd)

def _windowEnumerationHandler(hwnd, resultList):
    '''Pass to win32gui.EnumWindows() to generate list of window handle,
    window text, window class tuples.'''
    resultList.append((hwnd,
                       win32gui.GetWindowText(hwnd),
                       win32gui.GetClassName(hwnd)))

class ctrl_waveApps:
    
    m_ERROR_MSG = "no error"    #recoard error message.   
        
    def __init__(self):
        self.myobj = win_gui()
        self.conf_file_dir = ''
        self.dst = ''
        self.time_start = 0
        self.time_current = 0
        self.loop_time = 0
        self.wait_time = 0
        self.timeout = -1
        self.list_results_dir = []
        self.list_newest_dir = []
        self.report = ''
        self.src = ''
        self.list_dst_dir = []
        self.old_file = ''
        self.conf_file = ''
        self.new_file = ''
        
    #-----------------------------------------------------------------------------
    # Name:        GetErrorInfo -get error information
    # ruturn:      return string.the string is error message. if no error happen ,it is "no error".
    # Author:      <gongke>
    #
    # Created:     2013/05/20
    # RCS-ID:      $Id: rw_Excel_FLOW.py $
    #-----------------------------------------------------------------------------
    def GetErrorInfo(self):        
       return self.m_ERROR_MSG
              
    #-----------------------------------------------------------------------------
    # Name:         waveApps
    # purpose:      control waveApps to execute test case.
    # Parameter:    conf_file_dir_1:the file you use to configure test environment.
    #               ip_address_1:ip address of veriwave tester.
    #               dst_1:the dir you want to save test reports.
    #               my_wait_time_1:timeout handle.If time that you wait for report's popup
    #                              is larger than my_wait_time_1,the test will be stopped
    #                              and execute latter tests. 
    # explain:     
    # Author:       gongke
    #
    # Created:      2013/05/20
    #-----------------------------------------------------------------------------   
    def waveApps(self,conf_file_dir_1,dst_1,my_wait_time_1):
        self.my_wait_time = my_wait_time_1
        self.conf_file_dir = conf_file_dir_1
        if os.path.exists(dst_1) ==False:
            msg = dst_1  + " not exists , I will help you mkdir this path:" +dst_1
            print msg
            info_public(msg)
            os.mkdir(dst_1)
        self.dst = dst_1
        
        self.init_waveApps()
        self.init_PDF()
        if self.open_waveApps() == False:
            return False
        if self.choose_conf_file() == False:
            return False
        self.select_ssid()
        self.run_waveApps()
        self.operate_report()
        if self.close_waveApps() == False:
            return False
        if self.timeout == 0:
            self.find_newest_dir()
        else:
            print 'time is out!Enforce to stop the test.'
            return False
        return True
            
    #-----------------------------------------------------------------------------
    # Name:         init_waveApps
    # purpose:      initialize waveApps.If any waveApps window exists,close it.
    # explain:     
    # Author:       gongke
    #
    # Created:      2013/05/20
    #-----------------------------------------------------------------------------  
    def init_waveApps(self):
        try:
            hwnd0 = win32gui.FindWindow(WAVEApps_CLASS,None)
        except:
            log_public(ERR_NO_0001)            
            self.m_ERROR_MSG = ERR_NO_0001
            hwnd0 = 0
            print 'hwnd0:',hwnd0
            
        while hwnd0 != 0:
            self.close_waveApps()
            print 'close_waveApps'
            try:
                hwnd0 = win32gui.FindWindow(WAVEApps_CLASS,None)
                print 'new hwnd0---',hwnd0
            except:
                log_public(ERR_NO_0002)            
                self.m_ERROR_MSG = ERR_NO_0002
                hwnd0 = 0
            print 'new hwnd0:',hwnd0
        else:
            print 'hwnd0=0,init_waveApps has been done'
        return True
       
    #-----------------------------------------------------------------------------
    # Name:         init_PDF
    # purpose:      initialize pdf.If any pdf file exists,close it.
    # explain:     
    # Author:       gongke
    #
    # Created:      2013/05/20
    #-----------------------------------------------------------------------------  
    def init_PDF(self):
        try:
            hwnd1 = win32gui.FindWindow(PDF_CLASS,None)
        except:
            log_public(ERR_NO_0003)            
            self.m_ERROR_MSG = ERR_NO_0003
            hwnd1 = 0
            print 'hwnd1:',hwnd1
            
        while hwnd1 != 0:
            #close PDF window    
            time.sleep(2)
            win32gui.PostMessage(hwnd1, win32con.WM_SYSCOMMAND, win32con.SC_CLOSE, 0);
            print 'close_PDF'
            try:
                hwnd1 = win32gui.FindWindow(PDF_CLASS,None)
                print 'new hwnd1---',hwnd1
            except:
                log_public(ERR_NO_0004)            
                self.m_ERROR_MSG = ERR_NO_0004
                hwnd1 = 0
            print 'new hwnd1:',hwnd1
        else:
            print 'hwnd1=0,init_PDF has been done'
        return True

    #-----------------------------------------------------------------------------
    # Name:         open_waveApps
    # purpose:      open waveApps.
    # explain:     
    # Author:       gongke
    #
    # Created:      2013/05/20
    # Amend:        2013/07/05  ---yuanwen
    #-----------------------------------------------------------------------------       
    def open_waveApps(self): 
        #open waveApps,wait for 3 seconds   
        try:
            win32api.ShellExecute(0,'open',WAVEApps_EXE_PATH,'','',1)
            print "open waveApps"
            time.sleep(3)
        except:
            print 'open waveApps error'
            log_public(ERR_NO_0005)            
            self.m_ERROR_MSG = ERR_NO_0005
            return False
        '''       
        #find handle for the waveApps window
        hwnd2 = win32gui.FindWindow(WAVEApps_CLASS,'IxVeriwave WaveApps Main Page')
        print 'hwnd2',hwnd2
            
        #move window of 'IxVeriwave WaveApps Main Page' to top left corner
        win32gui.MoveWindow(hwnd2,0,0,626,270,1)
        time.sleep(0.5)
        #click button -- 'wired and wireless testing' 
        self.myobj.Mouse_LB_D(str_app = WAVEApps_CLASS,lb_dx = '238',lb_dy = '165',Flag = '1')
        time.sleep(0.5)
            
        #click button -- 'wired only testing'
        #self.myobj.Mouse_LB_D(str_app='QWidget',lb_dx='426',lb_dy='166',Flag='1')
            
        #click button -- 'apply'
        self.myobj.Mouse_LB_D(str_app = WAVEApps_CLASS,lb_dx = '305',lb_dy = '240',Flag = '1')
        '''
        return True

    #-----------------------------------------------------------------------------
    # Name:         choose_conf_file
    # purpose:      choose config file which has saved config infomation for test.
    # explain:     
    # Author:       gongke
    #
    # Created:      2013/05/20
    #-----------------------------------------------------------------------------   
    def choose_conf_file(self):
        #get control of waveApps window.    
        hwnd3 = win32gui.FindWindow(WAVEApps_CLASS,None)
        print 'hwnd3',hwnd3
        time.sleep(0.5)
        
        #set waveApps window to top.
        win32gui.SetForegroundWindow(hwnd3)
        time.sleep(0.5)
        
        #move waveApps window to top left corner.
        win32gui.MoveWindow(hwnd3,0,0,1448,878,1)
        
        #send Alt+F to open 'File' in menu bar.
        win32api.Sleep(1000)
        win32api.keybd_event(18,0,0,0);   #18��Alt�ļ���
        win32api.keybd_event(70,0,0,0);   #70��F�ļ���
        win32api.Sleep(1000)
        win32api.keybd_event(70,0,win32con.KEYEVENTF_KEYUP,0);
        win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
        win32api.Sleep(1000)
 
        #send O to open 'open' window.
        win32api.keybd_event(79,0,0,0);  #79��O�ļ���
        win32api.Sleep(1000)
        win32api.keybd_event(79,0,win32con.KEYEVENTF_KEYUP,0);
        win32api.Sleep(1000)
        
        #choose config file and open it.
        self.myobj.Find_Gui_edit(str_app = 'Open',control_class = 'ComboBox',filename = self.conf_file_dir,control_name = '',stop_flag = '0')
        self.myobj.Find_Gui_button(str_app = 'Open',control_class = 'Button',control_name = '��(&O)')   
        time.sleep(0.5) 
        
        hwnd4 = win32gui.FindWindow('#32770','Open')
        print 'hwnd4: ',hwnd4
            
        if hwnd4 > 0:
            log_public(ERR_NO_0006)            
            self.m_ERROR_MSG = ERR_NO_0006
            self.myobj.Find_Gui_button(str_app = 'Open',control_class = 'Button',control_name = 'ȷ��')
            time.sleep(0.5)
            self.myobj.Find_Gui_button(str_app = 'Open',control_class = 'Button',control_name = 'ȡ��')
            time.sleep(0.5)
            self.close_waveApps()
            print 'close_waveApps'
            return False
        else:
            print 'conf_file is correct.'
            return True
    
    #-----------------------------------------------------------------------------
    # Name:         Mouse_LB_click
    # purpose:      click the mouse's left butten.
    # explain:     
    # Author:       yuanwen
    #
    # Created:      2013/07/5
    #----------------------------------------------------------------------------- 
    def Mouse_LB_click(self,hwnd):

        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)
        time.sleep(1)
    
    #-----------------------------------------------------------------------------
    # Name:         click_CurrentPlace
    # purpose:      click on the current place.
    # explain:     
    # Author:       yuanwen
    #
    # Created:      2013/07/5
    #----------------------------------------------------------------------------- 
    def click_CurrentPlace(self,lb_dx,lb_dy):
        
        tmp=(string.atoi(lb_dx),string.atoi(lb_dy))
        
        win32api.SetCursorPos(tmp)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tmp[0], tmp[1])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tmp[0], tmp[1])
    
    #-----------------------------------------------------------------------------
    # Name:         select_ssid
    # purpose:      select ssid.
    # explain:     
    # Author:       yuanwen
    #
    # Created:      2013/07/5
    #----------------------------------------------------------------------------- 
    def select_ssid(self):  
              
        hwd0 = win32gui.FindWindow(WAVEApps_CLASS,None)
        #print hwd0
        win32gui.SetForegroundWindow(hwd0)
        hwd1 = win32gui.FindWindowEx(hwd0, None, WAVEApps_CLASS, 'qt_central_widget')
        #print hwd1
        hwd2 = win32gui.FindWindowEx(hwd1, None, WAVEApps_CLASS, 'mainStack')
        #print hwd2
        hwd3 = win32gui.FindWindowEx(hwd2, None, WAVEApps_CLASS, 'portSetup')
        #print hwd3
        hwd4 = win32gui.FindWindowEx(hwd3, None, WAVEApps_CLASS, 'buttonGroup28')
        #print hwd4


        #click Connect butten
        hwd5 = win32gui.FindWindowEx(hwd4, None, WAVEApps_CLASS, 'chassisConnectBtn')
        #print hwd5
        self.Mouse_LB_click(hwd5)
        time.sleep(5)

        #click Scan Channels butten
        hwd6 = win32gui.FindWindowEx(hwd4, None, WAVEApps_CLASS, 'autoScanBtn')
        self.Mouse_LB_click(hwd6)
        time.sleep(30)

        #click Clients butten
        hwd7 = win32gui.FindWindowEx(hwd1, None, WAVEApps_CLASS, 'groupBox66')
        #print hwd7
        hwd8 = win32gui.FindWindowEx(hwd7, None, WAVEApps_CLASS, 'mainToolBox')
        #print hwd8
        ComboBox_list = findControls(hwd8,wantedClass = WAVEApps_CLASS)
        #print ComboBox_list
        hwd9 = ComboBox_list[130]
        #print hwd9
        self.Mouse_LB_click(hwd9)
        time.sleep(2)

        #select SSID
        self.click_CurrentPlace(lb_dx = '1040',lb_dy = '226')
        self.click_CurrentPlace(lb_dx = '1040',lb_dy = '226')
        self.click_CurrentPlace(lb_dx = '1040',lb_dy = '226')
        time.sleep(1)
        self.click_CurrentPlace(lb_dx = '1040',lb_dy = '245')
        time.sleep(1)

        return True
    
    #-----------------------------------------------------------------------------
    # Name:         run_waveApps
    # purpose:      run waveApps,begin the test.
    # explain:     
    # Author:       gongke
    #
    # Created:      2013/05/20
    #----------------------------------------------------------------------------- 
    def run_waveApps(self):        
        #click the start button to run test.
        self.myobj.Mouse_LB_D(str_app = WAVEApps_CLASS,lb_dx = '215',lb_dy = '80',Flag = '1')
        return True

    #-----------------------------------------------------------------------------
    # Name:         operate_report
    # purpose:      close pdf of result when it pops up.
    # explain:     
    # Author:       gongke
    #
    # Created:      2013/05/20
    #-----------------------------------------------------------------------------   
    def operate_report(self):
        #record start time of the test.
        time_start = time.time()
        print 'time_start:',time_start
        
        #get handle of PDF window,hwnd5=0 means there is not any PDF window.
        try:
            hwnd5 = win32gui.FindWindow(PDF_CLASS,None)
        except:
            log_public(ERR_NO_0007)            
            self.m_ERROR_MSG = ERR_NO_0007
            hwnd5 = 0
        print 'hwnd5:',hwnd5
        
        #loop to check whether the result pdf is created.
        #hwnd5 == 0 means the result pdf is not created,else created.
        while hwnd5 == 0:
            
            #check hwnd5 every 10 seconds.
            time.sleep(10)
            
            #timeout judgement
            time_current = time.time()
            loop_time = time_current - time_start
            print 'loop_time',loop_time
        
            wait_time = string.atoi(self.my_wait_time)
            if loop_time <= wait_time:
                self.timeout = 0
                print 'timeout = 0,no timeout'
            else:
                self.timeout = 1
                print 'timeout = 1,timeout!'
                break
        
            #check hwnd5.
            try:
                hwnd5 = win32gui.FindWindow(PDF_CLASS,None)
            except:
                log_public(ERR_NO_0008)            
                self.m_ERROR_MSG = ERR_NO_0008
                hwnd5 = 0

            print 'new_hwnd5:',hwnd5
            
        else:
            print 'pdf is created.'
        
        #close PDF window    
        time.sleep(3)
        win32gui.PostMessage(hwnd5, win32con.WM_SYSCOMMAND, win32con.SC_CLOSE, 0);    
        return True
       
    #-----------------------------------------------------------------------------
    # Name:         find_newest_dir
    # purpose:      copy the result report to a dir you defined and rename it.Its 
    #               new name consists of name of its father dir ,the config file 
    #               name and its original name.
    # explain:     
    # Author:       gongke
    #
    # Created:      2013/05/20
    #-----------------------------------------------------------------------------        
    def find_newest_dir(self):
        #find the newest dir in results dir which saves test results.
        list_results_dir = os.listdir(WAVEApps_RESULT_DIR)
        st = list_results_dir.sort(key = lambda fn: os.path.getmtime(WAVEApps_RESULT_DIR + "\\" + fn) if not os.path.isdir(WAVEApps_RESULT_DIR + "\\" + fn) else 0)
        d = datetime.datetime.fromtimestamp(os.path.getmtime(WAVEApps_RESULT_DIR + "\\" + list_results_dir[-1]))
        print ('last dir is '+list_results_dir[-1])  
        
        list_newest_dir = os.listdir(WAVEApps_RESULT_DIR + '\\' + list_results_dir[-1])
        print 'list_newest_dir:',list_newest_dir
        
        #find the PDF report in the newest dir.The PDF report represents the test result.
        pdf_list = []
        for i in list_newest_dir:    
            n,ext = os.path.splitext(i)    
            if ext.lower() == '.pdf':  
                pdf_list.append(i)
        print 'pdf_list:',pdf_list
        report = pdf_list[0]
        print 'report is ',report
        
        #copy the PDF report to the dst dir.
        src = WAVEApps_RESULT_DIR + "\\" + list_results_dir[-1] + "\\" + report
        print 'src file is ',src
        #shutil.copy2(src,self.dst)
        shutil.copy(src,self.dst)
        print 'copy pdf to dst dir'
        #find the newest file in the dst dir,the file is the newest report copied from results dir.
        list_dst_dir = os.listdir(self.dst)
        dst_st = list_dst_dir.sort(key = lambda fn: os.path.getmtime(self.dst + "\\" + fn) if not os.path.isdir(self.dst + "\\" + fn) else 0)
        dst_d = datetime.datetime.fromtimestamp(os.path.getmtime(self.dst + "\\" + list_dst_dir[-1]))
        print ('last dst dir is '+list_dst_dir[-1]) 
        
        #change the name of the pdf report.
        old_file = self.dst + "\\" + list_dst_dir[-1]
        print 'old_file:',old_file
        conf_file = os.path.basename(self.conf_file_dir)
        print 'conf_file:',conf_file
        new_file = self.dst + "\\" + list_results_dir[-1] + "-" + conf_file + "-" + list_dst_dir[-1]
        print 'new_file:',new_file
        shutil.move(old_file,new_file)
        return True
    
    
    #-----------------------------------------------------------------------------
    # Name:         close_waveApps
    # purpose:      close waveApps.
    # explain:     
    # Author:       gongke
    #
    # Created:      2013/05/20
    #-----------------------------------------------------------------------------         
    def close_waveApps(self):
        #get the handle of waveApps window.
        try:
            hwnd6 = win32gui.FindWindow(WAVEApps_CLASS,None)
            print 'hwnd6:',hwnd6 
            time.sleep(1)
        
            #set the waveApps window to the top.
            win32gui.SetForegroundWindow(hwnd6)
            time.sleep(1)
        except:
            print 'close error'
            log_public(ERR_NO_0009)            
            self.m_ERROR_MSG = ERR_NO_0009
            return False
        
        #click the title bar.
        #self.myobj.Mouse_LB_D(str_app = WAVEApps_CLASS,lb_dx = '75',lb_dy = '10',Flag = '1')
            
        #send Alt+F to open 'File' in menu bar.
        win32api.Sleep(1000)
        win32api.keybd_event(18,0,0,0);   #18��Alt�ļ���
        win32api.keybd_event(70,0,0,0);   #70��F�ļ���
        win32api.Sleep(1000)
        win32api.keybd_event(70,0,win32con.KEYEVENTF_KEYUP,0);
        win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
        win32api.Sleep(1000)

        #send X to close waveApps window.
        win32api.keybd_event(88,0,0,0);  #88��X�ļ���
        win32api.Sleep(1000)
        win32api.keybd_event(88,0,win32con.KEYEVENTF_KEYUP,0);
        win32api.Sleep(1000)
        
        if self.timeout == 1:
            #send Alt+Y to exit waveApps without save.
            win32api.keybd_event(18,0,0,0);   #18��Alt�ļ���
            win32api.keybd_event(89,0,0,0);   #89��Y�ļ���
            win32api.Sleep(1000)
            win32api.keybd_event(89,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.Sleep(1000)
        else:
            #send Alt+N to exit waveApps without save.
            win32api.keybd_event(18,0,0,0);   #18��Alt�ļ���
            win32api.keybd_event(78,0,0,0);   #78��N�ļ���
            win32api.Sleep(1000)
            win32api.keybd_event(78,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.Sleep(1000)           
        return True


if __name__ == '__main__':    
    myclass=ctrl_waveApps()
    #myclass.waveApps(conf_file_dir_1 = r'F:\hemaolin\script\HThoughput_AMPDU_20MHz_SGI_DOWN.wml',dst_1 = 'e:\gongke-result',my_wait_time_1 = '600')
    myclass.waveApps(conf_file_dir_1 = r'F:\hemaolin\script\HThoughput_AMPDU_40MHz_SGI_Bidirectional.wml',dst_1 = 'e:\gongke-result',my_wait_time_1 = '100')
    #myclass.waveApps(conf_file_dir_1 = r'F:\hemaolin\script\HThoughput_AMPDU_20MHz_SGI_Bidirectional.wml',dst_1 = 'e:\gongke-result',my_wait_time_1 = '300')
    
