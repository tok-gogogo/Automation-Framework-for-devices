# -*- coding: UTF-8 -*- 
#-----------------------------------------------------------------------------
# Name:        rssid.py
# Purpose:     
#
# Author:      <gongke>
#
# Created:     2013/03/27
# RCS-ID:      $Id: rssid.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
#<0.0.1> Create by gongke @2013/03/30

import win32gui
import win32ui
import win32api
import win32con

from pywinauto import application
import time
import os
import re
import string
from WtLog import log_public

import win32gui
import win32ui
import win32api
import win32con
from win_GUI import * 
import string
from public import *

 
#define KEYS
#-------------------------------------------------------------------------------
KEY_GUOBIAO ='gb18030'
KEY_NETDIALOG = u"网络连接"
KEY_NETDIALOG_CONTROL_LV_TEXT = "text"
KEY_DIALOG_READY = "ready"
KEY_NETDIALOG_CONTROL_LV_IMAGE=  "image"
KEY_NETDIALOG_FILE = "%F"
KEY_NETDIALOG_FILE_CLOSE = "C" 
KEY_NETDIALOG_FILE_RESOSE = "R"
KEY_NETDIALOG_FILE_STATUS = "U"
KEY_NETDIALOG_FILE_LAUNCH= "A"
KEY_NETDIALOG_VIEW = "%V"
KEY_NETDIALOG_VIEW_REFLASH="R"
KEY_NETDIALOG_HIT = "H"
KEY_NETDIALOG_ICON = "I"
KEY_PAUSH_SLEEP_TIEM= 0.5
KEY_RESORSE_DLG_TAB_WIRESS = 1
KEY_LAUNCH_WAIT = 10
KEY_WIRELESS = u"无线网络连接"
KEY_WIRELESS_BUTTON = u"查看无线网络"
KEY_DELETE_BUTTON =  u"删除"
KEY_ADD_BUTTON = u"添加"
KEY_WIRELESS_BUTTON_REFLESH = u"刷新网络列表"
KEY_DEFAULT_WAIT_TIME = 20
KEY_LS_ITEM_NUM = 1
KEY_WIRELESS_BUTTON_CONNECT = u"连接"
KEY_WIRELESS_BUTTON_DISCONNECT = u"断开"
KEY_WIRELESS_BUTTON_CHILD_YES= u"是"
KEY_WIRELESS_BUTTON_CHILD_NO_SINGNO = u"Windows 无法连接到选定网络"
KEY_WIRELESS_BUTTON_CHILD_NO_WARMING =u"您正在连接到不安全的网络"
KEY_WIRELESS_BUTTON_CHILD_BTN_STILL = u"仍然连接"
FIND_KEY_NAME = u"正在"
KEY_NAME_MENU = u"名称"
KEY_MODE_VIEW_MENU = u"类型"
#-------------------------------------------------------------------------------
KEY_FIND_IPCONFIG = "ipconfig"        
KEY_FIND_WIRESS_NAME= u"无线网络连接"
KEY_FIND_WIRESS_NAME_PROPERTY = u"无线网络连接 属性"
KEY_FIND_WIRESS_NAME_STATUS = u"无线网络连接 状态"
KEY_FIND_WIRESS_NAME_STATUS_TAB = u"常规"
KEY_FIND_WIRESS_PORPTY = u"无线网络属性"
KEY_FIND_WIRESS_PROTECT_EAP = u"受保护的 EAP 属性"
KEY_FIND_WIRESS_EAP_MSCHAP = u"EAP MSCHAPv2 属性"
KEY_FIND_WIRESS_VEN_TAP = u"验证"
KEY_DIALOG_YES = u"确定"
DIALOG_DISAPR_WAIT_TIME = 180
#-------------------------------------------------------------------------------
#Security Model
SECURITY_MODEL_WPA = u"启用安全的无线网络 (WPA) "
SECURITY_MODEL_WPA2 = u"启用安全的无线网络 (WPA2) "
SECURITY_MODEL_WPA_PSK = u"启用安全的无线网络 (WPA-PSK) "
SECURITY_MODEL_WPA2_PSK = u"启用安全的无线网络 (WPA2-PSK) "
SECURITY_MODEL_NOT_SET = u"启用安全的无线网络"
SECURITY_MODEL_AES ="AES"
SECURITY_MODEL_PROCTED = u"受保护的 EAP (PEAP)"
SECURITY_MODEL_BTN_ADD = u"添加..."
#-------------------------------------------------------------------------------
#code 
KEY_DSTAY_IDX = "idx"
KEY_DSTAY_CONTS = "strConts"              
KEY_SUCCES_CONNECT = u"已连接上"
KEY_WIRESS_LIST_SIGNAL =u"信号强度"
#-------------------------------------------------------------------------------
#input PASSWORD box
INPUT_TIMEXAX = 60 #second
KEY_TIP_CLSS = "tooltips_class32"
KEY_INPUT_PASSW_TIP = u"单击此处选择连接到网络的证书或其它凭据"
KEY_INPUT_PASSW_DIALOG = u"输入凭据"   
#-------------------------------------------------------------------------------
#Pop up menu
KEY_POP_MENU_V = u"查看"
KEY_POP_MENU_V_H = u"缩略图"
KEY_POP_MENU_S = u"排列图标"
KEY_POP_MENU_S_NAME = u"名称"
KEY_POP_MENU_RF = u"刷新"
KEY_POP_MENU_RSE = u"属性"
KEY_POP_MENU_STU = u"状态"
KEY_POP_MENU_LAUCH = u"启用"
KEY_POP_MENU_CONNECT_DIALOG=u"查看可用的无线连接"

