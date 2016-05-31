# -*- coding: gb18030 -*- 
#-----------------------------------------------------------------------------
# Name:        rw_Excel_FLOW.py
# Purpose:     read infromation from Excel.this excel record operation of Web page.
#
# Author:      <gongke>
#
# Created:     2013/02/06
# RCS-ID:      $Id: rw_Excel_FLOW.py $
# Copyright:   (c) 2006
# Licence:     <0.1.0>
#-----------------------------------------------------------------------------
# Version events
# <0.1.0> Create 
# <0.1.1> Add 'bCA'-parameter for OperateACWebPage(). Judge weather have CA authentication.
# <0.1.2> Add OperateACWebPage() to rw_Excel_FLOW module.
# <0.1.3> Add function --GetErrorInfo(). 2013/02/28
# <0.1.4> Modify for chinese of listbox. 2013/03/04
# <0.1.5> upgrade for upload CSV file. 2013/03/07 
# <0.1.6> upgrade for submit opration. 2013/03/12
# <0.1.7> upgrade for click two time of Web dialog. 2013/03/14
# <0.1.8> upgrade for quick .2013/03/21,zhang dong
# <0.1.9> update for inclease checkPageIsBusy() function. 2013/03/25,zhang dong
# <1.1.10> update for compare two value from table of web. add MainCheckTableOne(),MainCheckTableTwo(),2013/04/08,zhang dong
# <1.1.11> update for close IE Broswer window. Add ManiCloseIEWindow(),2013/04/10,zhang dong.
# <1.1.12> Add AP_login() for AP login.2013/05/17,gongke.
#<1.1.13> and check_Landdlg for check web  2014/01/28 gongke
#import sys
#sys.coinit_flags = 0 # Important for multithreading,set flag to 0.

import xlrd
#import xlwt

from PAM30 import PAMIE
import time
import thread 
import cModalPopUp
from WtLog import log_public
import string
import win32gui
import win32api
import win32con
import os
import sys
from global_parame import *
from public import *
import win32com.client
from win_GUI import * 
import pythoncom
from pywinauto import *
from selenium import webdriver
from selenium import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import win32com.client
import unittest, time, re,random
import urllib
import chardet
import shutil
import traceback

#---------------------------------------
KEY_SHEETNAME = 'SheetName'
KEY_URL = 'URL'
KEY_ASSIST = 'ASSIST'
KEY_CONTROLTYPE = 'ControlType'
KEY_CONTROLNAME = 'ControlName'
KEY_CONTROLVALUE = 'ControlValue'
#---------------------------------------
#list
KEY_STNAME_INDEX = 0
KEY_URL_INDEX = 1
KEY_HEADPART = 3
#---------------------------------------
#excel
KEY_HEAD = 'HEADER'
KEY_END = 'END'
KEY_A_COL = 0
KEY_B_COL = 1
KEY_C_COL = 2
KEY_D_COL = 3

#---------------------------------------
KEY_ROW = 'rowx'
KEY_COL = 'coly'

#---------------------------------------

KEY_URL_OPEN_FLAG = 'http'
KEY_SELENIUM_FLAG = 'SELENIUM'
#-----------------------------

KEY_SELENIUM_FIND_ELEMENT_BY_ID='BYID'
KEY_SELENIUM_FIND_ELEMENT_BY_NAME='BYNAME'
KEY_SELENIUM_FIND_ELEMENT_BY_XPATH='XPATH'
KEY_SELENIUM_FIND_ELEMENT_BY_CSS='CSS'
KEY_SELENIUM_FIND_ELEMENT_BY_CLASSNAME='CLASS'
KEY_SELENIUM_DIALOG ='DIALOG'
KEY_SELENIUM_IDENTIFY='IDENTIFY'

#--------------
#Error List
ERR_FILE_OPENFAIL_0001 = 'error:Open excel file failed.Please check file whether exist or Excel application installed./ErrorCode-Excel-0001'
ERR_EXCEL_URL_0002 = 'error:not find KeyWord-URL,Please check format of file./ErrorCode-Excel-0002'
ERR_EXCEL_ASSIST_0003 = 'error:not find KeyWord-NO,Please check format of file./ErrorCode-Excel-0003'
ERR_EXCEL_CONTROLTYPE_0004 = 'error:not find KeyWord-ControlType,Please check format of file.check whether can find END mark./ErrorCode-Excel-0004'
ERR_EXCEL_CONTROLNAME_0005 = 'error:not find KeyWord-ControlName,Please check format of file.check whether can find END mark./ErrorCode-Excel-0005'
ERR_EXCEL_CONTROLVALUE_0006 = 'error:not find KeyWord-ControlValue,Please check format of file.check whether can find END mark./ErrorCode-Excel-0006'
ERR_EXCEL_URL_VALUE_0007 ='error: not find value of URL,Please check format of file./ErrorCode-Excel-0007'
ERR_EXCEL_NO_VALUE_0008 = 'error: not find value of NO,Please check format of file./ErrorCode-Excel-0008'
ERR_EXCEL_CONTROLTYPE_VALUE_0009 = 'error: not find value of ControlType,Please check format of file./ErrorCode-Excel-0009'
ERR_EXCEL_CONTROLNAME_VALUE_0010 = 'error: not find value of ControlValue,Please check format of file./ErrorCode-Excel-0010'
ERR_TABLE_OPENFAIL_0011 = 'error: Open excel file failed,Please check path of file is right or check sheetname./ErrorCode-Excel-0010'

#--------------------------------------
#Web Control
#Wait Event Type
KEY_WEB_WAIT_EVENT_TIME = 'time'
KEY_WEB_WAIT_EVENT_DIALOG = 'dialog'
#--------------------------------------
KEY_IE_VERSION = 'd=document.createElement("div");d.id = "iversion";d.style.display="none";\
d.innerHTML=navigator.appVersion;document.body.appendChild(d);'
#---------------------------------------
#Web Control Type
KEY_WEB_TYPE_SEARCH = 'SEARCH'
KEY_WEB_TYPE_SEARCHBOX = 'SEARCHBOX'
KEY_WEB_TYPE_TEXTBOX  = 'TEXTBOX'
KEY_WEB_TYPE_CHECKBOX  = 'CHECKBOX'
KEY_WEB_TYPE_LISTBOX  = 'LISTBOX'
KEY_WEB_TYPE_BUTTON  = 'BUTTON'
KEY_WEB_TYPE_WAIT  = 'WAIT'
KEY_WEB_TYPE_JAVASCRIPT  = 'JAVASCPIPT'
KEY_WEB_TYPE_JAVASCRIPT_GET ='JAVASCPIPTGET'
#KEY_WEB_TYPE_GROUP_CHECKBOX = 'GROUP_CHECKBOX'

KEY_WEB_TYPE_OPEN_FILE = "OPENFILE"
KEY_WEB_TYPE_OPEN_DEFAULT = "input"
KEY_WEB_TYPE_OPEN_DEFAULT_Name = "name"
KEY_WEB_TYPE_SUBMIT = "SUBMIT"
KEY_WEB_TYPE_DEFAULT  = "input"
KEY_WEB_TYPE_SUBMIT_TYPE = "type"
KEY_WEB_TYPE_COMPARE_TABLE_VALUE_ONE = "CMPTB-1"
KEY_WEB_TYPE_COMPARE_TABLE_VALUE_TWO = "CMPTB-2"

KEY_WEB_TYPE_RADIOBUTTON ='RADIO'

KEY_WEB_TYPE_GETRADIOSELECTED ='GETRADIOSELECTED'
KEY_WEB_TYPE_GETRADIOVALUES ='GETRADIOVALUES'


KEY_WEB_TYPE_GETTABLETEXT='GETTABLETEXT'
KEY_WEB_TYPE_GETTABLEDATA='GETTABLEDATA'
KEY_WEB_TYPE_GETTABLEROWINDEX='GETTABLEROWINDEX'

KEY_WEB_TYPE_GETTEXTBOXSVALUE='GETTEXTBOXSVALUE'
KEY_WEB_TYPE_GETTEXTBOXVALUE='GETTEXTBOXVALUE'
KEY_WEB_TYPE_GETCHECKBOXCHECKED_CYKJ  = 'GETCHECKBOXCHECKED_ONU'
KEY_WEB_TYPE_GETCHECKBOXVALUE  = 'GETCHECKBOXVALUE'
KEY_WEB_TYPE_GETLISTBOXVALUES  = 'GETLISTBOXVALUES'
KEY_WEB_TYPE_GETLISTBOXSELECTED = 'GETLISTBOXSELECTED'
KEY_WEB_TYPE_GETFORMVALUE='GETFORMVALUE'
KEY_WEB_TYPE_GETPAGE  = 'GETPAGE'
KEY_WEB_TYPE_GETIMAGEVALUE_CYKJ='GETIMAGEVALUE_PORTCONFIG'

KEY_WEB_TYPE_FIND_ElEMENT ='ELEMENT'
KEY_TABLE_ROW = "row"
KEY_TABLE_COLUMN ="column"
KEY_WEB_TYPE_CLOSE_IE = "CLOSEIE"

KEY_WEB_TYPE_SENDKEY='DIALOGBUTTON'
KEY_WEB_TYPE_BUTTON_TAGKEYWORD ='BUTTONTAGKEYWORD'

KEY_WEB_TYPE_DIALOG_OP ='MULTIDIALOG'
#---------------------------------------
KEY_WEB_TYPE_OPEN_DLG_TITLE = "WindowsName"
KEY_WEB_TYPE_OPEN_DLG_TEXTVALUE = "TextValue"
KEY_WEB_TYPE_OPEN_DLG_BUTTON = "ButtonName" 
KEY_WEB_TYPE_OPEN_DLG_DST_KEY = "KEY"
KEY_WEB_TYPE_OPEN_DLG_DST_VALUE = "VALUE"


#---------------------------------------
KEY_URL = 'URL'
KEY_ASSIST = 'ASSIST'
KEY_CONTROLTYPE = 'ControlType'
KEY_CONTROLNAME = 'ControlName'
KEY_CONTROLVALUE = 'ControlValue'
KEY_URL_NONE = 'NONE'
KEY_URL_WAITEVENT_START = 'START'
KEY_URL_WAITEVENT_END = 'END'
KEY_GROUP = 'G'
KEY_COMMENT = 'C'

KEY_USERNAME ='USERNAME'
KEY_PASSWD='PASSWD'

FLAG_ONU = False

IE_DEBU = True

#--------------------------------------
#AP login information
LOGIN_USERNAME_ZNAP = 'admin'
LOGIN_PASSWORD_ZNAP = 'password'
LOGIN_USERNAME_GONGJIN = 'admin'
LOGIN_PASSWORD_GONGJIN = 'admin'

