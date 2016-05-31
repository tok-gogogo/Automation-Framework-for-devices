# -*- coding: gb18030 -*- 
#-----------------------------------------------------------------------------
# Name:        CrtlACWeb.py
# Purpose:     
#
# Author:      <gongke>
#
# Created:     2013/01/30
# RCS-ID:      $Id: CrtlACWeb.py $
# Copyright:   (c) 2006
# Version:     <0.1.1>
#-----------------------------------------------------------------------------
# Version events
# <0.1.0> Create
# <0.1.1> Add 'bCA'-parameter for OperateACWebPage(). Judge weather have CA authentication.

from PAM30 import PAMIE
import time
from WtLog import log_public
import win32gui
import thread 
import cModalPopUp

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
IE_DEBUG =True

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







class OprACWeb:
    
    m_Group_Idx = -1
    m_Obj_WaitDialog_Cancel = 0
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
                        IE_DEBUG = True
                        ret = ie.navigate(dstURL[KEY_URL])
                        
                        if ret == False:
                            ie.quit()
                            #write logging
                            log_public(WEB_ERR_NO_0001+dstURL[KEY_URL])
                            return False
                        
                        if IE_DEBU==True:
                            print '@@@@@@@@@@@@@@@@@@@open IE_DEBUG @@@@@@@@@@@@@@@@@@@'
                            print ie.pageGetText()
                            msg_print =  ie.pageGetText()
                            log_print(msg_print)
                            
                        if KillCA == True:
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
                            return False
                        
                    elif Value== KEY_WEB_TYPE_CHECKBOX:
                        if self.MainCheckBox(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                            log_public(WEB_ERR_NO_0004+dstComb[KEY_CONTROLNAME])
                            return False

                    elif Value == KEY_WEB_TYPE_LISTBOX:
                        if self.MainListBox(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                            log_public(WEB_ERR_NO_0005+dstComb[KEY_CONTROLNAME])
                            return False 

                    elif Value == KEY_WEB_TYPE_BUTTON:
                        if self.MainButton(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME]) == False:
                            log_public(WEB_ERR_NO_0006+dstComb[KEY_CONTROLNAME])                            
                            False

                    elif Value == KEY_WEB_TYPE_WAIT:
                        if self.waitEvent(dstComb[KEY_CONTROLNAME],dstComb[KEY_CONTROLVALUE]) == False:
                            log_public(WEB_ERR_NO_0007+dstComb[KEY_CONTROLNAME])
                            return False

                    elif Value == KEY_WEB_TYPE_JAVASCRIPT:                        
                        if self.MainJavaScript(ie,dstComb[KEY_ASSIST],dstComb[KEY_CONTROLNAME]) == False:
                           log_public(WEB_ERR_NO_0008+dstComb[KEY_CONTROLNAME])   
                           return False

                    elif Value == KEY_WEB_TYPE_GROUP_CHECKBOX:
                        if  self.GetGoupCheckBoxIndex(ie,dstComb[KEY_CONTROLNAME]) == False:
                           log_public(WEB_ERR_NO_0009+dstComb[KEY_CONTROLNAME])   
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
        print strTemp         
        if strTemp.find('&&') == -1:
            return False
        
        strTempWnd = strTemp[0:strTemp.find('&&')]
        strTempWnd = strTempWnd[strTempWnd.find('=')+1:len(strTempWnd)] 
        print  strTempWnd
        log_public(strTempWnd)
                      
        strTempBtn = strTemp[strTemp.find('&&')+2:len(strTemp)]
        strTempBtn = strTempBtn[strTempBtn.find('=')+1:len(strTempBtn)]
        print  strTempBtn 
        log_public(strTempBtn)
        log_public(2)
        print str(time.clock())
                
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
        print idxStt
        idxEnd = IEVersion.find(';',idxStt,len(IEVersion))

        VersionKey = IEVersion[idxStt:idxEnd]
            
        if VersionKey.find('8')>=0:
            return 8
        elif VersionKey.find('6')>=0:
            return 6
        else:
            return -1
        


        