#-------------------------------------------------------------------------------
#Error list
ERR_001 = "ERR_001:Can not open Net Connect Dialog."
ERR_002 = "ERR_002:Can not find the Input password Tips."
ERR_003 = "ERR_003:Can not input user name and password at <Input Password> dialog."
ERR_004 = "ERR_004:Can not find SSID at <Wiress Property> dialog's ListBox."
ERR_005 = "ERR_005:Can not set SSID's Security at <Wiress Property>."
ERR_006 = "ERR_006:Can not find specipy SSID at <Wiress Property> ListBox."
ERR_007 = "ERR_007:Can not delete SSID at ListBox of <Wiress Property>."
ERR_008 = "ERR_008:Can not select Set WiressConfig tab of <Wiress Property>."
ERR_009 = "ERR_009:TIME OUT,but network still connecting."
ERR_010 = "ERR_010:Can not Open wires dialog "
ERR_011 = "ERR_011:Can not find wiress icon."
ERR_012 = "ERR_012:Can not find SSID at List <WiressConnect>."
ERR_013 = "ERR_013:Can not Refresh SSID List."
ERR_014 = "ERR_014:Can not lanuch <Net Connect> Dialog."
ERR_015 = "ERR_015:Not install Wiress Driver."
ERR_016 = "ERR_016:Can not check Wiress Driver."
ERR_017 = "ERR_017:can not find Wiress icon."
ERR_018 = "ERR_018:user name or password is empty."
ERR_019 = "ERR_019:no signal at the area."
ERR_020 = "ERR_020:can not get key."
ERR_021 = "ERR_021:Can not connect to SSID,Connect failded." 
ERR_022 = "ERR_022:Can Control <Net Status> dialog,Connect failded." 
ERR_023 = "ERR_023:Can not operate popup menu." 
ERR_024 = "ERR_024:Exception error" 

#-------------------------------------------------------------------------------