#--------------------------------------
#control web error information list
#format is Error-WebControl-XXXX-Who-Value-Where-What-trouble shoot.
WEB_ERR_NO_0001 = 'Can not Open Web page./Please check this:Can you ping AC success? Can you Open web page by manual success? The IP address written at excel is right?/ErrorCode-WebControl-0001/URL/Value is '
WEB_ERR_NO_0002 = 'Can not get IE version./Please check this:If IE installed? If IE run normally?/Error-WebControl-0002-/IEVersion/Value is '
WEB_ERR_NO_0003 = 'Can not set Text Box./Please check this:Check ExcelData,If the ControlName is right?/ErrorCode-WebControl-0003/Who/Value is '
WEB_ERR_NO_0004 = 'Can not set Check Box/Please check this:Check ExcelData,If the ControlName or ControlValue is right?/ErrorCode-WebControl-0004/Who/Value is '
WEB_ERR_NO_0005 = 'Can not select List Box/Please check this:Check ExcelData,If the ControlName or ControlValue is right?/ErrorCode-WebControl-0005/Who/Value is '
WEB_ERR_NO_0006 = 'Can not click button/Please check this:Check ExcelData,If the ControlName is right?/ErrorCode-WebControl-0006/Who/Value is '
WEB_ERR_NO_0007 = 'Can not wait The Event./Please check this:Check ExcelData,If the format of ControlName is right?if you wait dialogyou need fill right format.eg,dialog$WindowsName=MyDial&&ButtonName=Yes/ErrorCode-WebControl-0007/Who/Value is '
WEB_ERR_NO_0008 = 'Can not enable java script./Please check this: Check ExcelData,If the ControlName is right?/ErrorCode-WebControl-0008/Who/Value is '
WEB_ERR_NO_0009 = 'GET GROUP ERROR/Please check this: check ExcelData,If the control value is right?/ErrorCode-WebControl-0009/Who/Value is '''
WEB_ERR_NO_0010 = 'Can not find Element./Please check this: Check ExcelData,If the ControlName is right?/ErrorCode-WebControl-0010/Who/Value is '
WEB_ERR_NO_0011 = 'Can not find Element for submit button./Please check this: Check ExcelData,If the ControlName is right?/ErrorCode-WebControl-0011/Who/Value is '
WEB_ERR_NO_0012 ='controlname or controlvalue is empty./ErrorCode-WebControl-0012'
WEB_ERR_NO_0013 ='Can not get table text value.please check control value is right./ErrorCode-WebControl-0013'
WEB_ERR_NO_0014 ='the format of Controlvalue is wrong./ErrorCode-WebControl-0014'
WEB_ERR_NO_0015 ='controlname or controlvalue is empty./ErrorCode-WebControl-0015'
WEB_ERR_NO_0016 ='compare value is different./ErrorCode-WebControl-0016'
WEB_ERR_NO_0017 ='Can not get table text value.please check control value is right./ErrorCode-WebControl-0017'
WEB_ERR_NO_0018 ='Can not close IE windows,please check IE windows title whether ritht./ErrorCode-WebControl-0018'
WEB_ERR_NO_0019 = 'AP login error.Please check whether FlowName parameter is correct./ErrorCode-WebControl-0019'  
WEB_ERR_NO_0020 = 'can not get hwnd of AP login window.Please check if there is an AP login window./ErrorCode-WebControl-0020'
WEB_ERR_NO_0021 = 'you input wrong username or password.Please check it./ErrorCode-WebControl-0021'
WEB_ERR_NO_0022 = 'MultiDialog operation error.Please check it./ErrorCode-WebControl-0022'
ENCODE_DECODE = 'gb18030'
DEFAULT_RUN = 10 

                               
                                           
class Class_RW_Excel:   


    m_ERROR_MSG = "no error"    #recoard error message.
    m_Group_Idx = -1
    m_Obj_WaitDialog_Cancel = 0
    m_bSTOP = False
    m_CmpLst = []              #storage compare value.
    #-----------------------------------------------------------------------------
    # Name:        GetErrorInfo -get error information
    # ruturn:      return string.the string is error message. if no error happen ,it is "no error".
    # Author:      <gongke>
    #
    # Created:     2013/02/28
    # RCS-ID:      $Id: rw_Excel_FLOW.py $
    #-----------------------------------------------------------------------------
    
    def __init__(self):
        self.myobj = win_gui()
        self.global_p = {}       
        self.test_NG_error=''  
        self.ap_flag = 0
        self.hwndnew = 0
        self.Onu_login_Flag = 0 
        self.Wait_Dialog_time =5
        self.Land_Dialog_check_total = 8
        
            
    
    def GetErrorInfo(self):   
        #log_print(self.m_ERROR_MSG )     
        return self.m_ERROR_MSG         
   
    def SetStop(self):
        self.m_bSTOP = True


        
    #-----------------------------------------------------------------------------
    # Name:        readWebPage
    # Purpose:     read information of web page to be control by python.
    # parameter:   filePath-the Excel path,include excel file name.
    #              FlowName-the flow name. at C coloumn of Excel file. eg:'CONFIG'.
    #              bCA -String type. tow value 'CAON','CAOFF','CAON' mean have CA authentication.'CAOFF' mean not have CA authentication
    # Author:      <gongke>
    #
    # Created:     2013/02/06
    # RCS-ID:      $Id: rw_Excel_FLOW.py $
    # Copyright:   (c) 2006
    # Licence:     <your licence>
    #-----------------------------------------------------------------------------
    def setWebPage(self,filePath,FlowName,bCA):
        log_print( 'setWebPage fuction')
        print filePath,FlowName,bCA
        version_file = find_parentpath()+'\\auto_conf\\version.ini'
        tmp_Land_Dialog_check_total=read_ini(version_file,'Land_Dialog_check_total','ACweb Debug')
        tmp_Wait_Dialog_time =read_ini(version_file,'tmp_Wait_Dialog_time','ACweb Debug')
        if len(tmp_Land_Dialog_check_total.strip())>0:
            self.Land_Dialog_check_total = string.atoi(tmp_Land_Dialog_check_total.strip())
        if len(tmp_Wait_Dialog_time.strip())>0:
            self.Wait_Dialog_time = string.atof(tmp_Wait_Dialog_time.strip())
        self.hwndnew = 0
        dic_flowname = {'ZNAP':1,'GONGJIN':2,'OTHER':3,'ONU':4} 
        flowname = FlowName
        if dic_flowname.has_key(flowname.split('_')[-1].strip()) == True:
            self.ap_flag = 1
            #print 'AP web.'
        else:
            self.ap_flag = 0
            #print 'AC web.'
        
        p_path1 = os.path.abspath(sys.argv[0])
        tmp_global_file ='\\global\\global_param.xls'
        findstr = 'Simu'
        path_parent = Getfindpath(p_path1,findstr)
        global_file = path_parent + tmp_global_file
        self.read_global_param(global_file)
        
        myPath = filePath  
        log_print(myPath)       
        lst = []
        obj_book = 0
        obj_table = 0
        
        LOOPMAX = 0
        shttName =''
        ret = 0 #return value form function
        
        obj_book =  self.OpenFile(myPath)
        #print obj_book
        #print obj_book.sheet_names()
        for sheet_name in obj_book.sheet_names():
             
            if sheet_name == u'0-ACPAGE' :
                obj_table = obj_book.sheet_by_name(sheet_name) 
                break            
        print obj_table
        if obj_table == 0 :
            log_public(ERR_TABLE_OPENFAIL_0011)
            self.m_ERROR_MSG = ERR_TABLE_OPENFAIL_0011
            return False
        
        #while loop
        bNeedReadHead = True
        NEXTNODE = True

        myDictNodeCur = {'rowx':'','coly':''}
        myDictNodeNext = {'rowx':'','coly':''}
        dct_Cell={} #dicitionary
        while NEXTNODE == True:
            
            #read START
            if bNeedReadHead == True:
                if self.ReadFlowHeader(obj_table,FlowName,myDictNodeNext) == False:
                    return  False
                bNeedReadHead = False           
            
            if (myDictNodeNext[KEY_ROW] == -1) & ( myDictNodeNext[KEY_COL] == -1):
                NEXTNODE = False
                continue
            
            myDictNodeCur.update(myDictNodeNext)
            #read Page
            if self.ReadFlowPage(obj_table,myDictNodeCur,myDictNodeNext,lst) == False:
                return False
            
            if (myDictNodeNext[KEY_ROW] == -1) & (myDictNodeNext[KEY_COL] == -1):
                NEXTNODE = False
                continue 
        #print lst   #need dele    
        log_print( 'web execl,lst:')
        log_print( lst)
        if self.OperateACWebPage(FlowName,bCA,lst) == False:
            return False
            
        del lst    
        return True
        
    #read Flowchart header            
    def ReadFlowHeader(self,obj_table,FlowName,dctNode):
        log_print( 'ReadFlowHeader fuction')
        myFlowName = ''
        myDict = {'rowx':'','coly':''}
        nrows = obj_table.nrows
        for rows in range(0,nrows):
            dct_Combn={}
            myHeader = obj_table.cell(rows,KEY_B_COL).value
            myHeader.strip()
            if myHeader != '':
                if myHeader == 'FLOWHEADER':
                     myFlowName = obj_table.cell(rows,KEY_C_COL).value
                     print 'FlowName:',FlowName,' myFlowName:',myFlowName
                     if myFlowName == FlowName:
                         strOrg =  obj_table.cell(rows+1,KEY_C_COL).value
                         print 'strOrg:',strOrg
                         strOrg.strip()
                         self.transform(strOrg,dctNode)                         
                         return True                    
        
        return False
    
    
    
    #read page information
    def ReadFlowPage(self,obj_table,dctCurNode,dctNextNode,lst):
        log_print( 'ReadFlowPage fuction')
        lstSub = []
        strNextNode = ''    
      
        ret = self.ReadWebPgURL(obj_table,dctCurNode,lstSub)
        if ret == False:
            return False
        else:
            strNextNode = ret
            

        ret = self.CheckWebPgControl(obj_table,dctCurNode)            
        if ret == False:
            return False
            
        ret = self.ReadWebPgControl(obj_table,dctCurNode,lstSub)
        if ret == False:
            return False    
            
        lst.append(lstSub)
            
        self.transform(strNextNode,dctNextNode)

               

    #open excel file,get object of work book.
    def OpenFile(self,filePath):
        log_print( 'OpenFile fuction')
        try:
            obj_book = xlrd.open_workbook(filePath)
            return obj_book
        except:
            log_public(ERR_FILE_OPENFAIL_0001)            
            self.m_ERROR_MSG = ERR_FILE_OPENFAIL_0001
    
    #read URL
    def ReadWebPgURL(self,obj_table,dctCurNode,lst):
        log_print( 'ReadWebPgURL fuction')
        strNextNode = ''
        myURL =''      
        row = dctCurNode[KEY_ROW]
        col = dctCurNode[KEY_COL]
        
        #Get Keyword URL 
        myURL = obj_table.cell(row+1,col).value
        myURL.strip()
        
        #check Keyword URL 
        if cmp(myURL,KEY_URL) == -1:
            log_public( ERR_EXCEL_URL_0002)
            self.m_ERROR_MSG = ERR_EXCEL_URL_0002
            return False
          
        #Get URL Value    
        myURLValue = obj_table.cell(row+1,col+1).value 
        myURLValue.strip()      
        #test value.can not be empty.
        if myURLValue =='':
            log_public(ERR_EXCEL_URL_VALUE_0007)
            self.m_ERROR_MSG = ERR_EXCEL_URL_VALUE_0007
            return False
            
        dct_URL = {KEY_URL:myURLValue}
        lst.append(dct_URL)            
        
        #get NextNode
        strNextNode = obj_table.cell(row,col+3).value
        return strNextNode

    #check controlType,controlName,controlValue format    
    def CheckWebPgControl(self,obj_table,dctCurNode):
        log_print( 'CheckWebPgControl fuction')
        row = dctCurNode[KEY_ROW]+2
        col = dctCurNode[KEY_COL]        

        myASSIST = obj_table.cell(row,col).value
        myASSIST.strip()
        myControlType = obj_table.cell(row,col+1).value
        myControlType.strip()

        myControlName = obj_table.cell(row,col+2).value
        myControlName.strip()
        myControlValue = obj_table.cell(row,col+3).value
        myControlValue.strip()
        
        if cmp(myASSIST,KEY_ASSIST) == -1:
            log_public(ERR_EXCEL_ASSIST_0003)   
            self.m_ERROR_MSG = ERR_EXCEL_ASSIST_0003       
            return False
            
        if cmp(myControlType,KEY_CONTROLTYPE) == -1:             
            log_public(ERR_EXCEL_CONTROLTYPE_0004)
            self.m_ERROR_MSG = ERR_EXCEL_CONTROLTYPE_0004
            return False
        
        if cmp(myControlName,KEY_CONTROLNAME) == -1:               
            log_public( ERR_EXCEL_CONTROLNAME_0005)
            self.m_ERROR_MSG = ERR_EXCEL_CONTROLNAME_0005
            return False
        
        if cmp(myControlValue,KEY_CONTROLVALUE) == -1:
           log_public( ERR_EXCEL_CONTROLVALUE_0006)
           self.m_ERROR_MSG = ERR_EXCEL_CONTROLVALUE_0006
           return False           

    #read controlType,controlName,controlvalue    
    def ReadWebPgControl(self,obj_table,dctCurNode,lst):
        log_print( 'ReadWebPgControl fuction')
        print 'ReadWebPgControl'
        row = dctCurNode[KEY_ROW]+3
        col = dctCurNode[KEY_COL]      
        
        nrows = obj_table.nrows  
        timesBlank = 0 
        
        
        for rows in range(row,nrows):
            dct_Combn={}
            mySubASSIST = str(obj_table.cell(rows,col).value)
            mySubASSIST.strip()
            if mySubASSIST == KEY_END:
                return True
            
            dct_ASSIST ={KEY_ASSIST:mySubASSIST}
            dct_Combn.update(dct_ASSIST)
            
            mySubControlType = str(obj_table.cell(rows,col+1).value)
            mySubControlType.strip()
            if mySubControlType =='':
                log_public(ERR_EXCEL_NO_VALUE_0008)
                self.m_ERROR_MSG = ERR_EXCEL_NO_VALUE_0008
                return False
            dct_CONTROLTYPE= {KEY_CONTROLTYPE:mySubControlType}         
            dct_Combn.update(dct_CONTROLTYPE)
                    
            mySubControlName = str(obj_table.cell(rows,col+2).value.encode(ENCODE_DECODE)) 
            mySubControlName.strip()
            if mySubControlName =='':
                log_public(ERR_EXCEL_CONTROLNAME_VALUE_0010)
                self.m_ERROR_MSG = ERR_EXCEL_CONTROLNAME_VALUE_0010
                return False
            dct_CONTROLNAME = {KEY_CONTROLNAME:mySubControlName}
            dct_Combn.update(dct_CONTROLNAME)
                    
            
            mySubControlValue = obj_table.cell(rows,col+3).value
            if isinstance(mySubControlValue,float) == False & isinstance(mySubControlValue,int) == False:
                
                #mySubControlValue = obj_table.cell(rows,col+3).value.encode('gb18030')  #2013/03/04,gongke,if the string have chinese use unicode,else use encode('gb18030')
                
                if self.isChinese(mySubControlValue) == True:
                    mySubControlValue = obj_table.cell(rows,col+3).value
                else:
                    mySubControlValue = obj_table.cell(rows,col+3).value.encode(ENCODE_DECODE)
                
            else:
                mySubControlValue = str(mySubControlValue)
                mySubControlValue = mySubControlValue.encode(ENCODE_DECODE)
                mySubControlValue = mySubControlValue[0:mySubControlValue.find('.')]


            dct_CONTROLVALUE = {KEY_CONTROLVALUE:mySubControlValue}
            dct_Combn.update(dct_CONTROLVALUE)                
            
            lst.append(dct_Combn)            
            del dct_Combn
            
        return True
    
    
    
    def isChinese(self,strCheck):   
        log_print( 'isChinese fuction')     
        hz_yes = False   
        for  ch  in  strCheck:
              
            if  isinstance(ch, unicode):
                  
                if ch >= u'\u4e00' and ch<=u'\u9fa5': #have chinese.
                    hz_yes = True   
                    break   
            else :  
                continue
                        
        return hz_yes
    
    #translate form ,eg:B3,tha is :row is 3,col is B, then change to number row=2,col=1    
    def transform(self,strOrg,dctRowCol):
        log_print( 'transform fuction')
        myStrOrg = strOrg
        lstColch = []
        lstColn = []        
        lstRown = []
        if (strOrg == 'NULL')|(strOrg == ''):
           dctRowCol[KEY_ROW] = -1
           dctRowCol[KEY_COL] = -1
           return
        #check string
        self.checkString(strOrg)
        #get Col
        for ch in myStrOrg:
           if ch.isalpha() == True:               
               lstColch.append(ch)
           else:
               break
        
        for ndex in range(len(lstColch)):
                           
            lstColn.append( self.strToNum(lstColch[ndex]))
            
        
       #get col
        dctRowCol[KEY_COL] = self.Cal26(lstColn)
        
                
       #get Row        
        for ch in myStrOrg:
           if ch.isalpha() == True:
               continue
           else:
               lstRown.append(int(ch))
        
       #get row
        dctRowCol[KEY_ROW] = self.Cal10(lstRown)        
     
        
               
        
    #calculate 26    
    def Cal26(self,lst):
        sum = 0
        for x in range(len(lst)):
            sum  = sum  + lst.pop()*(26**x)
        
        sum = sum - 1
        return sum            
        
    #calculate 10   
    def Cal10(self,lst):
        sum = 0    
        for x in range(len(lst)):
            sum  = sum  + lst.pop()*(10**x)
        
        sum = sum - 1
        return sum          
        
        
    #check sting format    
    def checkString(self,string):
        nSetpOld =0
        nSetpNew =0
        
         
        idx = 0
        if string.isalnum() == True:
            
            for ch in string:                
                if (ch.isalpha() == False)&(idx == 0):                    
                    return False                  
                idx = idx + 1
            return True
        
        else:
            return False
          
          
          
    #change chat to numbers of every coloumn      
    def strToNum(self,ch):

        if (ch == 'A') | (ch == 'a'):return 1
        if (ch == 'B') | (ch == 'b'):return 2
        if (ch == 'C') | (ch == 'c'):return 3
        if (ch == 'D') | (ch == 'd'):return 4
        if (ch == 'E') | (ch == 'e'):return 5
        if (ch == 'F') | (ch == 'f'):return 6
        if (ch == 'G') | (ch == 'g'):return 7
        if (ch == 'H') | (ch == 'h'):return 8
        if (ch == 'I') | (ch == 'i'):return 9        
        if (ch == 'J') | (ch == 'j'):return 10
        if (ch == 'K') | (ch == 'k'):return 11
        if (ch == 'L') | (ch == 'l'):return 12
        if (ch == 'M') | (ch == 'm'):return 13
        if (ch == 'N') | (ch == 'n'):return 14
        if (ch == 'O') | (ch == 'o'):return 15
        if (ch == 'P') | (ch == 'p'):return 16
        if (ch == 'Q') | (ch == 'q'):return 17        
        if (ch == 'R') | (ch == 'r'):return 18    
        if (ch == 'S') | (ch == 's'):return 19           
        if (ch == 'T') | (ch == 't'):return 20  
        if (ch == 'U') | (ch == 'u'):return 21                
        if (ch == 'V') | (ch == 'v'):return 22   
        if (ch == 'W') | (ch == 'w'):return 23           
        if (ch == 'X') | (ch == 'x'):return 24           
        if (ch == 'Y') | (ch == 'y'):return 25           
        if (ch == 'Z') | (ch == 'z'):return 26           
        
        return -1                

