# -*- coding: gb18030 -*- 
#-----------------------------------------------------------------------------
# Name:        rw_Excel_selenium.py
# Purpose:     read infromation from Excel.this excel record operation of Web page.Use selenium
#
# Author:      <gongke>
#
# Created:     2015/02/03
# RCS-ID:      $Id: rw_Excel_selenium.py $
# Copyright:   (c) 2006
# Licence:     <0.1.0>
#-----------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import xlrd
from WtLog import log_public
import string
import win32gui
import win32api
import win32con
import os
import sys
from global_parame import *
from public import *
from pywinauto import *
import unittest, time, re,random
import urllib
import chardet
import shutil
import traceback

KEY_SHEETNAME = 'SheetName'
KEY_URL = 'URL'
KEY_ASSIST = 'ASSIST'
KEY_COMMENT = 'C'
KEY_LAND ='LAND'
KEY_CONTROLTYPE = 'ControlType'
KEY_CONTROLNAME = 'ControlName'
KEY_CONTROLVALUE = 'ControlValue'
KEY_HEAD = 'HEADER'
KEY_END = 'END'
KEY_A_COL = 0
KEY_B_COL = 1
KEY_C_COL = 2
KEY_D_COL = 3

#---------------------------------------
KEY_ROW = 'rowx'
KEY_COL = 'coly'
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


ENCODE_DECODE = 'gb18030'

KEY_WEB_TYPE_WAIT  = 'WAIT'
KEY_WEB_TYPE_CLICK  = 'CLICK'
KEY_WEB_TYPE_SWITCHDEFAULT = 'SWITCHDEFAULT'
KEY_WEB_TYPE_SWITCHFRAME = 'SWITCHFRAME'
KEY_WEB_TYPE_DIALOG = 'DIALOG'
KEY_WEB_TYPE_DIALOG_UPDATA ='UPDATA'

KEY_WEB_WAIT_EVENT_TIME = 'time'

KEY_WEB_TYPE_LISTBOX  = 'LISTBOX'


KEY_SELENIUM_FIND_ELEMENT_BY_ID='BYID'
KEY_SELENIUM_FIND_ELEMENT_BY_NAME='BYNAME'
KEY_SELENIUM_FIND_ELEMENT_BY_XPATH='XPATH'
KEY_SELENIUM_FIND_ELEMENT_BY_CSS='CSS'
KEY_SELENIUM_FIND_ELEMENT_BY_CLASSNAME='CLASS'
KEY_WEB_TYPE_TEXTBOX  = 'TEXTBOX'
KEY_WEB_TYPE_CHECKBOX  = 'CHECKBOX'

KEY_COM_TEXT_GET = "GET"


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