class ssid:   
    
    def __init__(self):
        log_print( "init rssid")
        self.m_ERROR_MSG = "no error"    #recoard error message.
        self.error_NG = ''
        self.wingui = win_gui()
        self.ssid_user =''
        self.total_exec_all =0
        
        
    #000 
    #when error occur,get error informaiton.   
    
    def SetErrorInfo(self):
        self.m_ERROR_MSG = "no error"
        
    def GetErrorInfo(self):
        log_print( self.m_ERROR_MSG)
        msg = 'send check ' + str(self.total_exec_all)+' times'
        log_print(msg)
        return self.m_ERROR_MSG      
           
           
    #001
    #-----------------------------------------------------------------------------
    # Name:        connect
    # Purpose:     connect to specify SSID.
    # parameter:   setSSID-SSID name.
    #              strUSER-the user name,Only use when the SSID have security.
    #              strPASSWORD -the password,Only use when the SSID have security.
    # Return:      return True,when connect success,else return False.              
    # Author:      <gongke>    #
    # Created:     2013/03/30
    #-----------------------------------------------------------------------------
    def connect(self,setSSID,strUSER="",strPASSWORD=""):
        self.peap_flag_first = True
        log_print( ">>Connect")
        #close exit dialog
        self.closeExistDialog()        
        

        #check wireless Driver whether installed.
        '''
        if self.CheckWirelessDriver() == False:
            return False
        
           
        #check wireless whether launched.
        if self.CheckWirelseeLaunch()  == False:
            if self.launchWiressConnect() == False:   
                print 'launchWiressConnect return false'
                return False
        
        #go to connect SSID
        '''
        if self.DoConnectSSID(setSSID,strUSER,strPASSWORD) == False:
            return False
        else:
            return True
        
        return True
        
    
    #002
    def CheckWirelessDriver(self):
        log_print( ">>CheckWirelessDriver")
        if self.lauchNetWindow() == False:
            return False
        #print '********* lanch Netwindow ok'
        time.sleep(1)
        try:     
                  
            app=application.Application().connect_(title_re=KEY_NETDIALOG )
            app[KEY_NETDIALOG].Wait(KEY_DIALOG_READY)   
            #print '********* lanch Netwindow ok111'         
            time.sleep(6)
            
            #show by image
            #app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_VIEW,pause=KEY_PAUSH_SLEEP_TIEM)
            #app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_HIT,pause=KEY_PAUSH_SLEEP_TIEM)
               
            #myMenu = [KEY_POP_MENU_V,KEY_POP_MENU_V_H]
            #self.PopMenuClick(app,KEY_NETDIALOG,myMenu)      
            
            
            #self.wingui.app_first("网络连接")  
            self.find_wind(KEY_NETDIALOG) 
            #self.wingui.shortcut_keys(['Alt','V'])
            win32api.keybd_event(18,0,0,0)
            win32api.keybd_event(86,0,0,0)
            win32api.keybd_event(86,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
            time.sleep(1)
            #self.wingui.shortcut_keys(['H'])
            
            win32api.keybd_event(72,0,0,0)
            win32api.keybd_event(72,0,win32con.KEYEVENTF_KEYUP,0)
            
            
            #print '********* lanch Netwindow ok333'  
            
            time.sleep(1)
            #sort by name
            #app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_VIEW,pause=KEY_PAUSH_SLEEP_TIEM)
            #app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_ICON,pause=KEY_PAUSH_SLEEP_TIEM)
            #app[KEY_NETDIALOG].TypeKeys(KEY_NAME_MENU,pause=KEY_PAUSH_SLEEP_TIEM)
            #myMenu = [KEY_POP_MENU_S,KEY_POP_MENU_S_NAME]
            #self.PopMenuClick(app,KEY_NETDIALOG,myMenu)
            #self.wingui.shortcut_keys(['Alt','V'])
            
            win32api.keybd_event(18,0,0,0)
            win32api.keybd_event(86,0,0,0)
            win32api.keybd_event(86,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
            time.sleep(1)
            #self.wingui.shortcut_keys(['I']) 
            
            win32api.keybd_event(73,0,0,0)
            win32api.keybd_event(73,0,win32con.KEYEVENTF_KEYUP,0)
           
            time.sleep(1)
            
            self.Mouse_LB_D(KEY_NETDIALOG,'310','243')
            '''
            print '*************'
            app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_VIEW,pause=KEY_PAUSH_SLEEP_TIEM)
            app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_ICON,pause=KEY_PAUSH_SLEEP_TIEM)
            app[KEY_NETDIALOG].TypeKeys(KEY_MODE_VIEW_MENU,pause=KEY_PAUSH_SLEEP_TIEM)
            print '*************11'
            '''
            #refresh the window for icon display.
            #app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_VIEW,pause=KEY_PAUSH_SLEEP_TIEM)
            #app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_VIEW_REFLASH,pause=KEY_PAUSH_SLEEP_TIEM)
            #myMenu = [KEY_POP_MENU_RF]
            #self.PopMenuClick(app,KEY_NETDIALOG,myMenu )
            
            
            time.sleep(2)
            
            #check icon
            log_print('******ListViewWrapper *****')
            print app[KEY_NETDIALOG].ListViewWrapper.ItemCount()
            s=None
            s = app[KEY_NETDIALOG].ListViewWrapper.Items()
            log_print( s)
            log_print('******ListViewWrapper end *****')
            for ct in s:
                #print '************************'
                #print 'ct:',ct[KEY_NETDIALOG_CONTROL_LV_TEXT]
                #print 'KEY_WIRELESS:',KEY_WIRELESS
                #print '************************'
                if ct[KEY_NETDIALOG_CONTROL_LV_TEXT].find(KEY_WIRELESS) >= 0:
                    #print 'find_the wl......'
                    
                    #find icon return True
                    #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE,pause=KEY_PAUSH_SLEEP_TIEM)
                    #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE_CLOSE,pause=KEY_PAUSH_SLEEP_TIEM)
                    
                    self.closeExistDialog()
                    return True
            
            
            #not find icon return False    
            #app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE,pause=KEY_PAUSH_SLEEP_TIEM)
            #app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE_CLOSE,pause=KEY_PAUSH_SLEEP_TIEM) 
            #app[KEY_NETDIALOG].Close()
            
            log_public(ERR_015)
            self.m_ERROR_MSG = ERR_015         
            self.closeExistDialog()                    
            return False    
        except Exception ,excet_str:
            log_print( excet_str)
            log_public(ERR_016)
            self.m_ERROR_MSG = ERR_016      
            self.closeExistDialog()       
            return False        
    
    
    #003
    def CheckWirelseeLaunch(self):
        log_print( ">>CheckWirelseeLaunch")
        #send command to cmd. 
        info = os.popen(KEY_FIND_IPCONFIG).read()
        #check whether the wiress is launch.
        if info.find(KEY_FIND_WIRESS_NAME.encode(KEY_GUOBIAO))>= 0:            
            return True    

        return False   

        
    #004    
    #def CheckSSIDIsConnect(self):
        #print "ok"       
        
        
    #005
    def DoConnectSSID(self,setSSID,strUSER,strPASSWORD):
        log_print( ">>DoConnectSSID")       
        self.ssid_user = setSSID
        #define variable
        idxIcon = 0
        bFindSSID = False
        bConn = False
        strSecurityModel = None
        dstGet={KEY_DSTAY_IDX:0,KEY_DSTAY_CONTS:""}
       
        #open Wireless dialog
        #app = self.OpenWiressDialog()   
        
        LstIDX =[0]
        app = self.OpenNetDialogAndSelectIcon(LstIDX)
        app = application.Application().connect_(title_re=KEY_WIRELESS)
        
        if app == None:
            return False
        #reflesh and chck ssid exist
        if self.refleshSSIDList(app) == False:
            return False
        
        
        bFindSSID = self.findKeyfromWiressList(app,setSSID,dstGet)
        strSSID = dstGet[KEY_DSTAY_CONTS]
        idx = dstGet[KEY_DSTAY_IDX]     
        
        print 'self.findKeyfromWiressList ,bFindSSID:',bFindSSID
        
        if bFindSSID == False:
            return False
        
        '''
        #check Security Model          
        strSecurityModel = self.CheckSSIDSecurity(strSSID) 
        
        #set Security.
        if strSecurityModel != None:            
            if self.SetSecurity(setSSID,strSecurityModel)==False:
                return False
        '''          
        #select SSID
        app[KEY_WIRELESS].ListBoxWrapper.Select(idx)
        
        #get "connect/disconnect" button name to judge connect or disconnect status.
        btnlst = app[KEY_WIRELESS].Button6.WindowText()        
        if btnlst.find(KEY_WIRELESS_BUTTON_CONNECT) >= 0:
            bConn = True
        elif  btnlst.find(KEY_WIRELESS_BUTTON_DISCONNECT) >= 0:
            bConn = False
            
        #click "Connect" button
        if bConn == True:               
            app[KEY_WIRELESS][KEY_WIRELESS_BUTTON_CONNECT].Click()                
           
             
                
            #check and close dialog
            if self.waitDialogDisappear(app) == True:
                
                '''
                #input password
                if strSecurityModel != None:
                    print 'strSecurityModel inputPassword'
                    if self.InputPASSWORD(strUSER,strPASSWORD) == False:
                        return False
                '''
                if self.refleshSSIDList(app) == False:
                    return False
                #close Wiress dialog
                app[KEY_WIRELESS].Close()   
                            
                time.sleep(3) #wait for dialog ready
                if self.CheckStatus(KEY_SUCCES_CONNECT) == False:
                    log_print('CheckStatus is False')
                    return False 
                else:
                    log_print('CheckStatus is True')
                    return True              
                         
            else:
                
                return False                
            
        #click disconnect button       
        else:

            app[KEY_WIRELESS][KEY_WIRELESS_BUTTON_DISCONNECT].Click()  
            time.sleep(1)             
            app[KEY_WIRELESS][KEY_WIRELESS_BUTTON_CHILD_YES].Click()
            time.sleep(1)
            
            #wait refresh
            #reflesh and chck ssid exist
            if self.refleshSSIDList(app) == False:
                return False
            
            bFindSSID = self.findKeyfromWiressList(app,setSSID,dstGet)
            strSSID = dstGet[KEY_DSTAY_CONTS]
            idx = dstGet[KEY_DSTAY_IDX]    
            
            print 'self.findKeyfromWiressList 2222 ,bFindSSID:',bFindSSID
            
            if bFindSSID == False:                
                return False            

            #select SSID
            app[KEY_WIRELESS].ListBoxWrapper.Select(idx)
            time.sleep(1)              
            #connect again
            app[KEY_WIRELESS][KEY_WIRELESS_BUTTON_CONNECT].Click()  
            time.sleep(1) 
            
            #check and close dialog
            
            if self.waitDialogDisappear(app) == True:               
                
                #input password
                '''
                if strSecurityModel != None:
                    print 'strSecurityModel inputPassword  222'
                    if self.InputPASSWORD(strUSER,strPASSWORD) == False:
                        return False
                '''
                if self.refleshSSIDList(app) == False:
                    return False
                #close Wiress dialog
                app[KEY_WIRELESS].Close()
                
                time.sleep(3) #wait for dialog ready                 
                #check success      
                if self.CheckStatus(KEY_SUCCES_CONNECT) == False:  
                    log_print('CheckStatus is False')                 
                    return False
                else:
                    log_print('CheckStatus is True')
                    return True
            else:
                return False
            
        return True               

        
    #006
    def lauchNetWindow(self):
        log_print( ">>lauchNetWindow")     
        time.sleep(2)
        try:
           info = os.popen("ncpa.cpl").read()   
           #print '******* ncpa.cpl*********'
           #print info
           #print '*******ncpa.cpl end *********'
           time.sleep(5)   
        except Exception ,excet_str:
            log_print( excet_str)
            log_public(ERR_001)
            self.m_ERROR_MSG = ERR_001 
            log_print( self.m_ERROR_MSG)
            self.closeExistDialog() 
            return False
        print 'True 11111111'
        return True
    
    #007
    def closeExistDialog(self):
        log_print( ">>closeExistDialog" )          
        #close "wiress" dialog
        try:
            app=application.Application().connect_(title_re=KEY_WIRELESS )
            app[KEY_WIRELESS].Close()
        except Exception ,excet_str:
            log_print( excet_str)
            log_print( "no wiress dilog")
            #self.m_ERROR_MSG = ERR_024 
            
        #close "Net connect" dialog
        try:
            app=application.Application().connect_(title_re=KEY_NETDIALOG )
            app[KEY_NETDIALOG].Close()
        except Exception ,excet_str:
            log_print( excet_str)
            log_print( "no net dilog" ) 
            #self.m_ERROR_MSG = ERR_024               

    
    #008  
    def refleshSSIDList(self,appObj,TIMEMAX= KEY_DEFAULT_WAIT_TIME ):
        log_print( ">>refleshSSIDList")           
        try:
            time.sleep(0.5)
            appObj[KEY_WIRELESS][KEY_WIRELESS_BUTTON_REFLESH].Click() 
            time.sleep(0.5)
            
            itime = 0
            #check sssid list exist.
            while itime < TIMEMAX:            
                iNum = appObj[KEY_WIRELESS].ListBoxWrapper.ItemCount()
                
                if iNum > KEY_LS_ITEM_NUM:
                    return True
                    break
                
                time.sleep(1)
                itime+=1
                
            if itime == TIMEMAX:                 
                 log_public(ERR_012)
                 self.m_ERROR_MSG = ERR_012
                 self.closeExistDialog() 
                 return False            
                          
        except Exception ,excet_str:
            log_print( excet_str)
            log_public(ERR_013)
            self.m_ERROR_MSG = ERR_013
            self.closeExistDialog() 
            return False

    
    #009    
    def launchWiressConnect(self):
        log_print( ">>launchWiressConnect")           
        breturn = False
        self.lauchNetWindow()
        idxIcon = 0
        RET = None
        
        try:
            app=application.Application().connect_(title_re=KEY_NETDIALOG )
            app[KEY_NETDIALOG].Wait(KEY_DIALOG_READY)     
    
            #check icon
            '''
            s=None
            s = app[KEY_NETDIALOG].ListViewWrapper.Items()    
            print '11111',app[KEY_NETDIALOG].ListViewWrapper.ItemCount() 
            for i in   range(app[KEY_NETDIALOG].ListViewWrapper.ItemCount()):
                print 'GetItem:' ,i,app[KEY_NETDIALOG].ListViewWrapper.GetItem(i)
            '''
            for i in range (app[KEY_NETDIALOG].ListViewWrapper.ItemCount()):
                ct = app[KEY_NETDIALOG].ListViewWrapper.GetItem(i)
                if ct[KEY_NETDIALOG_CONTROL_LV_TEXT].find(KEY_WIRELESS) >= 0:
                    idxIcon = i 
                    break
            '''
            for ct in s:
                print '############start#############'
                print ct[KEY_NETDIALOG_CONTROL_LV_TEXT]
                print ct[KEY_NETDIALOG_CONTROL_LV_IMAGE]
                print '#############end############'
                
                if ct[KEY_NETDIALOG_CONTROL_LV_TEXT].find(KEY_WIRELESS) >= 0:
                    print 'findl8******************************'
                    print "image",ct[KEY_NETDIALOG_CONTROL_LV_IMAGE]
                    #print item = 
                    idxIcon = ct[KEY_NETDIALOG_CONTROL_LV_IMAGE]
                    break
            print '22222 idxIcon:' , idxIcon 
            '''
            print idxIcon
            if idxIcon == None:
                log_public(ERR_011)
                self.m_ERROR_MSG = ERR_011
                self.closeExistDialog() 
                breturn = False
            
            #Select icon
            app[KEY_NETDIALOG].ListViewWrapper.Select(idxIcon)    
            RET = app[KEY_NETDIALOG].ListViewWrapper.GetItemRect(idxIcon)      
            time.sleep(0.5)
            print '22222 idxIcon: here' 
            #send "Enter" Key to lauch wiress.
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE,pause=KEY_PAUSH_SLEEP_TIEM)
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE_LAUNCH,pause=KEY_PAUSH_SLEEP_TIEM)
            
            #myMenu = [KEY_POP_MENU_LAUCH]
            #self.PopMenuClick(app,KEY_NETDIALOG,myMenu,RET)
            
              
            #self.wingui.shortcut_keys(['Alt','F'])
            win32api.keybd_event(18,0,0,0)
            win32api.keybd_event(70,0,0,0)
            win32api.keybd_event(70,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
            time.sleep(1)
            #self.wingui.shortcut_keys(['A'])
           
            win32api.keybd_event(65,0,0,0)
            win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0)
           
            
            time.sleep(KEY_LAUNCH_WAIT)
            #close "net connect" dialog
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE,pause=KEY_PAUSH_SLEEP_TIEM)
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE_CLOSE,pause=KEY_PAUSH_SLEEP_TIEM)
            self.closeExistDialog()  
            breturn = True
        except Exception ,excet_str:
            log_print( excet_str)
            log_public(ERR_010)
            self.m_ERROR_MSG = ERR_010
            self.closeExistDialog() 
            breturn = False
            
        return  breturn
    
    
    #010    
    def waitDialogDisappear(self,appObj,TIMEMAX= DIALOG_DISAPR_WAIT_TIME ):
        log_print( ">>waitDialogDisappear")             
        time.sleep(1)
        strNoSingno = ""
        strWarming =""
        itime = 0
        #check child dialog disapear
        print 'waitDialogDisappear',appObj
        
        
        time.sleep(1)
        self.shortcut_keys(['C'])
        time.sleep(4)
        
        while True:      
            try:
                strWarming = appObj[KEY_WIRELESS].Static2.WindowText()
                print 'waitDialogDisappear,strWarming',strWarming
            except Exception ,excet_str:
                log_print( excet_str)
                log_public(ERR_009)
                self.m_ERROR_MSG = ERR_009 
                self.closeExistDialog() 
                return False
            if None == appObj[KEY_WIRELESS].Parent() :
                print 'Parent is None'
                msg = "ssid connect " + str(itime)  + " s"
                log_print(msg)
                
                return True #the child dialog is disappear,not need to wait.
            if  strWarming.find(FIND_KEY_NAME) >=0:
                time.sleep(1)
                itime+=1
                
            '''      
            if None == appObj[KEY_WIRELESS].Parent() :
                return True #the child dialog is disappear,not need to wait.
            #check whether Static2/Static1 is exist.
            
            strWarming = appObj[KEY_WIRELESS].Static2.WindowText() 
            print 'waitDialogDisappear,strWarming',strWarming
            if  strWarming.find(KEY_WIRELESS_BUTTON_CHILD_NO_WARMING) >=0:                
                appObj[KEY_WIRELESS][KEY_WIRELESS_BUTTON_CHILD_BTN_STILL].Click()
                time.sleep(1)
                return True
                
            strNoSingno = appObj[KEY_WIRELESS].Static1.WindowText() 
            print 'waitDialogDisappear,strNoSingno',strWarming
            if strNoSingno.find(KEY_WIRELESS_BUTTON_CHILD_NO_SINGNO) >=0:
                log_public(ERR_019)
                self.m_ERROR_MSG = ERR_019 
                self.closeExistDialog() 
                return False
           
            time.sleep(1)
            itime+=1               
            
        if itime == TIMEMAX:
            appObj[KEY_WIRELESS].Close()
        '''
        log_public(ERR_009)
        self.m_ERROR_MSG = ERR_009 
        self.closeExistDialog() 
        return False #Time out,because the child dialog still exist.


    #011    
    #return True if use security,else return False.
    def CheckSSIDSecurity(self,str):
        log_print( ">>CheckSSIDSecurity")       
        strModel = None
        
        if str.find(SECURITY_MODEL_WPA_PSK) >= 0:
            strModel =  "WPA-PSK"
        elif str.find(SECURITY_MODEL_WPA2_PSK) >= 0:
            strModel =  "WPA2-PSK" 
        elif str.find(SECURITY_MODEL_WPA2) >= 0:
            strModel =  "WPA2"      
        elif str.find(SECURITY_MODEL_WPA) >= 0:
            strModel =  "WPA"
        elif str.find(SECURITY_MODEL_NOT_SET) >= 0: 
            strModel =  "WPA"
       
        return strModel   
      
      
    #012  
    def OpenNetDialogAndSelectIcon_check(self,lstOUT): 
        log_print( ">>OpenNetDialogAndSelectIcon")               
        app = None
        iIcon = 0
        #lauch "net connect" dialog
        if self.lauchNetWindow() == False:
            return app        
        
        time.sleep(3)
        print '1111111'
        try:
            #geconnect to "net connect" dialog
            app=application.Application().connect_(title_re=KEY_NETDIALOG )
            app[KEY_NETDIALOG].Wait(KEY_DIALOG_READY)      
                        
            print '2222222'
            #check icon
            #s = app[KEY_NETDIALOG].ListViewWrapper.Items()  
            
            for i in range(app[KEY_NETDIALOG].ListViewWrapper.ItemCount()):
                print 'here 333333'
                ct = app[KEY_NETDIALOG].ListViewWrapper.GetItem(i)
                if ct[KEY_NETDIALOG_CONTROL_LV_TEXT].find(KEY_WIRELESS) >= 0:
                    iIcon = i
                    lstOUT[0] = iIcon
                    break
            '''
            for ct in s:
                if ct[KEY_NETDIALOG_CONTROL_LV_TEXT].find(KEY_WIRELESS) >= 0:
                    iIcon = ct[KEY_NETDIALOG_CONTROL_LV_IMAGE]
                    lstOUT[0] = iIcon
                    break
            '''
            #Select icon
            app[KEY_NETDIALOG].ListViewWrapper.Select(iIcon) 
            
               
        except Exception ,excet_str:
            log_print( excet_str)            
            log_public(ERR_017)
            self.m_ERROR_MSG = ERR_017
            self.closeExistDialog() 
            
        return app
    
    def OpenNetDialogAndSelectIcon(self,lstOUT): 
        log_print( ">>OpenNetDialogAndSelectIcon")               
        app = None
        iIcon = 0
        #lauch "net connect" dialog
        if self.lauchNetWindow() == False:
            return app        
        
        time.sleep(3)
        print '1111111'
        try:
            #geconnect to "net connect" dialog
            app=application.Application().connect_(title_re=KEY_NETDIALOG )
            app[KEY_NETDIALOG].Wait(KEY_DIALOG_READY)      
                        
            print '2222222'
            #check icon
            #s = app[KEY_NETDIALOG].ListViewWrapper.Items()  
            
            for i in range(app[KEY_NETDIALOG].ListViewWrapper.ItemCount()):
                print 'here 333333'
                ct = app[KEY_NETDIALOG].ListViewWrapper.GetItem(i)
                if ct[KEY_NETDIALOG_CONTROL_LV_TEXT].find(KEY_WIRELESS) >= 0:
                    iIcon = i
                    lstOUT[0] = iIcon
                    break
            '''
            for ct in s:
                if ct[KEY_NETDIALOG_CONTROL_LV_TEXT].find(KEY_WIRELESS) >= 0:
                    iIcon = ct[KEY_NETDIALOG_CONTROL_LV_IMAGE]
                    lstOUT[0] = iIcon
                    break
            '''
            #Select icon
            app[KEY_NETDIALOG].ListViewWrapper.Select(iIcon) 
            tempRect = app[KEY_NETDIALOG].ListViewWrapper.GetItemRect(iIcon)
            self.PopMenuClick(app,KEY_NETDIALOG,[KEY_POP_MENU_CONNECT_DIALOG],tempRect)
            time.sleep(5)
           
               
        except Exception ,excet_str:
            log_print( excet_str)            
            log_public(ERR_017)
            self.m_ERROR_MSG = ERR_017
            self.closeExistDialog() 
            
        return app
    
        
    #013   
    def OpenWiressResourse(self):
        log_print( ">>OpenWiressResourse" )          
        app = None      
        LstIDX =[0] 
        RET = None
        app = self.OpenNetDialogAndSelectIcon(LstIDX)
        time.sleep(1)
        print 'OpenWiressResourse  OpenNetDialogAndSelectIcon',LstIDX
        
        try:
            #Open "resorse" dialog
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE,pause=KEY_PAUSH_SLEEP_TIEM)
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE_RESOSE,pause=KEY_PAUSH_SLEEP_TIEM)
            print 'OpenWiressResourse here'
            RET =app[KEY_NETDIALOG].ListViewWrapper.GetItemRect(LstIDX[0])  
            print  'RET',RET
            #myMenu = [KEY_POP_MENU_RSE]
            #self.PopMenuClick(app,KEY_NETDIALOG,myMenu,RET)   
            #self.wingui.shortcut_keys(['Alt','F'])
            time.sleep(1)
            
            win32api.keybd_event(18,0,0,0)
            win32api.keybd_event(70,0,0,0)
            win32api.keybd_event(70,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
            
            time.sleep(1)
            #self.wingui.shortcut_keys(['R'])
        
            win32api.keybd_event(82,0,0,0)
            win32api.keybd_event(82,0,win32con.KEYEVENTF_KEYUP,0)
          
            time.sleep(3)
            #close "net connect" dialog
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE,pause=KEY_PAUSH_SLEEP_TIEM)
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE_CLOSE,pause=KEY_PAUSH_SLEEP_TIEM) 
            #self.closeExistDialog()  
            #connect to "resorse" dialog
            
            app=application.Application().connect_(title_re=KEY_FIND_WIRESS_NAME_PROPERTY ) 
            print 'OpenWiressResourse here 23'
            time.sleep(1)
        except Exception ,excet_str:
            log_print( excet_str)
            #self.m_ERROR_MSG = ERR_024 
            app = None
        return app
    
    
    #014 
    def OpenWiressDialog(self):  
        log_print( ">>OpenWiressDialog")                 
        app = None
        app = self.OpenWiressResourse()
        
        try:
            #slelect "wiress config" tab
            app[KEY_FIND_WIRESS_NAME_PROPERTY].TabControlWrapper.Select(KEY_RESORSE_DLG_TAB_WIRESS) 
            
            #open "Wierssless" dialog
            app[KEY_FIND_WIRESS_NAME_PROPERTY][KEY_WIRELESS_BUTTON].Click()
            time.sleep(1)
        except Exception ,excet_str:
            log_print( excet_str)
            #self.m_ERROR_MSG = ERR_024 
            app = None
            
        return app
    
    
    #015       
    def SetSecurity(self,strSSIDName,strMod):   
        log_print( ">>SetSecurity")     
        strGetssid = ""
        bFindSSID = False
        
        app = self.OpenWiressResourse()
        if app == None:
            return False
        
        try:
            #slelect "wiress config" tab
            app[KEY_FIND_WIRESS_NAME_PROPERTY].TabControlWrapper.Select(KEY_RESORSE_DLG_TAB_WIRESS) 
            time.sleep(2)
            #check icon
            s = app[KEY_FIND_WIRESS_NAME_PROPERTY].ListViewWrapper.Items()        
            for ct in s:    
                if ct[KEY_NETDIALOG_CONTROL_LV_TEXT].find(strSSIDName) >= 0:
                    bFindSSID = True
                    break

        except Exception ,excet_str:
            log_print( excet_str)             
            log_public(ERR_006)
            self.m_ERROR_MSG = ERR_006
            self.closeExistDialog() 
            return False             
                
        #Select icon
        if bFindSSID == True:
            try:
                s = app[KEY_FIND_WIRESS_NAME_PROPERTY].ListViewWrapper.Items()        
                for ct in s:                 
                    strGetssid = ct[KEY_NETDIALOG_CONTROL_LV_TEXT]
                    app[KEY_FIND_WIRESS_NAME_PROPERTY].ListViewWrapper.Select(strGetssid)           
                    app[KEY_FIND_WIRESS_NAME_PROPERTY].Button5.Click()    #click "delete" button 
                    time.sleep(1)

                app[KEY_FIND_WIRESS_NAME_PROPERTY][KEY_DIALOG_YES].Click()  #click "Yes" button             
                time.sleep(1)      
            except Exception ,excet_str:
                log_print( excet_str)
                log_public(ERR_007)
                self.m_ERROR_MSG = ERR_007
                self.closeExistDialog() 
                return False      
                                             
            app = self.OpenWiressResourse()   
            if app == None:
                return False
            
            try:     
                #slelect "wiress config" tab
                app[KEY_FIND_WIRESS_NAME_PROPERTY].TabControlWrapper.Select(KEY_RESORSE_DLG_TAB_WIRESS) 
                time.sleep(5) #sleep 5 seconds, for wait dialog ready.
            except Exception ,excet_str:
                log_print( excet_str)                
                log_public(ERR_008)
                self.m_ERROR_MSG = ERR_008
                self.closeExistDialog() 
                return False     
            
        #Add SSID        
        #click "Add" button
        try:
            app[KEY_FIND_WIRESS_NAME_PROPERTY][SECURITY_MODEL_BTN_ADD].Click()                              #click "Add" button
            time.sleep(1)        
            app[KEY_FIND_WIRESS_PORPTY].Edit1.SetEditText(strSSIDName)                      #input SSID name
            time.sleep(0.5) 
            app[KEY_FIND_WIRESS_PORPTY].ComboBox1.Select(strMod)                            #select security Model
            time.sleep(0.5) 
            app[KEY_FIND_WIRESS_PORPTY].ComboBox2.Select(SECURITY_MODEL_AES)                #select security key model,default select AES
            time.sleep(0.5) 
            app[KEY_FIND_WIRESS_PORPTY].TabControlWrapper.Select(KEY_FIND_WIRESS_VEN_TAP)   #jump to tab 2.  
            time.sleep(0.5) 
            app[KEY_FIND_WIRESS_PORPTY].ComboBox1.Select(SECURITY_MODEL_PROCTED)            #select item 0. proctected EAP.   
            time.sleep(1) 
            app[KEY_FIND_WIRESS_PORPTY].Button1.Click()                                     #open proctected resourse dialog,by click button "Property"
            time.sleep(1) 

            app[KEY_FIND_WIRESS_PROTECT_EAP].Checkbox0.UnCheck()           #uncheck Verify 
            time.sleep(1) 
            app[KEY_FIND_WIRESS_PROTECT_EAP].Checkbox4.UnCheck()           #uncheck quick Link. 
            time.sleep(1) 
            app[KEY_FIND_WIRESS_PROTECT_EAP].Button0.Click()               #open "EAP MSCHAPv2"  dialog,click button of "config" 
            time.sleep(1) 

            app[KEY_FIND_WIRESS_EAP_MSCHAP].Checkbox1.UnCheck()           #uncheck Auto Login. 
            time.sleep(1) 
            app[KEY_FIND_WIRESS_EAP_MSCHAP][KEY_DIALOG_YES].ClickInput()               #Click "Yes" button     
            time.sleep(1) 
       
            app[KEY_FIND_WIRESS_PROTECT_EAP][KEY_DIALOG_YES].ClickInput()               #Click "Yes" button
            time.sleep(1) 
            app[KEY_FIND_WIRESS_PORPTY][KEY_DIALOG_YES].ClickInput()                   #Click "Yes" button               
            time.sleep(1)  
            app[KEY_FIND_WIRESS_NAME_PROPERTY][KEY_DIALOG_YES].ClickInput()                        #Click "Yes" button
            time.sleep(5)         #wait for dialog ready 
        except Exception ,excet_str:
            log_print( excet_str)
            log_public(ERR_005)
            self.m_ERROR_MSG = ERR_005
            self.closeExistDialog() 
            return False
            
        return True
    
    #016       
           
    def findKeyfromWiressList(self,app,strFind,dstGet):
        log_print( ">>findKeyfromWiressList")    
        bFind = False  
        time.sleep(2)
        strKey = None
        
        try:
            #get list of ssid information
            LS_SSID = app[KEY_WIRELESS].ListBoxWrapper.ItemTexts()  
            
            #print 'LS_SSID:',LS_SSID
            #find SSID
            idx = 0        
            for strSSID in LS_SSID: 
                
                #get key world
                strKey = self.getKey(strSSID)
                if strKey == None:
                    bFind == False
                    break
                
                if strKey ==  strFind:
                #if strSSID.find(strFind) >= 0:
                    bFind = True
                    dstGet[KEY_DSTAY_IDX] = idx
                    dstGet[KEY_DSTAY_CONTS]  = strSSID
                    break
                
                idx+=1                
        except Exception ,excet_str:
            log_print( excet_str)
            log_public(ERR_020)
            self.m_ERROR_MSG = ERR_020 
            self.closeExistDialog()             
            
        if bFind == False:
            log_public(ERR_004)
            self.m_ERROR_MSG = ERR_004 
            self.closeExistDialog() 
            
        return bFind    


    #017    
    def InputPASSWORD(self,strUser,strPASS,waittime=INPUT_TIMEXAX):
        log_print( ">>InputPASSWORD")            
        bFound = False
        iTimeCount = 0
        
        strUser.strip()
        strPASS.strip()
        print 'InputPASSWORD' ,strUser,strPASS
        if strUser == "" or strPASS == "" :
            log_public(ERR_018)
            self.m_ERROR_MSG = ERR_018     
            self.closeExistDialog()         
            return False
        print 'strUser,strPASS not NULL' 
        while bFound == False:
            #time count
            if iTimeCount > waittime:
                print 'input pass timeout'
                log_public(ERR_002)
                self.m_ERROR_MSG = ERR_002 
                self.closeExistDialog() 
                return False
            
            time.sleep(1)
            iTimeCount += 1
            
            #find tooltips
            try:
                print 'KEY_TIP_CLSS'
                app=application.Application().connect_(class_name=KEY_TIP_CLSS) 
                bFound = True
                time.sleep(2)
                break
            except Exception ,excet_str:
                log_print( excet_str)
                #self.m_ERROR_MSG = ERR_024 
                #continue
                break       
                 
        try:        
            #click tip to open input dialog.
            print 'KEY_TIP_CLSS  Click'
            #app[KEY_INPUT_PASSW_TIP].Click()           
            time.sleep(0.5)   
            print 'KEY_TIP_CLSS  connect_'
            app=application.Application().connect_(title_re=KEY_INPUT_PASSW_DIALOG )
            print 'KEY_TIP_CLSS  connect_1111'
            app[KEY_INPUT_PASSW_DIALOG].Edit1.SetEditText(strUser)    #input user name
            time.sleep(0.5)
            app[KEY_INPUT_PASSW_DIALOG].Edit2.SetEditText(strPASS)    #input passaword
            time.sleep(0.5)
            app[KEY_INPUT_PASSW_DIALOG].button1.Click()               #click YES button     
            time.sleep(0.5)    
            print   'KEY_TIP_CLSS  True'
            return True
        except Exception ,excet_str:
            log_print( excet_str)
            log_public(ERR_003)
            self.m_ERROR_MSG = ERR_003 
            self.closeExistDialog() 
            return False            
 
     #018    
    def CheckStatus(self,strPutStarus):
        log_print( ">>CheckStatus")
        time.sleep(3) #wait for dialog ready
        app = None   
        LstIDX =[0] 
        RET = None
        
        app = self.OpenNetDialogAndSelectIcon_check(LstIDX)
        print 'CheckStatus  OpenNetDialogAndSelectIcon',LstIDX
        try:
            #Open "resorse" dialog
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE,pause=KEY_PAUSH_SLEEP_TIEM)
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE_STATUS,pause=KEY_PAUSH_SLEEP_TIEM)
            
            RET =app[KEY_NETDIALOG].ListViewWrapper.GetItemRect(LstIDX[0])  
               
            #myMenu = [KEY_POP_MENU_STU]
            #self.PopMenuClick(app,KEY_NETDIALOG,myMenu,RET)   
            #self.wingui.shortcut_keys(['Alt','F'])
            win32api.keybd_event(18,0,0,0)
            win32api.keybd_event(70,0,0,0)
            win32api.keybd_event(70,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
            time.sleep(1)
            #self.wingui.shortcut_keys(['U'])
            
            win32api.keybd_event(85,0,0,0)
            win32api.keybd_event(85,0,win32con.KEYEVENTF_KEYUP,0)
            
             
            time.sleep(1)
            #close "net connect" dialog
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE,pause=KEY_PAUSH_SLEEP_TIEM)
            #-app[KEY_NETDIALOG].TypeKeys(KEY_NETDIALOG_FILE_CLOSE,pause=KEY_PAUSH_SLEEP_TIEM) 
            self.closeExistDialog()   
            #connect to "resorse" dialog
            app=application.Application().connect_(title_re=KEY_FIND_WIRESS_NAME_STATUS ) 
            time.sleep(1)
            
            
            
            #select tab 1
            app[KEY_FIND_WIRESS_NAME_STATUS].TabControlWrapper.Select(KEY_FIND_WIRESS_NAME_STATUS_TAB) 
            time.sleep(1)
            #get static
            strGetStarus = app[KEY_FIND_WIRESS_NAME_STATUS].Static3.WindowText() 
            print 'strGetStarus:',strGetStarus,strPutStarus
            msg =  'Get: '+ strGetStarus + ' Compare: ' + strPutStarus
            log_print(msg)
            self.total_exec_all = self.total_exec_all  +1 
            if strGetStarus == strPutStarus:
                strGetStarus = app[KEY_FIND_WIRESS_NAME_STATUS].Static5.WindowText()
                print 'strGetStarus:',strGetStarus,self.ssid_user
                msg =  'Get: '+ strGetStarus + ' Compare: ' + strPutStarus
                log_print(msg)
                app[KEY_FIND_WIRESS_NAME_STATUS].Close()
                if strGetStarus.strip() == self.ssid_user.strip():
                    return True
                else:
                    return False
            else:
                log_public(ERR_021)
                self.m_ERROR_MSG = ERR_021             
                app[KEY_FIND_WIRESS_NAME_STATUS].Close()               
                return False
                         
        except Exception ,excet_str:
            log_print( excet_str)
            
            log_public(ERR_022)
            self.m_ERROR_MSG = ERR_022 
            self.closeExistDialog()             
            return False
        
    #019    
    def PopMenuClick(self,app,dlgName,lstMenuName,RET=None,TIMEWAIT=0.5):

        cntX = 0
        cntY = 0
        coords = (0,0)
        tempRet = None
        tempCoord =(0,0)
        try:
            if RET == None:
                
                tempRet = app[dlgName].ListViewWrapper.ClientRect()
                tempCoord = (tempRet.left,tempRet.top)
                
                app[dlgName].ListViewWrapper.RightClickInput(tempCoord)
                time.sleep(TIMEWAIT)
                
                for tempname in lstMenuName:
                                 
                    app.PopupMenu.WrapperObject().MenuItem(tempname).Click()
                    time.sleep(TIMEWAIT) 

            else:

                cntX =  (RET.right - RET.left)/2
                cntY =  (RET.bottom - RET.top)/2

                coords = (RET.left + cntX ,RET.top + cntY )     
                app[dlgName].ListViewWrapper.RightClickInput(coords)
                time.sleep(TIMEWAIT)
                
                for tempname in lstMenuName:  
                    app.PopupMenu.WrapperObject().MenuItem(tempname).Click()
                    time.sleep(TIMEWAIT) 
            return True
        except Exception ,excet_str:
            log_print( excet_str)
            log_public(ERR_023)
            self.m_ERROR_MSG = ERR_023
            return False
        
    #20        
    def getKey(self,strInfoIN):       
        log_print(">>>getKey")
        
        strKeyOUT = None
        idx = -1     
        idx = strInfoIN.find(KEY_WIRESS_LIST_SIGNAL)
        
        if idx == -1:
            return None
        
        strKeyOUT = strInfoIN[0:idx-1]
        
        return strKeyOUT
    
    
    def dic_keycode(self,str_s='A'):
        dic={'Backspace':8,'Tab':9,'Enter':13,'Shift':16,'Ctrl':17,'Alt':18,\
        'Caps Lock':20,'Esc':27,'Spacebar':32,'Page Up':33,'Page Down':34,\
        'End':35,'Home':36,'Left':37,'Up':38,'Right':39,'Down':40,'Insert':45,\
        'Delete':46,'Help':47,'Num Lock':144,\
        'F1':112,'F2':113,'F3':114,'F4':115,'F5':116,'F6':117,'F7':118,'F8':119,'F9':120,'F10':121,'F11':122,'F12':123}
        if len(str_s) == 1:
            msg =  '\n str_s:' + str_s+','+ str(ord(str_s))
            log_print(msg)
            return ord(str_s)
        elif len(str_s)>1:
            if dic.has_key(str_s):
                msg= '\n str_s:'+str_s +' '+ str(dic[str_s])
                log_print(msg)
                return dic[str_s]
    
    def shortcut_keys(self,list_key=[]):
        for x in list_key:
            tmp = self.dic_keycode(x)
            try:
                win32api.keybd_event(tmp,0,0,0)
            except Exception ,excet_str:
                log_print( excet_str)
        for x in list_key:
            tmp = self.dic_keycode(x)
            try:
                win32api.keybd_event(tmp,0,win32con.KEYEVENTF_KEYUP,0)
            except Exception ,excet_str:
                log_print( excet_str)
    
    def find_wind(self,str_app):
        hwnd = win32gui.FindWindow(None, str_app)
        log_print(hwnd) 
        if hwnd>0:
            #win32gui.SetForegroundWindow(hwnd)
            win32gui.MoveWindow(hwnd,40,40,840,640,1)
            time.sleep(1)
            win32gui.MoveWindow(hwnd,0,0,800,600,1)
            #win32gui.ShowWindow(hwnd,win32con.SW_SHOWMAXIMIZED)
            #win_GUI.win_gui().Mousepos_print('20')
            time.sleep(1)
            return True
        return False
    
    def Mouse_LB_D(self,str_app,lb_dx,lb_dy,Flag='1'):
        time.sleep(1)
        tmp=(string.atoi(lb_dx),string.atoi(lb_dy))
        hwnd = win32gui.FindWindow(None, str_app)
        #msg = 'Mouse_LB str_app,hwnd '+str_app+' '+ str(hwnd)
        #log_print(msg)
        if hwnd > 0:
            win32api.SetCursorPos(tmp)
            time.sleep(1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tmp[0], tmp[1]) 
            time.sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tmp[0], tmp[1])
            time.sleep(0.05)
            return True
        return False
    
    
                        
                                                                   
if __name__ == "__main__":
    

    
    mycs = ssid()
    
    for i in range(0,1):
        #1    
        setSSID2 = "zhangqing"
        setSSID1 = "ZJCY_01567f"
        strUSER = "Zoomnet@%*"
        strPASSWORD = "Zoomnet@%*"
        
        #print setSSID
        tmp = 0
        tmp_result = 0 
        while True:
            mycs.SetErrorInfo()
            if tmp_result % 2 ==0:
                setSSID = setSSID1
            else:
                setSSID = setSSID2
            log_print(setSSID)
            
            tmp_result = tmp_result +1
            if mycs.connect(setSSID,strUSER,strPASSWORD) ==True:
                tmp = tmp +1
            
            msg='################ result start ##################'
            log_print(msg)
            msg = 'success is :'+ str(tmp) 
            log_print(msg)
            msg = 'send total:'+str(tmp_result)
            log_print(msg)
            mycs.GetErrorInfo()
            msg='################ result end  ##################'
            log_print(msg)
            if tmp_result > 200:
                break
            time.sleep(10)
        
        time.sleep(1)
