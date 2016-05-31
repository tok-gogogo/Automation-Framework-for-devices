# -*- coding: gb18030 -*- 
#-----------------------------------------------------------------------------
# Name:        rw_Excel_FLOW.py
# Purpose:     read infromation from Excel.this excel record operation of Web page.
#
# Author:      <chenshengcong>
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
import xlrd
#import xlwt

from PAM30 import PAMIE
import time
import win32gui
import thread 
import cModalPopUp
from WtLog import log_public
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
KEY_WEB_TYPE_TEXTBOX  = 'TEXTBOX'
KEY_WEB_TYPE_CHECKBOX  = 'CHECKBOX'
KEY_WEB_TYPE_LISTBOX  = 'LISTBOX'
KEY_WEB_TYPE_BUTTON  = 'BUTTON'
KEY_WEB_TYPE_WAIT  = 'WAIT'
KEY_WEB_TYPE_JAVASCRIPT  = 'JAVASCPIPT'
KEY_WEB_TYPE_GROUP_CHECKBOX = 'GROUP_CHECKBOX'
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




class Class_RW_Excel:   


    m_ERROR_MSG = "no error"    #recoard error message.
    m_Group_Idx = -1
    m_Obj_WaitDialog_Cancel = 0
    
    #-----------------------------------------------------------------------------
    # Name:        GetErrorInfo -get error information
    # ruturn:      return string.the string is error message. if no error happen ,it is "no error".
    # Author:      <chensc>
    #
    # Created:     2013/02/28
    # RCS-ID:      $Id: rw_Excel_FLOW.py $
    #-----------------------------------------------------------------------------
    def GetErrorInfo(self):
       return self.m_ERROR_MSG         
   
   
    #-----------------------------------------------------------------------------
    # Name:        readWebPage
    # Purpose:     read information of web page to be control by python.
    # parameter:   filePath-the Excel path,include excel file name.
    #              FlowName-the flow name. at C coloumn of Excel file. eg:'CONFIG'.
    #              bCA -String type. tow value 'CAON','CAOFF','CAON' mean have CA authentication.'CAOFF' mean not have CA authentication
    # Author:      <chensc>
    #
    # Created:     2013/02/06
    # RCS-ID:      $Id: rw_Excel_FLOW.py $
    # Copyright:   (c) 2006
    # Licence:     <your licence>
    #-----------------------------------------------------------------------------
    def setWebPage(self,filePath,FlowName,bCA):
        
        myPath = filePath        
        lst = []
        obj_book = 0
        obj_table = 0
        
        LOOPMAX = 0
        shttName =''
        ret = 0 #return value form function
        
        obj_book =  self.OpenFile(myPath)
        
        for sheet_name in obj_book.sheet_names():
            if sheet_name == u'0-ACPAGE' :
                obj_table = obj_book.sheet_by_name(sheet_name) 
                break            
        
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
        print lst   #need dele          
        if self.OperateACWebPage(bCA,lst) == False:
                return False
            
        del lst    
        return True
        
    #read Flowchart header            
    def ReadFlowHeader(self,obj_table,FlowName,dctNode):
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
                     if myFlowName == FlowName:
                         strOrg =  obj_table.cell(rows+1,KEY_C_COL).value
                         strOrg.strip()
                         self.transform(strOrg,dctNode)                         
                         return True                    
        
        return False
    
    
    
    #read page information
    def ReadFlowPage(self,obj_table,dctCurNode,dctNextNode,lst):
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
        try:
            obj_book = xlrd.open_workbook(filePath)
            return obj_book
        except:
            log_public(ERR_FILE_OPENFAIL_0001)            
            self.m_ERROR_MSG = ERR_FILE_OPENFAIL_0001
    
    #read URL
    def ReadWebPgURL(self,obj_table,dctCurNode,lst):
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
            self.m_ERROR_MSG = ERR_EXCEL_CONTROLTYPE_0005
            return False
        
        if cmp(myControlValue,KEY_CONTROLVALUE) == -1:
           log_public( ERR_EXCEL_CONTROLVALUE_0006)
           self.m_ERROR_MSG = ERR_EXCEL_CONTROLVALUE_0006
           return False           

    #read controlType,controlName,controlvalue    
    def ReadWebPgControl(self,obj_table,dctCurNode,lst):
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
            log_public(dct_CONTROLTYPE)            
            dct_Combn.update(dct_CONTROLTYPE)
                    
            mySubControlName = str(obj_table.cell(rows,col+2).value.encode('gb18030')) 
            mySubControlName.strip()
            if mySubControlName =='':
                log_public(ERR_EXCEL_CONTROLNAME_VALUE_0010)
                self.m_ERROR_MSG = ERR_EXCEL_CONTROLNAME_VALUE_0010
                return False
            dct_CONTROLNAME = {KEY_CONTROLNAME:mySubControlName}
            dct_Combn.update(dct_CONTROLNAME)
                    
            
            mySubControlValue = obj_table.cell(rows,col+3).value
            if isinstance(mySubControlValue,float) == False & isinstance(mySubControlValue,int) == False:
                mySubControlValue = obj_table.cell(rows,col+3).value.encode('gb18030')
            else:
                mySubControlValue = str(mySubControlValue)
                mySubControlValue = mySubControlValue[0:mySubControlValue.find('.')]


            dct_CONTROLVALUE = {KEY_CONTROLVALUE:mySubControlValue}
            dct_Combn.update(dct_CONTROLVALUE)                
            
            lst.append(dct_Combn)            
            del dct_Combn
            
        return True
    
    
    #translate form ,eg:B3,tha is :row is 3,col is B, then change to number row=2,col=1    
    def transform(self,strOrg,dctRowCol):
       

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
    def OperateACWebPage(self,bCA,lst):
        #global Obj_WaitDialog_Cancel
        #g_Group_Idx
        #define 'ie' object to control web page
        ie = PAMIE()

        #check version of IE. different version have different operate.
        nVer = self.getIEVersion(ie)                        
        if nVer == -1:
            log_public(WEB_ERR_NO_0002+dstURL[KEY_URL])
            self.m_ERROR_MSG = WEB_ERR_NO_0002+dstURL[KEY_URL]
            return False                      
        #KillCA = True
        KillCA = bCA
        #loop to control every web page,all the control information storage at lst.
        #we loop to get page information at 'lst' to control web pages.
        #We call it one page_operate.
        lstLen = len(lst)
        for i in range(lstLen):
            
            #define 'lstSub',this list go to storage web page information.
            lstSub=[]
            lstSub.extend(lst[i])


            #loop to control every control_components of one web page.
            #we loop to get control_components at 'lstSub' to control control_components of one web pages. 
            #We call it line_operation. 
            #Obj_WaitDialog_Cancel = 0  #if dialog popup after you click a button.you need to use WAIT DIALOG EVENT. This variable will starage the object.        
            lstSubLen = len(lstSub)
            for j in range(0,lstSubLen):
                
                #get URL path
                #URL path is storage at '1' index of 'lstSubLen',so judge 'j' wether equal 1.
                if j == 0 :
                    
                    #define 'dstURL' as dictionary to storage URL and its value.
                    dstURL={}
                    dstURL.update(lstSub[j])                
                    
                    #URL Value can be None sometime,we will not go to the page when the value is 'NONE'.
                    #if the value of 'KEY_URL' not NONE,we will got the page by 'navigate' function.
                    if dstURL[KEY_URL]!=KEY_URL_NONE:
                        ret = ie.navigate(dstURL[KEY_URL])
                        if ret == False:
                            ie.quit()
                            #write logging
                            log_public(WEB_ERR_NO_0001+dstURL[KEY_URL])
                            self.m_ERROR_MSG = WEB_ERR_NO_0001+dstURL[KEY_URL]
                            return False
                        
                        if KillCA == 'CAON':
                            #IE 8 need to click 'overridelink'
                            #IE 6 need to click 'CA authentication dialog'
                            if nVer == 8:                                        
                                time.sleep(1)
                                ret = ie.clickLink('overridelink')
                                #encode
                                if ret == False:
                                    ie.quit()
                                    #write logging
                                    log_public(WEB_ERR_NO_0001+dstURL[KEY_URL])
                                    self.m_ERROR_MSG = WEB_ERR_NO_0001+dstURL[KEY_URL]
                                    return False
                                
                                KillCA = False #not need to kill next time open URL                                                                
                            elif nVer == 6:
                                time.sleep(1)
                                KillCA = False   
                            
                else:
                    #get line_operation.
                    dstComb = {}
                    dstComb.update(lstSub[j])
                    
                    #if 'ASSIST' have '//',This line_operation will be ignore.
                    if dstComb[KEY_ASSIST]== KEY_COMMENT:                        
                        continue
                    
                    #dispatch line_operation.include kinds(set text box, set check box,select list box,...)
                    Value = dstComb[KEY_CONTROLTYPE]
                    if Value == KEY_WEB_TYPE_TEXTBOX:                        
                        if ie.setTextBox(dstComb[KEY_CONTROLNAME], dstComb[KEY_CONTROLVALUE]) == False:
                            log_public(WEB_ERR_NO_0003+dstComb[KEY_CONTROLNAME])
                            self.m_ERROR_MSG = WEB_ERR_NO_0003+dstComb[KEY_CONTROLNAME]
                            return False
                        
                    elif Value== KEY_WEB_TYPE_CHECKBOX:
                        if self.MainCheckBox(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                            log_public(WEB_ERR_NO_0004+dstComb[KEY_CONTROLNAME])
                            self.m_ERROR_MSG = WEB_ERR_NO_0004+dstComb[KEY_CONTROLNAME]
                            return False

                    elif Value == KEY_WEB_TYPE_LISTBOX:
                        if self.MainListBox(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                            log_public(WEB_ERR_NO_0005+dstComb[KEY_CONTROLNAME])
                            self.m_ERROR_MSG = WEB_ERR_NO_0005+dstComb[KEY_CONTROLNAME]
                            return False 

                    elif Value == KEY_WEB_TYPE_BUTTON:
                        if self.MainButton(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME]) == False:
                            log_public(WEB_ERR_NO_0006+dstComb[KEY_CONTROLNAME])    
                            self.m_ERROR_MSG =  WEB_ERR_NO_0006+dstComb[KEY_CONTROLNAME]                      
                            False

                    elif Value == KEY_WEB_TYPE_WAIT:
                        if self.waitEvent(dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                            log_public(WEB_ERR_NO_0007+dstComb[KEY_CONTROLNAME])
                            self.m_ERROR_MSG =  WEB_ERR_NO_0007+dstComb[KEY_CONTROLNAME]
                            return False

                    elif Value == KEY_WEB_TYPE_JAVASCRIPT:                        
                        if self.MainJavaScript(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME]) == False:
                           log_public(WEB_ERR_NO_0008+dstComb[KEY_CONTROLNAME])   
                           self.m_ERROR_MSG = WEB_ERR_NO_0008+dstComb[KEY_CONTROLNAME]
                           return False

                    elif Value == KEY_WEB_TYPE_GROUP_CHECKBOX:
                        if  self.GetGoupCheckBoxIndex(ie,dstComb[KEY_CONTROLNAME]) == False:
                           log_public(WEB_ERR_NO_0009+dstComb[KEY_CONTROLNAME])  
                           self.m_ERROR_MSG = WEB_ERR_NO_0009+dstComb[KEY_CONTROLNAME]
                           return False   
        #close ie after operation.                
        ie.quit()     
    
      

    #If web page have group,we use this function to get the index.             
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
        if strAssist == KEY_GROUP:
            myControlName = self.findButtonChangeId(obj_ie,strControlName)
        
        if obj_ie.clickButton(myControlName) == False:
            return False
        
        return True
                      
    #when the button at some group,we need change index.
    def findButtonChangeId(self,obj_ie,strControlName):
        
       strL = 'id_'
       strR = '_'
       
       if self.m_Group_Idx == -1:
           return False
       
       strGroupIndex = str(self.m_Group_Idx) 
       strNewControlName = ''
       
       idx = strControlName.find('(')
       if idx > 0:
           strControlName = strControlName[0:idx]  
            
       strNewControlName = strL+strControlName+strR+strGroupIndex

       return strNewControlName 
   
    
    #java operation main function                            
    def MainJavaScript(self,obj_ie,strAssist,strControlName):

        myControlName = strControlName
        if strAssist ==KEY_GROUP:
            myControlName = self.findJavaScriptChangeId(strControlName)
        
        if obj_ie.executeJavaScript(myControlName) == False:
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
        
        if obj_ie.selectListBox(myControlName, strControlValue) == False:
            return False
        
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
    def waitEvent(self,EventName,TimeOut):
        
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

        log_public(strTempWnd)
                      
        strTempBtn = strTemp[strTemp.find('&&')+2:len(strTemp)]
        strTempBtn = strTempBtn[strTempBtn.find('=')+1:len(strTempBtn)]


                
        nTime = 1
        aWindow = 0

        clickCancel = cModalPopUp.handlePopup('Confirm',strTempBtn) 
        clickCancel.popupName = strTempWnd
        clickCancel.start()
        return clickCancel
    
    #wait dialog function, end    
    def dialogEventEnd(self,obj_Cancel):
        obj_Cancel.join()
        

    # get version of ie. different version have different operation.            
    def getIEVersion(self,obj_ie):

        obj_ie.executeJavaScript(KEY_IE_VERSION)
        IEVersion = obj_ie.getDivValue('iversion','innerHTML') 
            
        idxStt = IEVersion.find('MSIE')

        idxEnd = IEVersion.find(';',idxStt,len(IEVersion))

        VersionKey = IEVersion[idxStt:idxEnd]
            
        if VersionKey.find('8')>=0:
            return 8
        elif VersionKey.find('6')>=0:
            return 6
        else:
            return False
       
       
"""     
if __name__ == "__main__":
    myObj = Class_RW_Excel();      
    cst = myObj.GetErrorInfo()
    print cst
"""