class Class_web_Selenium: 
    m_ERROR_MSG = "no error"    #recoard error message.
    m_bSTOP = False
    
    def __init__(self):
        self.global_p = {}  
    
    def GetErrorInfo(self):   
        #log_print(self.m_ERROR_MSG )     
        return self.m_ERROR_MSG   
    
    def SetStop(self):
        self.m_bSTOP = True
    
    def setWebPage(self,filePath,FlowName,bCA):
        log_print( 'setWebPage fuction')
        version_file = find_parentpath()+'\\auto_conf\\version.ini'
        tmp_Land_Dialog_check_total=read_ini(version_file,'Land_Dialog_check_total','ACweb Debug')
        tmp_Wait_Dialog_time =read_ini(version_file,'tmp_Wait_Dialog_time','ACweb Debug')
        if len(tmp_Land_Dialog_check_total.strip())>0:
            self.Land_Dialog_check_total = string.atoi(tmp_Land_Dialog_check_total.strip())
        if len(tmp_Wait_Dialog_time.strip())>0:
            self.Wait_Dialog_time = string.atof(tmp_Wait_Dialog_time.strip())
        
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
        
        if self.OperateWebPage(FlowName,bCA,lst) == False:
            return False
        
        del lst    
        return True
    
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
            
    def ReadWebPgURL(self,obj_table,dctCurNode,lst):
        log_print( 'ReadWebPgURL fuction')
        strNextNode = ''
        myURL =''      
        row = dctCurNode[KEY_ROW]
        col = dctCurNode[KEY_COL]
        
        #Get Keyword URL 
        HEADERFRAME = obj_table.cell(row,col+1).value
        HEADERFRAME.strip()
        
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
        dct_URL[KEY_HEAD]=HEADERFRAME;
        lst.append(dct_URL)            
        
        #get NextNode
        strNextNode = obj_table.cell(row,col+3).value
        return strNextNode
    
    def read_global_param(self,filename ='E:\\Simu_server\\global\\global_param.xls',sheetname='global'):
        testexcel = readexcel(filename,sheetname)
        self.global_p = testexcel.Excel_read()
        msg = self.global_p
        log_print(msg)
        
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
        print 'hz_yes:',hz_yes
        return hz_yes
    
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
    
    def ie_close(self,driver,stime = 5):
        time.sleep(stime)
        driver.quit()
        kill_program()
        
    def OperateWebPage(self,FlowName,bCA,lst):
        self.test_NG_error = ''
        kill_program()
        
        lst = self.Replace_global_multi_list(lst)
        dstURL={}
        if self.test_NG_error.find('the global file')>-1:
            log_print('not fined the global file')
            return False
        driver = webdriver.Ie()
        i = 0
        lstLen = len(lst)
        while i<lstLen:
            lstSub=[]
            lstSub.extend(lst[i])
            lstSubLen = len(lstSub)
            j = 0
            lstSubLen = len(lstSub)
            while j<lstSubLen:
                if j == 0 :
                    dstURL={}
                    dstURL.update(lstSub[j])
                    if self.OpenURL(driver,dstURL)==False:
                        return False
                else:
                    dstComb = {}
                    dstComb.update(lstSub[j])
                    if cmp(dstComb['ASSIST'],KEY_COMMENT)==0:
                        j+=1
                        continue
                    elif cmp(dstComb['ASSIST'],KEY_LAND)==0:
                        if self.LandDlg(dstComb)==False:
                            return False
                    else:
                        Value = dstComb[KEY_CONTROLTYPE]
                        log_print(KEY_WEB_TYPE_WAIT)
                        log_print(dstComb[KEY_CONTROLNAME])
                        log_print(dstComb[KEY_CONTROLVALUE])
                        log_print(dstComb['ASSIST'])
                        if Value == KEY_WEB_TYPE_WAIT:
                            if self.waitEvent(dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                                log_print('waitEvent is False')
                                if self.checkPageIsBusy(driver) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-1
                                    break                           
                                self.ie_close(driver)
                                log_public(WEB_ERR_NO_0007+dstComb[KEY_CONTROLNAME])
                                self.m_ERROR_MSG =  WEB_ERR_NO_0007+dstComb[KEY_CONTROLNAME]
                                return False
                        elif Value == KEY_WEB_TYPE_CLICK:
                            if self.EventClick(driver,dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE])==False:
                                if self.checkPageIsBusy(driver) == True:
                                    log_print('checkPageIsBusy reutrn True')
                                    i = i-1
                                    break  
                    
                        elif Value == KEY_WEB_TYPE_SWITCHDEFAULT:
                            if self.EventSwitchDefault(driver)==False:
                                return False
                        elif Value == KEY_WEB_TYPE_SWITCHFRAME:
                            if self.EventSwitchFrame(driver,dstComb[KEY_CONTROLNAME])==False:
                                return False
                        elif Value == KEY_WEB_TYPE_TEXTBOX:
                            if self.EventTextBox(driver,dstComb)==False:
                                return False
                        elif Value == KEY_WEB_TYPE_DIALOG:
                            if self.EventDialogA(dstComb)==False:
                                return False
                        elif Value ==KEY_WEB_TYPE_LISTBOX:
                            if self.EventListBox(driver,dstComb) ==False:
                                return False
                        elif Value ==KEY_WEB_TYPE_CHECKBOX:
                            if self.EventCheckBox(driver, dstComb) ==False:
                                return False
                        elif Value ==KEY_WEB_TYPE_DIALOG_UPDATA:
                            if self.EventDialogB(driver,dstComb)==False:
                                return False
                j+=1   
            i+=1
        return
    
    def EventCheckBox(self,driver,dstComb):
        by = dstComb['ControlName'].upper()
        value = dstComb['ControlValue']
        if self.EventClick(driver,by,value) ==False:
            return False
        return True
    
    def EventListBox(self,driver,dstComb):
        by = dstComb['ASSIST'].upper()
        try:
            if cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_ID)==0:
                Select(driver.find_element_by_id(dstComb['ControlName'])).select_by_visible_text(dstComb['ControlValue'])
                time.sleep(1)
                #driver.find_element_by_id(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_NAME)==0:
                Select(driver.find_element_by_name(dstComb['ControlName'])).select_by_visible_text(dstComb['ControlValue'])
                time.sleep(1)
                #driver.find_element_by_name(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_XPATH)==0:
                Select(driver.find_element_by_xpath(dstComb['ControlName'])).select_by_visible_text(dstComb['ControlValue'])
                time.sleep(1)
                #driver.find_element_by_xpath(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_CLASSNAME)==0:
                Select(driver.find_element_by_class_name(dstComb['ControlName'])).select_by_visible_text(dstComb['ControlValue'])
                time.sleep(1)
                #driver.find_element_by_class_name(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_CSS)==0:
                Select(driver.find_element_by_css_selector(dstComb['ControlName'])).select_by_visible_text(dstComb['ControlValue'])
                time.sleep(1)
        except Exception,e:
            log_print(e)
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
    
    def EventDialogB(self,driver,dstComb):
        log_print("EventDialogB Fuction")
        
        return True
    def EventDialogA(self,dstComb):
        log_print("EventDialogA Fuction")
        num_wait = 0
        app_l=[]
        FindDlgFlag = True
        while True:
            time.sleep(2)
            print '#num_wait:',num_wait
            tmptitle = unicode(dstComb['ControlName'],ENCODE_DECODE)
            #buttonName = unicode(dstComb['ControlValue'],ENCODE_DECODE)
            try:
                print 'title:',dstComb['ControlName']
                app_l = findwindows.find_windows(title_re = tmptitle)
                print '#app_l:',app_l
                if len(app_l)<=0:
                    num_wait+=1
                    time.sleep(3)
            except Exception,e:
                log_print(e)
                num_wait+=1
                time.sleep(5)
                pass
            
            if len(app_l)>0:
                print 'here:'
                try:
                    hwd = app_l[0]
                    app = Application()
                    app.connect_(handle = hwd)
                    dlg = app.window_(title_re =  tmptitle)
                    print 'here1'
                    #time.sleep(1)
                    dlg.window_(title_re = dstComb['ControlValue']).Click()
                    print 'here2'
                except Exception,e:
                    log_print(e)
                    return FindDlgFlag
                break
            elif num_wait>=self.Land_Dialog_check_total :
                return FindDlgFlag
        return True
    
    def EventTextBox(self,driver,dstComb):
        by = dstComb['ASSIST'].upper()
        try:
            if cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_ID)==0:
                driver.find_element_by_id(dstComb['ControlName']).clear()
                driver.find_element_by_id(dstComb['ControlName']).send_keys(dstComb['ControlValue'])
                time.sleep(1)
                #driver.find_element_by_id(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_NAME)==0:
                driver.find_element_by_name(dstComb['ControlName']).clear()
                driver.find_element_by_name(dstComb['ControlName']).send_keys(dstComb['ControlValue'])
                time.sleep(1)
                #driver.find_element_by_name(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_XPATH)==0:
                driver.find_element_by_xpath(dstComb['ControlName']).clear()
                driver.find_element_by_xpath(dstComb['ControlName']).send_keys(dstComb['ControlValue'])
                time.sleep(1)
                #driver.find_element_by_xpath(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_CLASSNAME)==0:
                driver.find_element_by_class_name(dstComb['ControlName']).clear()
                driver.find_element_by_class_name(dstComb['ControlName']).send_keys(dstComb['ControlValue'])
                time.sleep(1)
                #driver.find_element_by_class_name(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_CSS)==0:
                driver.find_element_by_css_selector(dstComb['ControlName']).clear()
                driver.find_element_by_css_selector(dstComb['ControlName']).send_keys(dstComb['ControlValue'])
                time.sleep(1)
            
        except Exception,e:
            log_print(e)
            return False
        
        return True
            
    def EventSwitchFrame(self,driver,frame):
        try:
            driver.switch_to_default_content()
            driver.switch_to_frame(frame)
            #driver.switch_to_default_content()
            #driver.switch_to_frame(frame)
            print "03URL:",driver.current_url
            time.sleep(2)
        except Exception,e:
            log_print(e)
            return False
        return True
    
    def EventSwitchDefault(self,driver):
        try:
            driver.switch_to_default_content()
            print "04URL:",driver.current_url
            time.sleep(2)
        except Exception,e:
            log_print(e)
            return False
        return True
    
    def EventClick(self,driver,by,value):
        by = by.upper()
        try:
            if cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_ID)==0:
                driver.find_element_by_id(value).click()
                time.sleep(1)
                #driver.find_element_by_id(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_NAME)==0:
                driver.find_element_by_name(value).click()
                time.sleep(1)
                #driver.find_element_by_name(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_XPATH)==0:
                driver.find_element_by_xpath(value).click()
                time.sleep(1)
                #driver.find_element_by_xpath(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_CLASSNAME)==0:
                driver.find_element_by_class_name(value).click()
                time.sleep(1)
                #driver.find_element_by_class_name(value).click()
            elif cmp(by,KEY_SELENIUM_FIND_ELEMENT_BY_CSS)==0:
                driver.find_element_by_css_selector(value).click()
                time.sleep(1)
                #driver.find_element_by_css_selector(value).click()
            else:
                return False
        except Exception,e:
            log_print(e)
            return False
        
    def waitEvent(self,EventName,TimeOut):
        #print 'waitEvent fuction:',EventName, TimeOut
        strTemp = EventName
        
        if strTemp.find('$') != -1:
            strTemp = strTemp[0:strTemp.find('$')]
        if strTemp == KEY_WEB_WAIT_EVENT_TIME:
            self.timeEvent(TimeOut)
            return True
        return False
        '''
        elif strTemp ==KEY_WEB_WAIT_EVENT_DIALOG:
            if TimeOut == KEY_URL_WAITEVENT_START:
                self.m_Obj_WaitDialog_Cancel = self.dialogEventStart(EventName)
                if self.m_Obj_WaitDialog_Cancel == False:
                    return False
                
            elif TimeOut == KEY_URL_WAITEVENT_END:
                self.dialogEventEnd(self.m_Obj_WaitDialog_Cancel)
            
            return True
        '''
       
    
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
    
    def timeEvent(self,TimeOut):
        nTim = int(TimeOut)
        time.sleep(nTim)
        
    def OpenURL(self,driver,tmpdic):
        try:
            if cmp(tmpdic['HEADER'].upper(),'FRAME')==0:
                driver.switch_to_default_content()
                time.sleep(2)
                print "01URL:",driver.current_url
                driver.switch_to_default_content()
                driver.switch_to_frame(tmpdic['URL'])
                #driver.switch_to_default_content()
                #driver.switch_to_frame(tmpdic['URL'])
                #driver.switch_to_frame(tmpdic['URL'])
                time.sleep(2)
                print "02URL:",driver.current_url
            else:
                driver.get(tmpdic['URL'])
        except Exception,e:
            log_print(e)
            return False
        return True
    
    def LandDlg(self,tmpdic):
        log_print("LandDlg Fuction")
        num_wait = 0
        app_l=[]
        while True:
            time.sleep(2)
            try:
                app_l = findwindows.find_windows(title_re = u"连")
                if len(app_l)<=0:
                    num_wait+=1
                    time.sleep(5)
            except Exception,e:
                log_print(e)
                num_wait+=1
                time.sleep(5)
                pass
            if num_wait>=self.Land_Dialog_check_total  or len(app_l)>0:
                break
            
        if len(app_l)>0:
            hwd = app_l[0]
            while True:
                app = Application()
                
                app.connect_(handle = hwd)
            
                dlg = app.window_(title_re = u"连接到")
            
                dlg['Edit2'].TypeKeys(tmpdic[KEY_CONTROLTYPE])
                #time.sleep(1)
                dlg['Edit3'].TypeKeys(tmpdic[KEY_CONTROLNAME])
                #time.sleep(1)
                dlg.window_(title_re = u'确定').Click()
                time.sleep(2)
                tmp = findwindows.find_windows(title_re = u"连")
                if len(tmp)>0:
                    hwd = tmp[0]
                else:
                    break
            
        else:
            return False
        return True
    
    '''
    def DoOtherControl(self,driver,dstComb):
        Value = dstComb[KEY_CONTROLTYPE]
        
        if Value == KEY_WEB_TYPE_WAIT:
            if self.waitEvent(dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                log_print('waitEvent is False')
                
        return True
    '''
    def checkPageIsBusy(self,driver):       
        print 'checkPageIsBusy fuction'
        time.sleep(1)  
        strName = str(driver.page_source)
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
            driver.back()
            time.sleep(3)
            log_public( "HTTP 500,Error")
            return True        

        elif strName.find("<BODY></BODY>") >= 0:    
            driver.back()
            time.sleep(3)
            log_public( "HTTP BLANK,Error")
            return True     
                        
        return False      
            
if __name__ == "__main__":
    myObj = Class_web_Selenium();
    TestPath = 'E:\\L1_ETH_OTHER\\Module_Other\\Case_eoc\\Account.xls'
    TestPath =raw_input("please input the Testcase Path:")
    total = 10000
    
    while total>0:
        try:
            result = myObj.setWebPage(TestPath,'CONFIG_ONU','CAOFF')
        except Exception, e:
            log_print(e)
            pass
        print 'result:',result
        total=total-1
        tmp = 10000 - total
        print "*********************************"
        print '####  run:',tmp
        print "*********************************"
        if result==False:
            break
        time.sleep(3)