#------------------------------------------Excel code end-------------------------------
    

    #-----------------------------------------------------------------------------
    # Name:        OperateACWebPage
    # Purpose:     control Web page
    # Parameters:  bCA- True(defalut value) the web page have CA authentication dialog,False not have CA authentication.
    #              lst -the list to hold information. this is input vlaue.
    # Author:      <chenshengcong>
    #
    # Created:     2013/01/30
    # RCS-ID:      $Id: CrtlACWeb.py $
    # Copyright:   (c) 2006
    # Licence:     <your licence>
    #-----------------------------------------------------------------------------
    
    
    def read_global_param(self,filename ='E:\\Simu_server\\global\\global_param.xls',sheetname='global'):
        testexcel = readexcel(filename,sheetname)
        self.global_p = testexcel.Excel_read()
        msg = self.global_p
        log_print(msg)
        
    def Replace_global_multi_list(self,list=[]):
        tmp_list =[]
        tmp_l=[]
        for x in list:
            tmp_l = self.Replace_global_param_dic(x)
            tmp_list.append(tmp_l)
        return tmp_list
            
    def Replace_global_param_dic(self,list=[]):
        #print '********** Replace_global_param_dic before**********:'
        #log_print(list)
        tmp_list_op = []
        for dic_t in list:
            #print dic_t
            dic_list_keys = dic_t.keys()
            dic_list_values=dic_t.values()
            tmp_list = self.Replace_global_param(dic_list_values)
            dic_tt = {}
            for i in range(len(dic_list_keys)):
                print dic_list_keys[i],tmp_list[i]
                dic_tt[dic_list_keys[i]] = tmp_list[i]
            tmp_list_op.append(dic_tt)
        #print '********** Replace_global_param_dic ___after  **********:'
        #log_print(tmp_list_op)
        return tmp_list_op
 
    def Replace_global_param(self,list=[]):
        #print '********** Replace_global_param **********'
        tmp_list_op = []
        for x in list:
            if x.find('%%')>-1:
                list_global = x.split('%%')
                tmp_t = 0
                tmp_str =''
                #print list_global
                for tmp_str_p in list_global:
                    if tmp_t % 2 == 0:
                        tmp_str= tmp_str + tmp_str_p
                    else:
                        #print '*******here********',tmp_str_p
                        if self.global_p.has_key(tmp_str_p)==True:
                            tmp_str = tmp_str + self.global_p[tmp_str_p]
                        else:
                            msg = 'the global file excel not find the global_parma:'+tmp_str_p
                            self.test_NG_error = msg
                            log_print(msg)
                    tmp_t = tmp_t + 1
                #print tmp_str
                tmp_list_op.append(tmp_str)
            else:
                tmp_list_op.append(x)
        return tmp_list_op
    
    def ie_close(self,ie,stime = 5):
        time.sleep(stime)
        ie.quit()
        kill_program()
        
    def OperateACWebPage(self,FlowName,bCA,lst):
        
        #print '********* OperateACWebPage fuction before111***********\n:'
        #log_print(lst)
        
        self.test_NG_error = ''
        kill_program()
        
        lst = self.Replace_global_multi_list(lst)
        #log_print('********* OperateACWebPage fuction _Replay_global111: ************\n')
        #log_print(lst)
        dstURL={}
        if self.test_NG_error.find('the global file')>-1:
            log_print('not fined the global file')
            return False
        try:
            pythoncom.CoInitialize()
            ie = PAMIE()
            nVer = self.getIEVersion(ie)  
            msg = 'IE VERSION :' + str(nVer)
            log_print(msg)
        except Exception ,exc_str:
            log_print(exc_str) 
            return False     
        if nVer == -1:
            log_public(WEB_ERR_NO_0002+dstURL[KEY_URL])
            self.m_ERROR_MSG = WEB_ERR_NO_0002+dstURL[KEY_URL]
            return False                      
        KillCA = bCA
        lstLen = len(lst)
        i = 0
        while i < lstLen:    
            lstSub=[]
            lstSub.extend(lst[i])
            if self.m_bSTOP == True:
                self.ie_close(ie)
            lstSubLen = len(lstSub)
            j = 0    
            while j < lstSubLen:    
                if self.m_bSTOP == True:
                    self.ie_close(ie)
                if j == 0 :
                    dstURL={}
                    dstURL.update(lstSub[j])                
                    if  dstURL[KEY_URL].split(KEY_URL_OPEN_FLAG)[0].upper().find(KEY_SELENIUM_FLAG)>-1:
                        try:
                            if self.SeleniumFuction(dstURL,lstSub)==False:
                                return False
                        except Exception,e:
                            log_print(e)
                            return False
                        j =lstSubLen
                    elif dstURL[KEY_URL]!=KEY_URL_NONE:
                        try:     
                            log_print( '******navigate *****')    
                            print 'dstURL[KEY_URL]:',dstURL[KEY_URL]           
                            ret = ie.navigate(dstURL[KEY_URL])
                            #time.sleep(1)
                        except Exception ,exc_str:
                            log_print( '******navigate except*****')
                            log_print(exc_str)
                            self.ie_close(ie)
                            log_public(WEB_ERR_NO_0001+dstURL[KEY_URL])
                            self.m_ERROR_MSG = WEB_ERR_NO_0001+dstURL[KEY_URL]
                            return False
                        
                        '''
                        if IE_DEBU==True:
                            msg_print=  '@@@@@@@@@@@@@@@@@@@ open IE_DEBUG start @@@@@@@@@@@@@@@@@@@' 
                            log_print(msg_print)
                            msg_print =  ie.()
                            #log_print(msg_print)
                            msg_print=  '@@@@@@@@@@@@@@@@@@@ open IE_DEBUG end @@@@@@@@@@@@@@@@@@@' 
                            log_print(msg_print)
                        '''
                        
                        if KillCA == 'CAON':
                            if nVer == 8  or nVer==9 or nVer==10:                                        
                                time.sleep(1)
                                ret = ie.clickLink('overridelink')
                                if ret == False:
                                    self.ie_close(ie)
                                    log_public(WEB_ERR_NO_0001+dstURL[KEY_URL])
                                    self.m_ERROR_MSG = WEB_ERR_NO_0001+dstURL[KEY_URL]
                                    return False      
                                KillCA = False #not need to kill next time open URL                                                                
                            elif nVer == 6:
                                time.sleep(1)
                                KillCA = False   
                            
                            #AP login operation.
                            time.sleep(1)
                            print 'sleep 1s'
                            if self.ap_flag == 1:
                                if FlowName.split('_')[-1]=='ONU':
                                    print 'FlowName onu '
                                    self.Onu_login_Flag =1
                                    if self.Onu_login(FlowName) == False:
                                        self.Onu_login_Flag = 0
                                        return False
                                elif self.AP_login(FlowName) == False:
                                    return False
                        time.sleep(self.Wait_Dialog_time)
                        app_f = findwindows.find_windows(class_name_re = "#32770")
                        
                        num_wait = 0
                        app_f = []
                        
                        while True:
                            try:
                                #print 'upperr:',FlowName.split('_')[-1].upper()
                                if FlowName.split('_')[-1].upper()!='ONU':
                                    break
                                app_f = findwindows.find_windows(title_re = u"连接到")
                                #print 'app_f:',app_f
                                if len(app_f)<0:
                                    num_wait+=1
                                    time.sleep(0.5)
                                
                            except Exception,e:
                                num_wait+=1
                                time.sleep(0.5)
                                pass
                            if num_wait>=self.Land_Dialog_check_total  or len(app_f)>0:
                                break
                            else:
                                num_wait+=1
                        if len(app_f)>0:
                            if self.check_Landdlg(app_f,lst[i]) ==False:
                               return False
                                                                                                               
                else:
                    
                    #get line_operation.
                    dstComb = {}
                    dstComb.update(lstSub[j])
                    log_print( '******dstComb *****')
                    log_print( dstComb)
                    #if 'ASSIST' have '//',This line_operation will be ignore.
                    #log_print(dstComb[KEY_ASSIST])
                    if dstComb[KEY_ASSIST]== KEY_COMMENT or dstComb[KEY_ASSIST]== KEY_USERNAME or dstComb[KEY_ASSIST]== KEY_PASSWD:      
                        j+=1                  
                        continue
                    
                    try:
                        #dispatch line_operation.include kinds(set text box, set check box,select list box,...)
                        log_print('******dispatch line_operation.include kinds try********* ')
                        Value = dstComb[KEY_CONTROLTYPE]
                        #log_print(Value)
                        if Value == KEY_WEB_TYPE_SEARCH:
                            log_print(KEY_WEB_TYPE_SEARCH) 
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE])
                            log_print ('searching begin!!')
                            if ie.searchKeyword(dstComb[KEY_CONTROLVALUE])==False:
                                log_print('search keyword is Falsse')
                                if self.checkPageIsBusy(ie) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-2
                                    break
                                return False
                            print ('searching end!!!')
                            #return True
                        if Value == KEY_WEB_TYPE_TEXTBOX:
                            #self.getTextAreasValue(ie)   
                            log_print(KEY_WEB_TYPE_TEXTBOX)   
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE])                  
                            if ie.setTextBox(dstComb[KEY_CONTROLNAME], dstComb[KEY_CONTROLVALUE]) == False:
                                log_print('setTextBox is False')
                                
                                if self.checkPageIsBusy(ie) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-2   
                                    break
                    
                                self.ie_close(ie)
                                log_public(WEB_ERR_NO_0003+dstComb[KEY_CONTROLNAME])
                                self.m_ERROR_MSG = WEB_ERR_NO_0003+dstComb[KEY_CONTROLNAME]
                                return False
                        
                        elif Value==KEY_WEB_TYPE_GETTEXTBOXVALUE:
                            log_print(KEY_WEB_TYPE_GETTEXTBOXVALUE)   
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE])  
                            attribute = 'value'
                            find_str = dstComb[KEY_CONTROLVALUE]
                            #print 'attribute:',attribute
                            #print 'find_str:',find_str
                            info = ie.getTextBoxValue(dstComb[KEY_CONTROLNAME],attribute)
                            #print 'info:',info
                            log_print('GetValue:'+info)
                            if info.find(find_str)>-1:
                                log_print('the keyword:'+find_str + ' find')
                            else:
                                log_print('the keyword:'+find_str + ' not find')
                                self.ie_close(ie)
                                return False
                                
                        elif Value==KEY_WEB_TYPE_GETPAGE:
                            log_print(KEY_WEB_TYPE_GETPAGE)   
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE]) 
                            info = ie.pageGetText()
                            log_print('GetPage:'+info)
                            if info.find(dstComb[KEY_CONTROLNAME])<0:
                                log_print('Error,not find the keyword:'+ dstComb[KEY_CONTROLNAME]+'!!!!')
                                return False
                            log_print('True,find the keyword:'+ dstComb[KEY_CONTROLNAME])
                            
                        elif Value==KEY_WEB_TYPE_GETLISTBOXSELECTED:
                            log_print(KEY_WEB_TYPE_GETLISTBOXSELECTED)   
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE])
                            info = ie.getListBoxSelected(dstComb[KEY_CONTROLNAME])
                            if info[0] != dstComb[KEY_CONTROLVALUE]:
                                log_print('Error,find listbox:'+ dstComb[KEY_CONTROLNAME]+ ' Value selected:'+info[0]+ ' Not:'+dstComb[KEY_CONTROLVALUE]+'!!!!')
                                return False
                            log_print('True,find listbox:'+ dstComb[KEY_CONTROLNAME]+ ' Value selected:'+dstComb[KEY_CONTROLVALUE]+'!!!!')
                            
                        elif Value==KEY_WEB_TYPE_GETCHECKBOXCHECKED_CYKJ:
                            log_print(KEY_WEB_TYPE_GETCHECKBOXCHECKED_CYKJ)
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE])
                            if ie.getCheckBoxesChecked_Cykj_onu(dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE])==False:
                                log_print('Error,find the checkbox  '+dstComb[KEY_CONTROLNAME]+'checked Not:'+dstComb[KEY_CONTROLVALUE]+'!!!!!')
                                return False
                            log_print('True,find the checkbox  '+dstComb[KEY_CONTROLNAME]+' checked:'+dstComb[KEY_CONTROLVALUE])
                                
                        elif Value==KEY_WEB_TYPE_GETIMAGEVALUE_CYKJ:
                            log_print(KEY_WEB_TYPE_GETIMAGEVALUE_CYKJ)
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE])
                            if ie.getImagesValue_CYKJ_onu(dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                                log_print('Error,find the PageImage :'+dstComb[KEY_CONTROLVALUE]+'!!!!!')
                                return False
                            log_print('True,find the PageImage :'+dstComb[KEY_CONTROLVALUE])
                            
                        elif Value== KEY_WEB_TYPE_CHECKBOX:
                            log_print(KEY_WEB_TYPE_CHECKBOX)
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE])
                            
                            if self.MainCheckBox(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                                log_print('MainCheckBox is False')
                                if self.checkPageIsBusy(ie) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-2 
                                    break                                
                                
                                self.ie_close(ie)
                                log_public(WEB_ERR_NO_0004+dstComb[KEY_CONTROLNAME])
                                self.m_ERROR_MSG = WEB_ERR_NO_0004+dstComb[KEY_CONTROLNAME]
                                return False

                        elif Value == KEY_WEB_TYPE_LISTBOX:
                            log_print(KEY_WEB_TYPE_LISTBOX)
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE])
                            if self.MainListBox(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                                log_print('MainListBox is False')
                                if self.checkPageIsBusy(ie) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-2 
                                    break                                

                                self.ie_close(ie)
                                log_public(WEB_ERR_NO_0005+dstComb[KEY_CONTROLNAME])
                                self.m_ERROR_MSG = WEB_ERR_NO_0005+dstComb[KEY_CONTROLNAME]
                                return False 
                            
                        
                            
                        elif Value ==KEY_WEB_TYPE_BUTTON_TAGKEYWORD:
                            log_print(KEY_WEB_TYPE_BUTTON_TAGKEYWORD)
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE])
                            #tag = dstComb[KEY_CONTROLVALUE].split('//')[0].strip()
                            #keyword=dstComb[KEY_CONTROLVALUE].split('//')[-1].strip()
                            if ie.button_clicktagkeyword(dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) ==False:
                                log_print('MainButton is False')
                                if self.checkPageIsBusy(ie) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-2                                 
                                    break                               
                                self.ie_close(ie)
                                log_public(WEB_ERR_NO_0006+dstComb[KEY_CONTROLNAME])    
                                self.m_ERROR_MSG =  WEB_ERR_NO_0006+dstComb[KEY_CONTROLNAME]                      
                                return False
                                
                        elif Value == KEY_WEB_TYPE_BUTTON:  
                            log_print(KEY_WEB_TYPE_BUTTON)
                            log_print(dstComb[KEY_CONTROLNAME])                         
                            if self.MainButton(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME]) == False:
                                log_print('MainButton is False')
                                if self.checkPageIsBusy(ie) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-2                                 
                                    break                               

                                self.ie_close(ie)
                                log_public(WEB_ERR_NO_0006+dstComb[KEY_CONTROLNAME])    
                                self.m_ERROR_MSG =  WEB_ERR_NO_0006+dstComb[KEY_CONTROLNAME]                      
                                return False

                        elif Value == KEY_WEB_TYPE_WAIT:
                            log_print(KEY_WEB_TYPE_WAIT)
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE])
                            if self.waitEvent(dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                                log_print('waitEvent is False')
                                if self.checkPageIsBusy(ie) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-1
                                    break                           
     
                                self.ie_close(ie)
                                log_public(WEB_ERR_NO_0007+dstComb[KEY_CONTROLNAME])
                                self.m_ERROR_MSG =  WEB_ERR_NO_0007+dstComb[KEY_CONTROLNAME]
                                return False
                        elif Value ==KEY_WEB_TYPE_DIALOG_OP:
                            log_print(KEY_WEB_TYPE_DIALOG_OP)
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE])
                            if self.MultiDialog_op(dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                                
                                self.ie_close(ie)
                                self.m_ERROR_MSG =  WEB_ERR_NO_0022
                                log_print(self.m_ERROR_MSG)
                                return False
                            
                            
                        elif Value == KEY_WEB_TYPE_JAVASCRIPT_GET:
                            log_print(KEY_WEB_TYPE_JAVASCRIPT_GET)
                            log_print(dstComb[KEY_CONTROLNAME])
                            if self.MainJavaScriptGet(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                                log_print('MainJavaScriptGet is False')
                                if self.checkPageIsBusy(ie) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-1
                                    break       
                                self.ie_close(ie)
                                log_public(WEB_ERR_NO_0008+dstComb[KEY_CONTROLNAME])   
                                self.m_ERROR_MSG = WEB_ERR_NO_0008+dstComb[KEY_CONTROLNAME]
                                return False
                            
                        elif Value == KEY_WEB_TYPE_JAVASCRIPT: 
                            
                            log_print(KEY_WEB_TYPE_JAVASCRIPT)
                            log_print(dstComb[KEY_CONTROLNAME])
                            if self.MainJavaScript(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                               log_print('MainJavaScript is False')
                               if self.checkPageIsBusy(ie) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-1
                                    break                           

                               self.ie_close(ie)
                               log_public(WEB_ERR_NO_0008+dstComb[KEY_CONTROLNAME])   
                               self.m_ERROR_MSG = WEB_ERR_NO_0008+dstComb[KEY_CONTROLNAME]
                               return False
                        
                        #modify.not use Group check box. Delete foloow code. by gongke,2013/03/12
                        #elif Value == KEY_WEB_TYPE_GROUP_CHECKBOX:
                        #    if  self.GetGoupCheckBoxIndex(ie,dstComb[KEY_CONTROLNAME]) == False:
                        #       log_public(WEB_ERR_NO_0009+dstComb[KEY_CONTROLNAME])  
                        #       self.m_ERROR_MSG = WEB_ERR_NO_0009 + dstComb[KEY_CONTROLNAME]
                        #       return False   
                           
                        elif Value == KEY_WEB_TYPE_OPEN_FILE:
                            log_print(KEY_WEB_TYPE_OPEN_FILE)
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(KEY_WEB_TYPE_OPEN_DEFAULT)
                            log_print(KEY_WEB_TYPE_OPEN_DEFAULT_Name)
                            if ie.clickElement(ie.findElement(KEY_WEB_TYPE_OPEN_DEFAULT, KEY_WEB_TYPE_OPEN_DEFAULT_Name,dstComb[KEY_CONTROLNAME])) == False:
                                log_print('clickElement is False')
                                if self.checkPageIsBusy(ie) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-1
                                    break                                
                                
                                self.ie_close(ie)
                                log_public(WEB_ERR_NO_0010+dstComb[KEY_CONTROLNAME])
                                self.m_ERROR_MSG = WEB_ERR_NO_0010+dstComb[KEY_CONTROLNAME]
                                return False
                            
                        elif Value == KEY_WEB_TYPE_SUBMIT:  
                            log_print(KEY_WEB_TYPE_SUBMIT)
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(KEY_WEB_TYPE_DEFAULT)
                            log_print(KEY_WEB_TYPE_SUBMIT_TYPE)                        
                            if ie.clickElement(ie.findElement(KEY_WEB_TYPE_DEFAULT, KEY_WEB_TYPE_SUBMIT_TYPE,dstComb[KEY_CONTROLNAME])) == False:
                                log_print('clickElement is False')
                                if self.checkPageIsBusy(ie) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-1
                                    break                                
                                
                                self.ie_close(ie)
                                log_public(WEB_ERR_NO_0011+dstComb[KEY_CONTROLNAME])
                                self.m_ERROR_MSG = WEB_ERR_NO_0011+dstComb[KEY_CONTROLNAME]
                                return False   
                            
                        #get Value 2 of Table    
                        elif Value == KEY_WEB_TYPE_COMPARE_TABLE_VALUE_ONE:
                            log_print(KEY_WEB_TYPE_COMPARE_TABLE_VALUE_ONE)
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE]) 
                            if self.MainCheckTableOne(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                                log_print('MainCheckTableOne is False')
                                del self.m_CmpLst
                                self.ie_close(ie)
                                return False
                        
                        #get Value 2 of Table and compare.
                        elif Value == KEY_WEB_TYPE_COMPARE_TABLE_VALUE_TWO:
                            log_print(KEY_WEB_TYPE_COMPARE_TABLE_VALUE_TWO)
                            log_print(dstComb[KEY_CONTROLNAME])
                            log_print(dstComb[KEY_CONTROLVALUE]) 
                            if self.MainCheckTableTwo(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                                log_print('MainCheckTableTwo is False')
                                del self.m_CmpLst
                                self.ie_close(ie)
                                return False  
                            
                        #close IE windows(broswer).    
                        elif Value == KEY_WEB_TYPE_CLOSE_IE:
                             log_print(KEY_WEB_TYPE_CLOSE_IE)
                             log_print(dstComb[KEY_CONTROLNAME])
                             if self.MainCloseIEWindow(dstComb[KEY_CONTROLNAME]) == False:
                                log_print('MainCloseIEWindow is False')
                                self.ie_close(ie)
                                return False   
                        elif Value ==KEY_WEB_TYPE_SENDKEY:
                            log_print(KEY_WEB_TYPE_SENDKEY)
                            log_print(dstComb[KEY_CONTROLNAME])
                            if self.Dialog_Button(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                                log_print('Dialog_Button is False')
                                del self.m_CmpLst
                                self.ie_close(ie)
                                return False  
                        elif Value ==KEY_WEB_TYPE_RADIOBUTTON:
                            log_print(KEY_WEB_TYPE_RADIOBUTTON)
                            log_print(dstComb[KEY_CONTROLNAME])
                            if ie.setRadioButton(dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE])==False:
                                self.ie_close(ie)
                                return False
                        elif Value ==KEY_WEB_TYPE_FIND_ElEMENT:
                            log_print(KEY_WEB_TYPE_FIND_ElEMENT)
                            log_print(dstComb[KEY_CONTROLNAME])
                            if self.Find_element(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                                log_print('Find_element is False')
                                del self.m_CmpLst
                                self.ie_close(ie)
                                return False  
                            
                    except Exception ,exc_str:
                        log_print('******dispatch line_operation.include kinds except********* ')
                        #log_print(exc_str)
                        #self.ie_close(ie) 
                        #return False
                        if self.checkPageIsBusy(ie) == True:
                            log_print('checkPageIsBusy reutrn True')
                            i = i-2                   
                            break                        
                        #log_print('******KEY_ASSIST except not quit********* ')
                        self.ie_close(ie)    
                        return False
                    
                j+=1 #for command loop
                
            i+=1    #for page loop           
        #close ie after operation.                
        self.ie_close(ie)
           
    
    
        
        
    def SeleniumFuction(self,dstURL,lstSub):
        print 'SeleniumFuction'
        dic_selenium ={KEY_SELENIUM_FIND_ELEMENT_BY_NAME:'find_element_by_name',
                       KEY_SELENIUM_FIND_ELEMENT_BY_ID:'find_element_by_id',
                       KEY_SELENIUM_FIND_ELEMENT_BY_XPATH:'find_element_by_xpath',
                       KEY_SELENIUM_FIND_ELEMENT_BY_NAME:'find_elements_by_class_name'}
        url = dstURL[KEY_URL].split(KEY_SELENIUM_FLAG)[-1].strip()
        try:
            driver = webdriver.Firefox()
            #driver = webdriver.Ie()
            driver.get(url)
        except Exception,e:
            log_print(e)
            return False
        lstSubLen  = len(lstSub) 
        j = 1    
        while j < lstSubLen:
            dstComb = {}
            dstComb.update(lstSub[j])
            print 'dstComb12222:',dstComb
            if dstComb[KEY_ASSIST]== KEY_COMMENT or dstComb[KEY_ASSIST]== KEY_USERNAME or dstComb[KEY_ASSIST]== KEY_PASSWD:      
                j+=1                  
                continue
            #if dstComb.has_key(KEY_ASSIST):
            '''
            print 'dstComb333:',dstComb,'len:',len(dstComb[KEY_ASSIST].strip())
            if len(dstComb[KEY_ASSIST].strip())>0:
                oper_seleium = dic_selenium(dstComb[KEY_ASSIST].strip())
            else:
                oper_seleium =''
            '''
            oper_seleium = dstComb[KEY_ASSIST]
            try:
                Value = dstComb[KEY_CONTROLTYPE]
                log_print(Value)
                print '2222KEY_CONTROLTYPE'
                if Value == KEY_WEB_TYPE_TEXTBOX :
                    log_print(KEY_WEB_TYPE_TEXTBOX)   
                    log_print(dstComb[KEY_CONTROLNAME])
                    log_print(dstComb[KEY_CONTROLVALUE])  
                    #if self.selenium_Textbox(driver,oper_seleium,dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE])==False:
                    if self.selenium_Textbox_op(driver,oper_seleium,dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE])==False:
                        return False
                elif Value == KEY_WEB_TYPE_BUTTON :
                    log_print(KEY_WEB_TYPE_BUTTON)   
                    log_print(dstComb[KEY_CONTROLNAME])
                    log_print(dstComb[KEY_CONTROLVALUE])
                    #if self.selenium_Button(driver,oper_seleium,dstComb[KEY_CONTROLNAME])==False:
                    if self.selenium_Button_op(driver,oper_seleium,dstComb[KEY_CONTROLNAME])==False:
                        return False  
                elif Value == KEY_WEB_TYPE_WAIT:
                    log_print(KEY_WEB_TYPE_WAIT)
                    log_print(dstComb[KEY_CONTROLNAME])
                    log_print(dstComb[KEY_CONTROLVALUE])
                    if self.waitEvent(dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                        return False
                elif Value == KEY_WEB_TYPE_JAVASCRIPT: 
                    log_print(KEY_WEB_TYPE_JAVASCRIPT)
                    log_print(dstComb[KEY_CONTROLNAME])
                    if self.selenium_Javascript(dstComb[KEY_CONTROLNAME])==False:
                        return False
                elif Value == KEY_SELENIUM_DIALOG:
                    log_print(KEY_SELENIUM_DIALOG)
                    log_print(dstComb[KEY_CONTROLNAME])
                    if self.selenium_Dialog(driver,dstComb[KEY_CONTROLNAME])==False:
                        return False
                
                elif Value == KEY_WEB_TYPE_LISTBOX:
                    log_print(KEY_WEB_TYPE_LISTBOX)
                    log_print(dstComb[KEY_CONTROLNAME])
                    if self.selenium_ListBox_op(driver,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE])==False:
                        return False
            except Exception,e:
                log_print(e)
                
                print traceback.format_exc()
                return False
            j+=1
        driver.close()
    
    def selenium_ListBox_op(self,driver,key_assert,name,value_set):
        while True:
            try:
                #driver.select(driver.find_element_by_name(name),value=value_set)
                print 'name:',name
                m = driver.find_element_by_name(name)
                value = "//option[@value='" +value_set.strip() +"']"
                m.find_element_by_xpath(value).click()
                #print 'm:',m
                break
            except Exception,e:
                msg ='not find_element_by_name do find_element_by_id: ' + name
                log_print(msg)
                pass
            try:
                #driver.select(driver.find_element_by_id(name),value=value_set)
                print 'name:',name
                m = driver.find_element_by_id(name)
                value = "//option[@value='" +value_set.strip() +"']"
                m.find_element_by_xpath(value).click()
                break
            except Exception,e:
                msg ='not find_element_by_id do find_element_by_xpath'
                log_print(msg)
                pass
            try:
                #driver.select(driver.find_element_by_xpath(name),value=value_set)
                print 'name:',name
                m = driver.find_element_by_xpath(name)
                value = "//option[@value='" +value_set.strip() +"']"
                m.find_element_by_xpath(value).click()
                
                break
            except Exception,e:
                msg ='not find the element:'+name
                log_print(msg)
                driver.close()
                return False
        return True
            
    def selenium_Javascript(self,driver,name):
        try:
            driver.execute_script(name)
        except Exception,e:
            log_print(e)
            driver.close()
            return False
        return True
    
    def selenium_Dialog(self,driver,name):
        try:
            dialog = driver.switch_to_alert()
            if name.strip()=='YES':
                dialog.accept()
            else:
                return True
        except Exception,e:
            log_print(e)
            driver.close()
            return False
        return True
    
    
    
    def selenium_Textbox_op(self,driver,oper_seleium,name,value):
        while True:
            try:
                driver.find_element_by_name(name).clear()
                driver.find_element_by_name(name).send_keys(value)
                break
            except Exception,e:
                msg ='not find_element_by_name do find_element_by_id: ' + name
                log_print(msg)
                pass
            try:
                driver.find_element_by_id(name).clear()
                driver.find_element_by_id(name).send_keys(value)
                break
            except Exception,e:
                msg ='not find_element_by_id do find_element_by_xpath'
                log_print(msg)
                pass
            try:
                driver.find_element_by_xpath(name).clear()
                
                driver.find_element_by_xpath(name).send_keys(value)
                break
            except Exception,e:
                msg ='not find the element:'+name
                log_print(msg)
                driver.close()
                return False
        return True
    
    def selenium_Textbox(self,driver,oper_seleium,name,value):
        try:
            if oper_seleium ==KEY_SELENIUM_FIND_ELEMENT_BY_NAME:
                driver.find_element_by_name(name).clear()
                driver.find_element_by_name(name).send_keys(value)
            elif oper_seleium ==KEY_SELENIUM_FIND_ELEMENT_BY_ID:
                driver.find_element_by_id(name).clear()
                driver.find_element_by_id(name).send_keys(value)
            elif oper_seleium ==KEY_SELENIUM_FIND_ELEMENT_BY_XPATH:
                driver.find_element_by_xpath(name).clear()
                driver.find_element_by_xpath(name).send_keys(value)
        except Exception,e:
            log_print(e)
            print traceback.format_exc()
            driver.close()
            return False
        return True
    
    
    def selenium_Button_op(self,driver,oper_seleium,name):
        while True:
            try:
                driver.find_element_by_name(name).click()
                break
            except Exception,e:
                msg ='not find_element_by_name do find_element_by_id: ' + name
                log_print(msg)
                pass
            try:
                driver.find_element_by_id(name).click()
                break
            except Exception,e:
                msg ='not find_element_by_name do find_element_by_id: ' + name
                log_print(msg)
                pass
            try:
                if name.find('//')<0:
                    name='//button[@type=\'' + name +'\']'
                driver.find_element_by_xpath(name).click()
                break
            except Exception,e:
                msg ='not find the element:'+name
                driver.close()
                return False
        return True
    
    def selenium_Button(self,driver,oper_seleium,name):
        try:
            if oper_seleium ==KEY_SELENIUM_FIND_ELEMENT_BY_NAME:
                driver.find_element_by_name(name).click()
            elif oper_seleium ==KEY_SELENIUM_FIND_ELEMENT_BY_ID:
                driver.find_element_by_id(name).click()
            elif oper_seleium ==KEY_SELENIUM_FIND_ELEMENT_BY_XPATH:
                driver.find_element_by_xpath(name).click()
        except Exception,e:
            log_print(e)
            driver.close()
            return False
        return True
    
    def Find_element(self,obj_ie,strassist,name,value):
        if strassist== KEY_WEB_TYPE_LISTBOX:
            find_e = obj_ie.findElement('select',strassist,'')
           
    def GetGoupCheckBoxIndex(self,obj_ie,strControlName):
        
        myValues=[]
        
        #find every check box.and select the last one.
        myCheckBoxes = obj_ie.getCheckBoxes()
        for checkbox in myCheckBoxes[:]:
            if checkbox.getAttribute('name').find(strControlName)>=0:
                    myValues.append(checkbox.getAttribute('name'))
        
        indx = len(myValues)
        indxF = indx-1
        self.m_Group_Idx = indxF #set index of group from check box. this value will be use later.
        
        return True
    
    #button operation main function
    def MainButton(self,obj_ie,strAssist,strControlName):
        
        myControlName = strControlName
        print 'myControlName:',myControlName
        if strAssist == KEY_GROUP:
            myControlName = self.findButtonChangeId(obj_ie,strControlName)
        
        if obj_ie.clickButton(myControlName) == False:
            return False
        
        return True
                      
    #when the button at some group,we need change index.
    def findButtonChangeId(self,obj_ie,strControlName,Flag_Onu=False):
        
       strL = 'id_'
       strR = '_'
       
       if self.m_Group_Idx == -1:
           return False
       
       strGroupIndex = str(self.m_Group_Idx) 
       strNewControlName = ''
       if Flag_Onu==False:
           idx = strControlName.find('(')
           if idx > 0:
               strControlName = strControlName[0:idx]
           strNewControlName = strL+strControlName+strR+strGroupIndex
       else:
           idx = strControlName.find('(')
           if idx > 0:
               strControlName = strControlName[0:idx]
           strNewControlName = strL+strControlName+strR+strGroupIndex
       print 'strNewControlName:',strNewControlName
       return strNewControlName 
   
    
    #java operation main function      
    def MainJavaScriptGet(self,obj_ie,strAssist='',strControlName='',strControlValue=''):
        myControlName = strControlName
        print 'strControlValue:',strControlValue
        try:
            info =obj_ie.executeJavaScript_Get(myControlName)
            if info ==None:
                return False
            else:
                log_print(info)
                #print '111:',info.decode(ENCODE_DECODE)
                #print '222:',info.decode(ENCODE_DECODE).find(strControlValue)
                if info.find(strControlValue)>-1:
                    log_print('****** find the keyword:'+strControlValue+' in the PageWeb ****** ')
                    return True
                else:
                    log_print('****** Not find the keyword:'+strControlValue+' in the PageWeb ******')
                    return False
                print '111',info.encode(ENCODE_DECODE)
                #print 're.findall:',re.findall(strControlValue,info)
        except Exception,e:
            log_print(e)
            return False
        return True
    
    def MainJavaScript(self,obj_ie,strAssist='',strControlName='',strControlValue=''):
        
        myControlName = strControlName
        if strAssist ==KEY_GROUP:
            myControlName = self.findJavaScriptChangeId(strControlName)
        elif strAssist=='TRUE' or strAssist=='FALSE':
            if obj_ie.executeJavaScript(myControlName,strControlValue.split(','),strAssist) == False:
                return False
            else:
                return True
        try:
           if obj_ie.executeJavaScript(myControlName) == False:
                return False
        except Exception,e:
            log_print(e)
            return False
        
        return True
    
    #when the java script at some group,we need change index.   
    def findJavaScriptChangeId(self,strControlName):
        
       strL = '('
       strR = ')'
       
       if self.m_Group_Idx == -1:
           return False
       
       strGroupIndex = str(self.m_Group_Idx) 
       strNewControlName = ''
       
       idx = strControlName.find('(')
       if idx > 0:
           strControlName = strControlName[0:idx]  
            
       strNewControlName = strControlName+strL+strGroupIndex+strR

       return strNewControlName   
        
    #List box operation main function              
    def MainListBox(self,obj_ie,strAssist,strControlName,strControlValue):
        
        myControlName = strControlName
        if strAssist == KEY_GROUP:
            myControlName = self.findListBoxChangeId(strControlName)
        log_print('listbox item:')
        log_print(obj_ie.getListBoxItemCount(myControlName))
        if obj_ie.getListBoxItemCount(myControlName)==0:
            msg = myControlName  +  ' is 0 hasnot item'
            log_print(msg)
            return False
        
        if obj_ie.selectListBox(myControlName, strControlValue) == False:
            print 'selectListBox is False'
            return False
        time.sleep(1)
        return True
    
    #when the list box at some group,we need change index.       
    def findListBoxChangeId(self,strControlName):
        
       strL = '['
       strR = ']'
       if self.m_Group_Idx == -1:
           return False
       
       strGroupIndex = str(self.m_Group_Idx) 
       strNewControlName = ''
        
       idx = strControlName.find('[')
       if idx > 0:
           strControlName = strControlName[0:idx]           
  
       strNewControlName = strControlName+strL+strGroupIndex+strR
       
       return strNewControlName
            
    #check box operation main function            
    def MainCheckBox(self,obj_ie,strAssist,strControlName,strControlValue):
        
        if strControlValue == '':
            return False
        
        myControlName = strControlName
        if strAssist == KEY_GROUP:
            myControlName = self.findCheckBoxChangeId(obj_ie,strControlName)
        
        if obj_ie.setCheckBox(myControlName,int(strControlValue)) == False:
            return False        
        
        return True           
             
             
    #when the check box at some group,we need change index.               
    def findCheckBoxChangeId(self,obj_ie,strControlName):
        strNewControlName = ''
        
        myValues=[]
        
        #find every check box.and select the last one.
        myCheckBoxes = obj_ie.getCheckBoxes()
        for checkbox in myCheckBoxes[:]:
            if checkbox.getAttribute('id').find(strControlName)>=0:
                    myValues.append(checkbox.getAttribute('id'))
        
        indx = len(myValues)
        indxF = indx-1
        self.m_Group_Idx = indxF #set index of group from check box. this value will be use later.
        for n in range(indx):
            if myValues[n].find(str(indxF))>=0:
                strNewControlName = myValues[n]
                break            
    
        return strNewControlName
    
   
    
    #wait event main function
    def MultiDialog_op_new(self,EventName,TimeOut):
        dic_keyword = {'type':None,'index':None,'title':None,'child':None,'rect':None,'indexrect':None,
                       'writetext':'test'}
        gui =  win_gui()
        num = 0
        hwnd = 0 
        
        while num<DEFAULT_RUN:
            time.sleep(1)
            num = num + 1
            try:
                hwnd = gui.find_main_window(EventName)
                if hwnd >0:
                    break
            except Exception ,e:
                pass
            
        if hwnd<=0:
            return False
        for x in TimeOut.split(';'):
            att = x.strip().split('=')[0].strip()
            attval = x.strip().split('=')[-1].strip()
            if dic_keyword.has_key(att):
                dic_keyword[att] = attval.encode(ENCODE_DECODE)

        att = dic_keyword['type']
        attval = dic_keyword['title']
        attrect = dic_keyword['rect']
        attindexrect = dic_keyword['indexrect']
        attindex = dic_keyword['index']
        attchild = dic_keyword['child']
        att_writevalue = dic_keyword['writetext']
        hchild = 0 
        
        try:      
            if attval!=None:
                ctrl_list = findControls(hwnd,wantedText =attval,wantedClass = att)
                if attindex ==None:
                    if len(ctrl_list) ==1:
                        hchild = ctrl_list[0]
                    else:
                        for x in ctrl_list:
                            if win32gui.GetWindowText(x).strip() == attval.strip():
                                hchild = x
                                break 
                        if  hchild<=0:
                            return False
                else:
                    index = string.atoi(attindex)-1
                    hchild = ctrl_list[index]
            else:
                ctrl_list = findControls(hwnd,wantedClass = att)
                ctrl_list = del_relist(ctrl_list)
                if attindex ==None:
                    if len(ctrl_list) ==1:
                        hchild = ctrl_list[0]
                    else:
                        for x in ctrl_list:
                            if win32gui.GetWindowText(x).strip() == attval.strip():
                                hchild = x
                                break 
                        if  hchild<=0:
                            return False
                else:
                    index = string.atoi(attindex)-1
                    hchild = ctrl_list[index]
            if hchild <=0:
                return False
            if dic_keyword['type']=='Button':
                clickButton(hchild)
            elif dic_keyword['type']=='Edit':
                if file_exist(att_writevalue)==True:
                    os.remove(att_writevalue)
                setEditText(hchild,text=att_writevalue)
                
        except Exception,e:
            log_print(e)
            return False
    
        return True 
    
    def MultiDialog_op(self,EventName,TimeOut):
        dic_keyword = {'type':None,'index':None,'title':None,'child':None,'rect':None,'indexrect':None,
                       'writetext':'test'}
        gui =  win_gui()
        num = 0
        hwnd = 0 
        while num<DEFAULT_RUN:
            time.sleep(1)
            num = num + 1
            try:
                hwnd = gui.find_main_window(EventName)
                if hwnd >0:
                    break
            except Exception ,e:
                pass
            
        if hwnd<=0:
            return False
        for x in TimeOut.split(';'):
            att = x.strip().split('=')[0].strip()
            attval = x.strip().split('=')[-1].strip()
            if dic_keyword.has_key(att):
                dic_keyword[att] = attval.encode(ENCODE_DECODE)

        att = dic_keyword['type']
        attval = dic_keyword['title']
        attrect = dic_keyword['rect']
        attindexrect = dic_keyword['indexrect']
        attindex = dic_keyword['index']
        attchild = dic_keyword['child']
        att_writevalue = dic_keyword['writetext']
        hchild = 0 
        
        try:      
            if attval!=None:
                ctrl_list = findControls(hwnd,wantedText =attval,wantedClass = att)
                if attindex ==None:
                    if len(ctrl_list) ==1:
                        hchild = ctrl_list[0]
                    else:
                        for x in ctrl_list:
                            if win32gui.GetWindowText(x).strip() == attval.strip():
                                hchild = x
                                break 
                        if  hchild<=0:
                            return False
                else:
                    index = string.atoi(attindex)-1
                    hchild = ctrl_list[index]
            else:
                ctrl_list = findControls(hwnd,wantedClass = att)
                ctrl_list = del_relist(ctrl_list)
                if attindex ==None:
                    if len(ctrl_list) ==1:
                        hchild = ctrl_list[0]
                    else:
                        for x in ctrl_list:
                            if win32gui.GetWindowText(x).strip() == attval.strip():
                                hchild = x
                                break 
                        if  hchild<=0:
                            return False
                else:
                    index = string.atoi(attindex)-1
                    hchild = ctrl_list[index]
            if hchild <=0:
                return False
            if dic_keyword['type']=='Button':
                clickButton(hchild)
            elif dic_keyword['type']=='Edit':
                if file_exist(att_writevalue)==True:
                    os.remove(att_writevalue)
                setEditText(hchild,text=att_writevalue)
                
        except Exception,e:
            log_print(e)
            return False
    
        return True 
        
        
    def waitEvent(self,EventName,TimeOut):
        #print 'waitEvent fuction:',EventName, TimeOut
        strTemp = EventName
        
        if strTemp.find('$') != -1:
            strTemp = strTemp[0:strTemp.find('$')]
       
        if strTemp == KEY_WEB_WAIT_EVENT_TIME:
            self.timeEvent(TimeOut)
            return True
        elif strTemp ==KEY_WEB_WAIT_EVENT_DIALOG:
            if TimeOut == KEY_URL_WAITEVENT_START:
                self.m_Obj_WaitDialog_Cancel = self.dialogEventStart(EventName)
                if self.m_Obj_WaitDialog_Cancel == False:
                    return False
                
            elif TimeOut == KEY_URL_WAITEVENT_END:
                self.dialogEventEnd(self.m_Obj_WaitDialog_Cancel)
            
            return True
        
    #wait time function, the unit is 1 second 
    def timeEvent(self,TimeOut):
        nTim = int(TimeOut)
        time.sleep(nTim)
    
    """
    #wait dialog function, start
    def dialogEventStart(self,strOperate):

        strTemp = strOperate
        strTempWnd = ''
        strTempBtn = ''
        strTemp = strTemp[strTemp.find('$')+1:len(strTemp)]
      
        if strTemp.find('&&') == -1:
            return False
        
        strTempWnd = strTemp[0:strTemp.find('&&')]
        strTempWnd = strTempWnd[strTempWnd.find('=')+1:len(strTempWnd)] 

                      
        strTempBtn = strTemp[strTemp.find('&&')+2:len(strTemp)]
        strTempBtn = strTempBtn[strTempBtn.find('=')+1:len(strTempBtn)]


                
        nTime = 1
        aWindow = 0

        clickCancel = cModalPopUp.handlePopup('Confirm',strTempBtn) 
        clickCancel.popupName = strTempWnd
        clickCancel.start()
        return clickCancel
    """
    
    
    #wait dialog function, start
    def dialogEventStart_bak(self,strOperate):

        
        bEnd = False
        bChooseFile = False
        strTemp = ""
        strTempInfo = ""
        strTempInfoKey = ""
        strTempInfoValue = ""
        
        dstComb = {}
        desInfo = {}
        
        strTemp = strOperate

        # cut "dialog" information
        
        strTemp = strTemp[strTemp.find('$')+1:len(strTemp)]
        if strTemp.find('&&') == -1:
            return False      

    
        #get option information
        while bEnd == False:
            
            if strTemp.find('&&') == -1: #check whether the last key.
                strTempInfo = strTemp 
            else:            
                strTempInfo = strTemp[0:strTemp.find('&&')]
                
            strTempInfoKey = strTempInfo[0:strTempInfo.find('=')]             
            strTempInfoValue = strTempInfo[strTempInfo.find('=')+1:len(strTempInfo)] 
            
            if strTempInfoKey == "":
                return False            
                            
            if strTempInfoValue == "":
                return False
                
            #check text value,if find the key word than it is choose file dialog.
            if strTempInfoKey == KEY_WEB_TYPE_OPEN_DLG_TEXTVALUE:
                bChooseFile = True
                
            
                
            desInfo ={strTempInfoKey:strTempInfoValue} #set to desInfo
            dstComb.update(desInfo)                     # add more than one element.
            desInfo.clear() #clear for using at next time            
          
            
            #reset             
            if strTemp.find('&&') == -1: #check whether the last key.
                bEnd = True                               
            strTemp  =  strTemp[strTemp.find('&&')+2:len(strTemp)] #cut and get the last string.
     


        #do operation            
        
        if bChooseFile == True:      #if it is choose file dialog,do fallow operation.      
            
            clickCancel = cModalPopUp.handlePopup('ChooseFile',dstComb[KEY_WEB_TYPE_OPEN_DLG_TEXTVALUE],dstComb[KEY_WEB_TYPE_OPEN_DLG_BUTTON]) 
            clickCancel.popupName = dstComb[KEY_WEB_TYPE_OPEN_DLG_TITLE]
            clickCancel.start()               
 
            
        else :
            clickCancel = cModalPopUp.handlePopup('Confirm',dstComb[KEY_WEB_TYPE_OPEN_DLG_BUTTON]) 
            clickCancel.popupName = dstComb[KEY_WEB_TYPE_OPEN_DLG_TITLE]
            clickCancel.start()  
            #          
            
        return clickCancel
    
    
    def dialogEventStart(self,strOperate,lst_t=[]):

        #print 'dialogEventStart'
        bEnd = False
        bChooseFile = False
        strTemp = ""
        strTempInfo = ""
        strTempInfoKey = ""
        strTempInfoValue = ""
        
        dstComb = {}
        desInfo = {}
        
        strTemp = strOperate

        # cut "dialog" information
        strTemp = strTemp[strTemp.find('$')+1:len(strTemp)]
        if strTemp.find('&&') == -1:
            return False      

        
            
        #get option information
        land_Flag = False
        while bEnd == False:
            if strTemp.find('WindowsName=连接到')>-1:
                land_Flag = True
            
            #print 'land_Flag:',land_Flag
            if strTemp.find('&&') == -1: #check whether the last key.
                strTempInfo = strTemp 
            else:            
                strTempInfo = strTemp[0:strTemp.find('&&')]
                
            strTempInfoKey = strTempInfo[0:strTempInfo.find('=')]             
            strTempInfoValue = strTempInfo[strTempInfo.find('=')+1:len(strTempInfo)] 
            
            if strTempInfoKey == "":
                return False            
                            
            if strTempInfoValue == "":
                return False
                
            #check text value,if find the key word than it is choose file dialog.
            if strTempInfoKey == KEY_WEB_TYPE_OPEN_DLG_TEXTVALUE:
                bChooseFile = True
            
                
            desInfo ={strTempInfoKey:strTempInfoValue} #set to desInfo
            dstComb.update(desInfo)                     # add more than one element.
            desInfo.clear() #clear for using at next time            
          
            
            #reset             
            if strTemp.find('&&') == -1: #check whether the last key.
                bEnd = True                               
            strTemp  =  strTemp[strTemp.find('&&')+2:len(strTemp)] #cut and get the last string.
     


        #do operation            
        if bChooseFile == True:      #if it is choose file dialog,do fallow operation. 
            #print 'here22222:',land_Flag     
            if land_Flag==True:
                #print 'here11111'
                clickCancel = cModalPopUp.handlePopup('Confirm_passwd',dstComb[KEY_WEB_TYPE_OPEN_DLG_TEXTVALUE],dstComb[KEY_WEB_TYPE_OPEN_DLG_BUTTON]) 
                clickCancel.popupName = dstComb[KEY_WEB_TYPE_OPEN_DLG_TITLE]
                clickCancel.start()
            else:
                clickCancel = cModalPopUp.handlePopup('ChooseFile',dstComb[KEY_WEB_TYPE_OPEN_DLG_TEXTVALUE],dstComb[KEY_WEB_TYPE_OPEN_DLG_BUTTON]) 
                clickCancel.popupName = dstComb[KEY_WEB_TYPE_OPEN_DLG_TITLE]
                clickCancel.start()               
 
        else :
            clickCancel = cModalPopUp.handlePopup('Confirm',dstComb[KEY_WEB_TYPE_OPEN_DLG_BUTTON]) 
            clickCancel.popupName = dstComb[KEY_WEB_TYPE_OPEN_DLG_TITLE]
            clickCancel.start()  
            #          
            
        return clickCancel


    #wait dialog function, end    
    def dialogEventEnd(self,obj_Cancel):
        obj_Cancel.join()
        #exit_thread
    
    # get version of ie. different version have different operation.            
    def getIEVersion(self,obj_ie):

        obj_ie.executeJavaScript(KEY_IE_VERSION)
        IEVersion = obj_ie.getDivValue('iversion','innerHTML') 
            
        idxStt = IEVersion.find('MSIE')

        idxEnd = IEVersion.find(';',idxStt,len(IEVersion))

        VersionKey = IEVersion[idxStt:idxEnd]
        log_print(VersionKey) 
        if VersionKey.find('8')>=0:
            return 8
        elif VersionKey.find('6')>=0:
            return 6
        elif VersionKey.find('9')>=0:
            return 9
        elif VersionKey.find('10')>=0:
            return 10
        else:
            return False
     
    #check page status.if page happen HTTP 500 error or Blank error,return True,else return False. 
    def checkPageIsBusy(self,ie):       
        print 'checkPageIsBusy fuction'
        time.sleep(1)  
        strName = ie.outerHTML()
        ''' 
        try:
            strName = ie.outerHTML()
        except Exception,str:
            log_print('outerHTML is except')
            log_print(str)
            return True
        '''
        time.sleep(1)
        #log_public(strName)
        if strName.find("HTTP 500") >= 0:
            ie.goBack()
            time.sleep(3)
            log_public( "HTTP 500,Error")
            return True        

        elif strName.find("<BODY></BODY>") >= 0:    
            ie.goBack()
            time.sleep(3)
            log_public( "HTTP BLANK,Error")
            return True     
                        
        return False                


    def MainCheckTableOne(self,obj_ie,strAssist,strControlName,strControlValue):  
        print ">>>MainCheckTableOne"
        
        strCMP1 = ""            
        dicCell = {KEY_TABLE_ROW:0,KEY_TABLE_COLUMN:0}
        if strControlValue == "" or strControlName == "":
            log_public(WEB_ERR_NO_0012)
            self.m_ERROR_MSG = WEB_ERR_NO_0012            
            return False   
             
        try:                    
 
            if self.dispath(strControlValue,dicCell) == False:
                return False
            
            strCMP1 = obj_ie.getTableText(strControlName,dicCell[KEY_TABLE_ROW],dicCell[KEY_TABLE_COLUMN])
            self.m_CmpLst.append(strCMP1)
            
            return True
        except:
            log_public(WEB_ERR_NO_0013+strControlName)
            self.m_ERROR_MSG = WEB_ERR_NO_0013+strControlName
            return False
        
    def Dialog_Button(self,obj_ie,strAssist,strControlName,strControlValue):
        print ">>Dialog_Button"
        try:
            new_obj = obj_ie.findWindow(strControlName)
            obj_ie._ie=new_obj
            obj_ie.clickButton(strControlValue)
            return True
        except Exception,e:
            log_print(e)
            return False
        
        
        
    def MainCheckTableTwo(self,obj_ie,strAssist,strControlName,strControlValue):
        print ">>>MainCheckTableTwo"
        
        strCMP1 = ""                        
        strCMP2 = "" 
        dicCell = {KEY_TABLE_ROW:0,KEY_TABLE_COLUMN:0}
        lstIndx = 0  
        if strControlValue == "" or strControlName == "":   
            log_public(WEB_ERR_NO_0015)
            self.m_ERROR_MSG = WEB_ERR_NO_0015                         
            return False  
                                      
        try:
            
            lstIndx = len(self.m_CmpLst)-1
            #get value 1 form list.
            strCMP1 = self.m_CmpLst.pop(lstIndx)          
            
            if self.dispath(strControlValue,dicCell)==False:
                return False
            
            #get value 2
            strCMP2 = obj_ie.getTableText(strControlName,dicCell[KEY_TABLE_ROW],dicCell[KEY_TABLE_COLUMN])        

            #compare
            if strCMP1 == strCMP2:
                return True
            else:
                log_public(WEB_ERR_NO_0016+strControlName)
                self.m_ERROR_MSG = WEB_ERR_NO_0016+strControlName
                return False
            
        except:
            log_public(WEB_ERR_NO_0017+strControlName)
            self.m_ERROR_MSG = WEB_ERR_NO_0017+strControlName            
            return False      
        

        
    def dispath(self,strValue,dicCell):      
        print ">>>dispath"
        strTemp = strValue
   
        strTempRow = ''
        strTempCol = ''
        #strTemp = strTemp[strTemp.find('/')+1:len(strTemp)]
      
        if strTemp.find('&&') == -1:
            log_public(WEB_ERR_NO_0014)
            self.m_ERROR_MSG = WEB_ERR_NO_0014
            return False
        
        strTempRow = strTemp[0:strTemp.find('&&')]        
        if strTempRow.find('=') == -1:
            log_public(WEB_ERR_NO_0014)
            self.m_ERROR_MSG = WEB_ERR_NO_0014
            return False
        
        strTempRow = strTempRow[strTempRow.find('=')+1:len(strTempRow)] 
        if strTempRow == "":
            log_public(WEB_ERR_NO_0014)
            self.m_ERROR_MSG = WEB_ERR_NO_0014
            return False
                      
        strTempCol = strTemp[strTemp.find('&&')+2:len(strTemp)]        
        if strTempCol.find('=') == -1:
            log_public(WEB_ERR_NO_0014)
            self.m_ERROR_MSG = WEB_ERR_NO_0014
            return False    
            
        strTempCol = strTempCol[strTempCol.find('=')+1:len(strTempCol)]
        if strTempCol == "":
            log_public(WEB_ERR_NO_0014)
            self.m_ERROR_MSG = WEB_ERR_NO_0014
            return False
        
        dicCell[KEY_TABLE_ROW] = string.atoi(strTempRow)
        dicCell[KEY_TABLE_COLUMN] = string.atoi(strTempCol)        
        
        return True        
        
        
    def MainCloseIEWindow(self,strControlName):
        print ">>>MainCloseIEWindow"     
        clss = "IEFrame"
        
        try:
            hwnd = win32gui.FindWindow(clss,strControlName)
            time.sleep(1)     
            win32api.SendMessage(hwnd,win32con.WM_CLOSE,0,0)  
            return True
        except:
            log_public(WEB_ERR_NO_0018)
            self.m_ERROR_MSG = WEB_ERR_NO_0018                 
            return False
        
    def Onu_login(self,FlowName):
        print 'onu_login fuction'
        if self.Onu_login_Flag == 1 :
            return True
        ap_name = FlowName.split('_')[-1]
        if ap_name =='ONU':
            login_username = LOGIN_USERNAME_GONGJIN
            login_password = LOGIN_PASSWORD_GONGJIN
            print 'GONGJIN:login_username--',login_username
            print 'GONGJIN:login_password--',login_password
        test_win = win_gui()
        
        hwnd = win32gui.FindWindow('#32770',None)
        print 'hwnd is ',hwnd
        if hwnd < 1:
            log_public(WEB_ERR_NO_0020)
            self.m_ERROR_MSG = WEB_ERR_NO_0020
            return False
        else:
            win32api.Sleep(100)
            win32api.keybd_event(18,0,0,0);
            win32api.keybd_event(85,0,0,0);
            win32api.Sleep(100)
            win32api.keybd_event(85,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.Sleep(100)
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys(login_username)
            
            win32api.Sleep(100)
            win32api.keybd_event(18,0,0,0);
            win32api.keybd_event(80,0,0,0);
            win32api.Sleep(100)
            win32api.keybd_event(80,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.Sleep(300)
            shell.SendKeys(login_password)
            win32api.Sleep(100)
            win32api.keybd_event(13,0,0,0);   
            win32api.Sleep(100)
            win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.Sleep(100)
            return True
        
    def check_Landdlg(self,hwdlist,lst_t=[]):
        
        try:
           for x in hwdlist:
               title_name= win32gui.GetWindowText(x)
               #print 'here',title_name
               if title_name.startswith('连接到')==True:
                   #app.connect_(handle=x)
                   #print '11111'
                   #time.sleep(1)
                   username='admin'
                   passwd ='admin'
                   if len(lst_t)!=0:
                       for y in lst_t:
                           #print 'lstSub[j]333332222215:' ,y
                           if y.has_key('ASSIST')==True:
                               if y['ASSIST'] == KEY_USERNAME:
                                    username = y['ControlType']
                               elif y['ASSIST'] == KEY_PASSWD:
                                       passwd = y['ControlType']
                   combolist =findControls(topHwnd=x,wantedClass='ComboBox')
                   combolist = list(set(combolist))
                   #print 'combolist:',combolist
                   dump_ed_hwnd = 0
                   for y in combolist:
                       dump_ed_hwnd = dumpWindow(y)[0][0]
                       #print 'dumpWindow:',dumpWindow(y),'dump_ed_hwnd',dump_ed_hwnd
                   if dump_ed_hwnd == 0 :
                       return False
                   Editlist = findControls(topHwnd=x,wantedClass='Edit')
                   #print 'Editlist:',Editlist
                   #print 'passwd:',passwd,'  username:',username
                   userFlag = False
                   tmp_hwd =[]
                   Editlist = list(set(Editlist))
                   for y in Editlist:
                       #print '2222',y, ' getEditText(y):',getEditText(y),'  len:',len(getEditText(y))
                       if y  in tmp_hwd:
                           continue
                       else:
                           tmp_hwd.append(y)
                       if len(getEditText(y))>1:
                           #print 'getEditText(y)',getEditText(y) , ' len:',len(getEditText(y))
                           continue
                       #print 'dump_ed_hwnd',dump_ed_hwnd,'  y:',y
                       if dump_ed_hwnd ==y:
                           setEditText(y,username)
                       else:
                           setEditText(y,passwd)
                       
                       win32api.Sleep(100)
                   #time.sleep(100)
                   b_hwd = findControl(topHwnd=x,wantedClass='Button',wantedText='确定')
                   #print 'button',b_hwd
                   clickButton(b_hwd)
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        return True
                
    def AP_login(self,FlowName):
        ap_name = FlowName.split('_')[-1]
        print 'ap_name:',ap_name
        FLAG_ONU == True
        if ap_name == 'ZNAP':
            login_username = LOGIN_USERNAME_ZNAP
            login_password = LOGIN_PASSWORD_ZNAP
            print 'ZNAP:login_username--',login_username
            print 'ZNAP:login_password--',login_password
        elif ap_name == 'GONGJIN':
            login_username = LOGIN_USERNAME_GONGJIN
            login_password = LOGIN_PASSWORD_GONGJIN
            print 'GONGJIN:login_username--',login_username
            print 'GONGJIN:login_password--',login_password
        elif ap_name =='ONU':
            login_username = LOGIN_USERNAME_GONGJIN
            login_password = LOGIN_PASSWORD_GONGJIN
            print 'GONGJIN:login_username--',login_username
            print 'GONGJIN:login_password--',login_password
            
        else:
            print 'FlowName wrong.There is no login information for your AP_manufacturer.'
            log_public(WEB_ERR_NO_0019)
            self.m_ERROR_MSG = WEB_ERR_NO_0019
            return False
        
        time.sleep(1)
        hwnd = win32gui.FindWindow('#32770',None)
        print 'hwnd is ',hwnd
        
        if hwnd < 1:
            log_public(WEB_ERR_NO_0020)
            self.m_ERROR_MSG = WEB_ERR_NO_0020
            return False
        else:
            #send Alt+U to input user name.
            win32api.Sleep(1000)
            '''
            win32api.keybd_event(18,0,0,0);
            win32api.keybd_event(85,0,0,0);
            win32api.Sleep(1000)
            win32api.keybd_event(85,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.Sleep(1000)
            print 'send Alt+U to input user name'
            '''
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys(login_username)
            print 'input user name'
            
            #send Alt+P to input password.
            
            win32api.Sleep(1000)
            win32api.keybd_event(18,0,0,0);
            win32api.keybd_event(80,0,0,0);
            win32api.Sleep(1000)
            win32api.keybd_event(80,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.Sleep(1000)
            #print 'send Alt+P to input password'
            
            
            shell.SendKeys(login_password)
            print 'input password'
            
            
            win32api.Sleep(1000)
            win32api.keybd_event(13,0,0,0);   
            win32api.Sleep(1000)
            win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0);
            win32api.Sleep(1000)
            
            '''
            #hwndnew = win32gui.FindWindow('#32770',None)
            time.sleep(1)
            print 'hwndnew 000:',self.hwndnew
            self.hwndnew = self.myobj.find_main_window('')
            print 'hwndnew is ',self.hwndnew 
            
            if self.hwndnew > 0:
                #close login window and return false.
                log_public(WEB_ERR_NO_0021)
                self.m_ERROR_MSG = WEB_ERR_NO_0021
                self.kill_ie()
                         
                #send Alt+P to make the cursor in the password box.
                win32api.Sleep(500)
                win32api.keybd_event(18,0,0,0);   
                win32api.keybd_event(85,0,0,0);   
                win32api.Sleep(500)
                win32api.keybd_event(85,0,win32con.KEYEVENTF_KEYUP,0);
                win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
                win32api.Sleep(500)
                
                self.myobj.Mouse_LB_D(str_app = '杩炴帴鍒�',lb_dx = '270',lb_dy = '260',Flag = '1')                
                print 'close ap login window.'
     
                #close ie window.
                win32api.keybd_event(18,0,0,0);   
                win32api.keybd_event(70,0,0,0);   
                win32api.Sleep(500)
                win32api.keybd_event(70,0,win32con.KEYEVENTF_KEYUP,0);
                win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
                win32api.Sleep(500)
                win32api.keybd_event(88,0,0,0);   
                win32api.Sleep(500)
                win32api.keybd_event(88,0,win32con.KEYEVENTF_KEYUP,0);
                print 'close ie window.'
                self.hwndnew = 0
                print 'final hwndnew:',self.hwndnew
                
                return False
                
            else:
                print 'input right username and password.'
            '''
            return True
        
    def kill_ie(self):
        result =False
        REC_read= 'wmic process where caption="iexplore.exe" get caption,commandline /value'
        REC_kill=  'TASKKILL /F /IM iexplore.exe'
        print_mes = os.popen(REC_read).read() 
        print print_mes
        #info_public(print_mes)
        if print_mes.find('Explorer')>-1:
            print_mes = os.popen(REC_kill).read() 
            print print_mes
            #info_public(print_mes)
        return result
    
    def getTextAreasValue(self,ie):
        print 'getTextAreasValue futction'
        try:
            if ie.tableExists('tbl'):
                print ie.getTableData('tbl')  
        except Exception ,str:
            print str
            pass
        
        print 'getTextAreasValue futction return '
        return True
    
        
if __name__ == "__main__":
    myObj = Class_RW_Excel();
    result = myObj.setWebPage('E:\\L1_ETH_OTHER\\Module_Other\\Case_eoc\\Webonu.xlsx','CONFIG25_ONU','CAOFF')
    print 'result:',result
    #myObj.setWebPage('D:\\playWeb\\WebPages_Flow.xls','PORTAL','CAOFF')
   

    
    #cst = myObj.GetErrorInfo()
    #print cst
