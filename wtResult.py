# -*- coding: gb18030 -*- 
from __future__ import with_statement
#-----------------------------------------------------------------------------
# Name:        wtResult.py
# Purpose:     Create and Write result
#
# Author:      <chenshengcong>
#
# Created:     2013/02/27
# RCS-ID:      $Id: wtResult.py $
# Copyright:   (c) 2013
# Version:     <0.0.1> - Create
#-----------------------------------------------------------------------------
#<0.0.2>:modify support chiness code
#<0.0.3>:Upgrade for version recoard.chen sheng cong @2013/03/08
#<0.0.4>:Upgrade.Create Test Report.chen sheng cong @2013/03/16
#<0.0.4>:update.Support chinese for report list.chen sheng cong @2013/03/25
import os
import time
import re,string,xlwt,public,codecs,sys
import locale
from public import *
from write_excel import *
import shutil

#---------------------------
KEY_UNICODE = 'gb18030'

KEY_OPRESULT_NANE ="Opresult"
KEY_FILE_NANE= "OPRESULT"
KEY_FILE_FORMAT = ".txt"
KEY_HEAD_START = u"//--------------------测试信息--------------------//\n"

KEY_HEAD_TCNAME =u"//测试用例名称："
KEY_HEAD_TOTALTIME=u"//脚本执行总时间："
KEY_HEAD_RESULT=u"//测试结果(OK/NG)："
KEY_HEAD_COMMENT=u"//备注："
KEY_HEAD_TESTTIME=u"//测试日期："
KEY_HEAD_TESTER=u"//测试者："
KEY_HEAD_VERSION = u"//版本信息："  #add version @2013/3/8/by chen sheng cong
KEY_END =       u"//------------------------------------------------//\n"
KEY_TAIL_START = u"//--------------------测试结果--------------------//\n"
#------------------------
KEY_LINE_SEPR = "//"
KEY_LINE_SEPR_D = "\\"
KEY_LINE_BLANK_MODEL = "                "
KEY_LINE_BLANK_COMMAND = "                          "
KEY_LINE_FEET ="\n"
KEY_CON = "_"
#KEY_ERRR_LN = u"出错位置:第"
KEY_ERRR_LN = u"总共:"
#KEY_ERRR_REASON = u"行，出错原因："
KEY_ERRR_REASON = u" 个NG"
#------------------------
KEY_TYPE_MODEL = "MODEL"
KEY_TYPE_COMMAND = "COMMAND"
KEY_RESULT_OK = "OK"
KEY_RESULT_NG = "NG"
KEY_TIME_FORMAT = "%Y%m%d_%H%M%S"
KEY_LOOP = "_loop"
#-------------------------

#Test Report
#------------------------------------------------------------------------
KEY_WERT_CHART = "|"
KEY_HOR_CHAR = "-"
KEY_SPACE_CHAR = " "
#------------------------------------------------------------------------
KEY_FILE_NAME = "AUTO_TEST_REPORT"
KEY_FILE_TITLE = u"自动化测试报告"
KEY_TEST_INFO = u"测试信息"
KEY_TEST_INFO_VERSION = u"测试版本："
KEY_TEST_INFO_TIME_ST = u"测试开始时间："
KEY_TEST_INFO_TIME_END = u"测试结束时间："
KEY_TEST_INFO_PATH_SCPT = u"测试脚本路径："
KEY_TEST_INFO_PATH_SCPT_RST = u"测试脚本结果路径："
#------------------------------------------------------
KEY_TEST_LIST = u"测试执行清单"
KEY_TEST_LIST_NO = u"序号"
KEY_TEST_LIST_RESULT = u"测试结果"
KEY_TEST_LIST_SCPT_NAME = u"测试用例名称"
KEY_TEST_LIST_SCPT_RST_NAME = u"测试脚本结果名称"
KEY_RESULT_OK = "OK"
KEY_RESULT_NG = "NG"
#------------------------------------------------------
KEY_RESULT = u"测试结果"
KEY_RESULT_VALUE = u"测试结果："
KEY_RESULT_TOTAL =  u"总数量"
KEY_RESULT_DONE =  u"执行数量"
KEY_RESULT_NOT_DONE= u"未执行数量"
KEY_RESULT_OK_NUM= u"OK数量"
KEY_RESULT_NG_NUM= u"NG数量"
KEY_RESULT_RATE = u"正确率"
KEY_RESULT_CHE_OK = u"成功"
KEY_RESULT_CHE_NG = u"失败"
#------------------------------------------------------
KEY_SPACE_8 = "        "
KEY_SPACE_15 = "               "
KEY_SPACE_17 = "                 "
KEY_SPACE_19 = "                   "

class clsWtResult:
    #-----------------------------------------------------------------------------
    # Name:        funWtResultHead - create resul file and write header.
    # Parameter:    foldName-input folder path. to save result file.
    #               strVersion - version information.eg,"MIPS_1018L1.8v8_R29_T10"
    #               strTcName-Test Script file path.(must include file name.)
    #               strTester-recoard tester name.
    # return:       result file name.
    # Author:      <chenshengcong>
    # Created:     2013/02/27
    # Version:     <0.0.1> - Create
    #-----------------------------------------------------------------------------
    def funWtResultHead_mod(self,foldName,strVersion,strTcName,loop='1',strTester = "tester001"):
        fileName = ""
        strTcTempName = ""
        #print 'funWtResultHead_mod loop:',loop
        #strTcTempName =  strTcName.encode(KEY_UNICODE).split("\\")[-1] #use open() to create file,not use encode().        
        strTcTempName =  strTcName.split("\\")[-1]    
        strTcTempName = strTcTempName.split(".txt")[0]

        strTime = time.strftime(KEY_TIME_FORMAT)
        if strVersion =='':
            fileName = foldName +  KEY_LINE_SEPR_D + strTcTempName +KEY_CON+KEY_FILE_NANE +KEY_LOOP+loop+ KEY_CON+ strTime + KEY_FILE_FORMAT
        else:
            fileName = foldName +  KEY_LINE_SEPR_D + strVersion + KEY_CON + strTcTempName +KEY_CON+KEY_FILE_NANE +KEY_LOOP+loop+ KEY_CON+ strTime + KEY_FILE_FORMAT
        
        
        
        try:
            fp = open(fileName,"a")
            fp.write(KEY_HEAD_START.encode(KEY_UNICODE))
            fp.write(KEY_HEAD_VERSION.encode(KEY_UNICODE)+strVersion+KEY_LINE_FEET)        
            fp.write(KEY_HEAD_TCNAME.encode(KEY_UNICODE)+strTcName.encode(KEY_UNICODE)+KEY_LINE_FEET)
            fp.write(KEY_HEAD_TESTTIME.encode(KEY_UNICODE)+strTime+KEY_LINE_FEET)
            #fp.write(KEY_HEAD_TESTER.encode(KEY_UNICODE)+strTester+KEY_LINE_FEET)
            fp.write(KEY_HEAD_TESTER.encode(KEY_UNICODE)+strTester+KEY_LINE_FEET)
            fp.write(KEY_END.encode(KEY_UNICODE))
            fp.write(KEY_LINE_FEET)
            fp.write(KEY_LINE_FEET)
            fp.write(KEY_LINE_FEET)
            fp.write(KEY_LINE_FEET)

            fp.close()
        except Exception,e:
            pass
        
        return fileName
        
    def funWtResultHead(self,foldName,strVersion,strTcName,strTester = "tester001"):    
           
        
        fileName = ""
        strTcTempName = ""

        #strTcTempName =  strTcName.encode(KEY_UNICODE).split("\\")[-1] #use open() to create file,not use encode().        
        strTcTempName =  strTcName.split("\\")[-1]    
        strTcTempName = strTcTempName.split(".")[0]

        strTime = time.strftime(KEY_TIME_FORMAT)
        fileName = foldName +  KEY_LINE_SEPR_D+ strVersion + KEY_CON + strTcTempName + KEY_CON+KEY_FILE_NANE + KEY_CON + strTime + KEY_FILE_FORMAT
        
        try:
            fp = open(fileName,"a")
            fp.write(KEY_HEAD_START.encode(KEY_UNICODE))
            fp.write(KEY_HEAD_VERSION.encode(KEY_UNICODE)+strVersion+KEY_LINE_FEET)        
            fp.write(KEY_HEAD_TCNAME.encode(KEY_UNICODE)+strTcName+KEY_LINE_FEET)
            fp.write(KEY_HEAD_TESTTIME.encode(KEY_UNICODE)+strTime+KEY_LINE_FEET)
            fp.write(KEY_HEAD_TESTER.encode(KEY_UNICODE)+strTester+KEY_LINE_FEET)
            fp.write(KEY_END.encode(KEY_UNICODE))
            fp.write(KEY_LINE_FEET)
            fp.write(KEY_LINE_FEET)
            fp.write(KEY_LINE_FEET)
            fp.write(KEY_LINE_FEET)
        except Exception,e:
            pass

        fp.close()

        return fileName
    
    
    #-----------------------------------------------------------------------------
    # Name:         funWtResultLine -write one line result.
    # Parameter:    fileName-name return by function funWtResultHead()
    #               strType-two kinds.eg:"#ftp" use "MODEL";eg:"init" use "COMMAND",
    #               strln-recoard line number.
    #               strRes-recoard result,two Value.eg:when test OK use "OK",when test error use "NG"
    #               strCommand - eg:"#ftp",or"cmd_command$    ping 192.168.4.232  -n 1, Received = 1"
    # Author:      <chenshengcong>
    # Created:     2013/02/27
    # Version:     <0.0.1> - Create
    #-----------------------------------------------------------------------------        
    def funWtResultLine_mod(self,fileName,strType,strln,strRes,strCommand):
        try:
            fp = open(fileName,"a")
            if strType == KEY_TYPE_MODEL :        
                strLineInfo = ""
                strLineInfo = KEY_LINE_SEPR+strln+KEY_LINE_SEPR+strRes+KEY_LINE_SEPR+KEY_LINE_BLANK_MODEL+strCommand+KEY_LINE_FEET       
                fp.write(strLineInfo)
        
            elif strType == KEY_TYPE_COMMAND:
                strLineInfo = ""
                strLineInfo = KEY_LINE_SEPR+strln+KEY_LINE_SEPR+strRes+KEY_LINE_SEPR+KEY_LINE_BLANK_COMMAND+strCommand+KEY_LINE_FEET
                fp.write(strLineInfo)       
            
            fp.close()
        except Exception,e:
            log_print(e,True)
            pass
            
        
    def funWtResultLine(self,fileName,strType,strln,strRes,strCommand):
        try:
            fp = open(fileName,"a")
        
            if strType == KEY_TYPE_MODEL :        
                strLineInfo = ""
                strLineInfo = KEY_LINE_SEPR+strln+KEY_LINE_SEPR+strRes+KEY_LINE_SEPR+KEY_LINE_BLANK_MODEL+strCommand+KEY_LINE_FEET       
                fp.write(strLineInfo)
        
            elif strType == KEY_TYPE_COMMAND:
                strLineInfo = ""
                strLineInfo = KEY_LINE_SEPR+strln+KEY_LINE_SEPR+strRes+KEY_LINE_SEPR+KEY_LINE_BLANK_COMMAND+strCommand+KEY_LINE_FEET
                fp.write(strLineInfo)       
            
            fp.close()
        except Exception,e:
            log_print(e,True)
            pass
        
        
    #-----------------------------------------------------------------------------
    # Name:        funWtTotal - write total result.
    # Parameter:    fileName--name return by function funWtResultHead()
    #               strRes-recoard result,two Value.eg:when test OK use "OK",when test error use "NG"
    #               strLn-recoard line number.
    #               strComment- When error happen,write error reason.
    # Author:      <chenshengcong>
    # Created:     2013/02/27
    # Version:     <0.0.1> - Create
    #-----------------------------------------------------------------------------        
    def funWtRetultTotal(self,fileName,strLn,strRes,strComment,scr_exec_time):
        try:
        
            fp = open(fileName,"a")
        
            fp.write(KEY_LINE_FEET)     
            fp.write(KEY_LINE_FEET)
            fp.write(KEY_LINE_FEET)     
            fp.write(KEY_LINE_FEET)
            fp.write(KEY_TAIL_START.encode(KEY_UNICODE))
            fp.write(KEY_HEAD_RESULT.encode(KEY_UNICODE)+strRes+KEY_LINE_FEET)
            if strRes == KEY_RESULT_NG:
                fp.write(KEY_HEAD_COMMENT.encode(KEY_UNICODE)+KEY_ERRR_LN.encode(KEY_UNICODE)+
                        strLn + KEY_ERRR_REASON.encode(KEY_UNICODE) + strComment+KEY_LINE_FEET)
            elif strRes == KEY_RESULT_OK:
                fp.write(KEY_HEAD_COMMENT.encode(KEY_UNICODE)+strComment+KEY_LINE_FEET)
            fp.write(KEY_HEAD_TOTALTIME.encode(KEY_UNICODE)+scr_exec_time+' seconds!'+KEY_LINE_FEET)
            fp.write(KEY_END.encode(KEY_UNICODE))
            fp.close()
        except Exception,e:
            log_print(e,True)
            pass
        
#***************************************************************************************************


    #-----------------------------------------------------------------------------
    # Name:        ReportInt - create test report.
    # Parameter:    foldName-input folder path. to save report file.
    #               strVersion - version information.eg,"MIPS_1018L1.8v8_R29_T10"
    #               strTcName-Test Script file path.
    # return:       result file name.(file's path and file's name). if fail,return None
    # Author:      <chen sheng cong>
    # Created:     2013/03/15
    # Version:     <0.0.1> - Create
    #-----------------------------------------------------------------------------
    def ReportInt(self,foldName,strVersion,strTcName): 
              
        if strVersion=='':
            strVersion = 'Manual_Test'
        try:
            fileName = None
            strTcTempName = ""
            dstRst = {"TotalNum":"0","DoneNum":"0","NotDoneNum":"0","OKNum":"0","NGNum":"0","Rate":"0"}

            strTime = time.strftime(KEY_TIME_FORMAT)
            fileName = foldName +  KEY_LINE_SEPR_D + KEY_FILE_NAME + KEY_CON + strVersion + KEY_CON + strTime + KEY_FILE_FORMAT
            
            write_tmp_file(fileName,'\\dist\\tmp_date\\tmp_param.ini','\\tmp_date\\tmp_param.ini')
            
            fp = open(fileName,"a")       
            
            #write TITLE
            self.fillHead_A(fp)
            self.fillHead_B(fp)       
            self.fillHead_C(fp)        
            self.fillHead_A(fp)
            
            self.fill(fp,KEY_LINE_FEET,2)  

            #write INFO                
            self.fillINFO_A(fp)
            self.fillINFO_B(fp)        
            self.fillINFO_C(fp,strVersion.decode(KEY_UNICODE),strTime,strTcName.decode(KEY_UNICODE),foldName.decode(KEY_UNICODE))              
            self.fillINFO_B(fp)        
            self.fill(fp,KEY_LINE_FEET,2)          
             
            #write result       
            self.fillRESULT_A(fp)
            self.fillRESULT_B(fp)        
            self.fillRESULT_C(fp)
            self.fillRESULT_B(fp)         
            self.fillRESULT_D(fp)
            self.fillRESULT_B(fp) 
            self.fillRESULT_E(fp,dstRst)
            self.fillRESULT_B(fp)    
            self.fill(fp,KEY_LINE_FEET,2)                              

            
            #write List    
            self.fillLIST_A(fp)
            self.fillLIST_B(fp)
            self.fillLIST_C(fp)
            self.fillLIST_B(fp)
                    
            fp.close()
            #print 'ReportInt fuction ....'
            self.xlwt_re = write_xlwt(fileName)
            
            self.xlwt_re.write_ReportInt(fileName,strTcName,strVersion,strTime)
            return fileName 
        
        except:
           return  fileName
           
    
    #-----------------------------------------------------------------------------
    # Name:        ReportWt - write every test result.
    # Parameter:    strfileName-input file name. filename will be return after call ReportInt() function
    #               dstRst - storage total result information.eg: {"Result":"OK","TotalNum":"10","DoneNum":"6","NotDoneNum":"4","OKNum":"4","NGNum":"2","Rate":"67%"}
    #               dstReport-storage script result information.eg:{"No":"1","Result":"OK","ScriptName":"3333.txt","ScriptRestName":"4444.txt"}
    #               strTester-recoard tester name.
    # return:       result file name
    # Author:      <chenshengcong>
    # Created:     2013/03/15
    # Version:     <0.0.1> - Create
    #-----------------------------------------------------------------------------
    def ReportWt(self,strfileName,dstRst,dstReport,log='',logbak=''): 
            
            
            try:
                #1,write Info end time
                strTime = time.strftime(KEY_TIME_FORMAT)
                self.Find_Replace(strfileName,"测试结束时间",strTime,15)
                #2,write result
                    
                self.Find_Replace(strfileName,"测试结果：",dstRst["Result"],41)
                            
                strRst = KEY_SPACE_8+dstRst["TotalNum"] + KEY_SPACE_15 + dstRst["DoneNum"]+ KEY_SPACE_17 +dstRst["NotDoneNum"] + KEY_SPACE_19 +dstRst["OKNum"] + KEY_SPACE_15 +dstRst["NGNum"] + KEY_SPACE_15 +dstRst["Rate"]           
        
                self.Find_Replace(strfileName,">>>",strRst,3) 
               
     
                #3,add list
                fp = open(strfileName,"a")
                self.fill(fp ,"|",1)            
                self.fill(fp ,dstReport["No"],0)        
                self.fill(fp ," ",5)          
                self.fill(fp ,dstReport["ScriptName"].decode(KEY_UNICODE),0)  
                self.fill(fp ," ",5)
                self.fill(fp ,dstReport["ScriptRestName"].decode(KEY_UNICODE),0)  
                self.fill(fp ," ",5)
                self.fill(fp ,dstReport["Result"],0)
                self.fill(fp,KEY_LINE_FEET,1)                                        
                self.fillLIST_B(fp)            
                
                fp.close()
                
                self.xlwt_re.write_ReportWt(strfileName,dstRst,dstReport,log,logbak)
                
                return True
            
            except:
                return False
                
   
    #fill list
    #---------------------------------------------------------------------------
    def fillLIST_A(self,fobj):
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_TEST_LIST,0)
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_LINE_FEET,1)           
  
  
    def fillLIST_B(self,fobj):
        self.fill(fobj,"|",1)
        self.fill(fobj,"-",103)
        self.fill(fobj,KEY_LINE_FEET,1)  
              
              
    def fillLIST_C(self,fobj):
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_TEST_LIST_NO,0)
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_TEST_LIST_SCPT_NAME,0)     
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_TEST_LIST_SCPT_RST_NAME,0) 
        self.fill(fobj,"|",1)   
        self.fill(fobj,KEY_TEST_LIST_RESULT,0) 
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_LINE_FEET,1)              
 
 
    #fill result
    #---------------------------------------------------------------------------
    def fillRESULT_A(self,fobj):    
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_RESULT,0)
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_LINE_FEET,1)   
  
    def fillRESULT_B(self,fobj):    
        self.fill(fobj,"|",1)
        self.fill(fobj,"-",103)
        self.fill(fobj,KEY_LINE_FEET,1)  

    def fillRESULT_C(self,fobj):    
        self.fill(fobj,"|",1)
        self.fill(fobj," ",30)
        self.fill(fobj,KEY_RESULT_VALUE,0)        
        self.fill(fobj," ",6)
        self.fill(fobj,KEY_LINE_FEET,1) 
                                

    def fillRESULT_D(self,fobj):    

        self.fill(fobj,"|",1)
        self.fill(fobj," ",10) 
        self.fill(fobj,KEY_RESULT_TOTAL,0)
        self.fill(fobj," ",10)     
        self.fill(fobj,KEY_RESULT_DONE,0) 
        self.fill(fobj," ",10)  
        self.fill(fobj,KEY_RESULT_NOT_DONE,0)     
        self.fill(fobj," ",10)  
        self.fill(fobj,KEY_RESULT_OK_NUM,0) 
        self.fill(fobj," ",10)              
        self.fill(fobj,KEY_RESULT_NG_NUM,0) 
        self.fill(fobj," ",10)              
        self.fill(fobj,KEY_RESULT_RATE,0)                     
        self.fill(fobj,KEY_LINE_FEET,1) 
        
 
    def fillRESULT_E(self,fobj,dstRst):      

        self.fill(fobj,">",3)
        self.fill(fobj," ",8)  
        self.fill(fobj,dstRst["TotalNum"],0) #total
        self.fill(fobj," ",15)     
        self.fill(fobj,dstRst["DoneNum"],0) #done
        self.fill(fobj," ",17)  
        self.fill(fobj,dstRst["NotDoneNum"],0) #no done    
        self.fill(fobj," ",19)  
        self.fill(fobj,dstRst["OKNum"],0) #OK
        self.fill(fobj," ",15)              
        self.fill(fobj,dstRst["NGNum"],0) #NG
        self.fill(fobj," ",15)              
        self.fill(fobj,dstRst["Rate"],0)  #rate    
        self.fill(fobj," ",6)                        
        self.fill(fobj,KEY_LINE_FEET,1) 
        
        
    #fill INFO       
    #---------------------------------------------------------------------------
    def fillINFO_A(self,fobj):
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_TEST_INFO,0)
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_LINE_FEET,1)   
    
    def fillINFO_B(self,fobj):
        self.fill(fobj,"|",1)
        self.fill(fobj,"-",66)
        self.fill(fobj,KEY_LINE_FEET,1)   
       
        
    def fillINFO_C(self,fobj,strVer,strTime,strTCPth,strTCRstPth):
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_TEST_INFO_VERSION+strVer,0)
        self.fill(fobj,KEY_LINE_FEET,1) 
        
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_TEST_INFO_TIME_ST+strTime,0)
        self.fill(fobj," ",2)
        self.fill(fobj,KEY_LINE_FEET,1)            

        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_TEST_INFO_TIME_END+strTime,0)
        self.fill(fobj," ",2)
        self.fill(fobj,KEY_LINE_FEET,1)  

        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_TEST_INFO_PATH_SCPT+strTCPth,0)
        self.fill(fobj,KEY_LINE_FEET,1)  

        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_TEST_INFO_PATH_SCPT_RST+strTCRstPth,0)
        self.fill(fobj,KEY_LINE_FEET,1)  
 
         
    #fill HEAD 
    #---------------------------------------------------------------------------
    def fillHead_A(self,fobj):
        self.fill(fobj," ",17)
        self.fill(fobj,"|",1)
        self.fill(fobj,"-",40)
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_LINE_FEET,1)
        
    def fillHead_B(self,fobj):
        self.fill(fobj," ",17)
        self.fill(fobj,"|",1)
        
        self.fill(fobj," ",12)
        self.fill(fobj,KEY_FILE_TITLE,0)        
        self.fill(fobj," ",14)
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_LINE_FEET,1)
                
    def fillHead_C(self,fobj):
        self.fill(fobj," ",17)
        self.fill(fobj,"|",1)
        self.fill(fobj," ",40)
        self.fill(fobj,"|",1)
        self.fill(fobj,KEY_LINE_FEET,1)      
    
    
    
    #--------------------------------------------------------------------------- 
    # write char to "txt" file. 
    #have two kinds. 
    #1-a string. 
    #2- a char,you can write same char more onetimes by iCount.
    def fill(self,fobj,strFLL,iCount=0):
        
        if iCount == 0:
            fobj.write(strFLL.encode(KEY_UNICODE))
        else:
            for idx  in range(0,iCount):
                fobj.write(strFLL)
               
               
               
    
          
        
    #---------------------------------------------------------------------------      
    #replace a string after find the key.
    #newfile-the file name,you need to open.
    #strFind-the key,you find.
    #strRepl- the string you want to replace(or write).     
    def Find_Replace(self,newfile,strFind,strRepl,iPos):
        lnum = 0
        with open(newfile,"r+") as fp:
            for my in fp:
                lnum +=1
                #print fp.readline()
            
            #print lnum
            iplsH = 0
            iplsT = 0
            fp.seek(0) 
            for num in range(0,lnum):   
                     
                mystr = fp.readline()   
                iplsT =  fp.tell()

                dix = mystr.find(strFind)
                dixrn = 0
                if dix != -1:
                    dixrn = mystr.find("\n")
                    
                    fp.seek(iplsH+iPos,0)           #clear
                    for i in range(iPos,dixrn):             
                        fp.write(" ") 
                                
                    fp.seek(iplsH+iPos+1,0)             
                    fp.write(strRepl) 
                    break
                iplsH = iplsT
 
        fp.close()
    
if __name__ == "__main__":
    
    newfile = "D:\\01_AutoTestTool_\\3_wtResult\\TXT_FORMAT"
    myobj = clsWtResult()
    name = "C:\\AC11我的.txt"
    version = "MISP_我的VER1.1.0"
    #strfileName = myobj.funWtResultHead(newfile,version,"C:\\AC11我的.txt")
    strfileName = myobj.ReportInt(newfile,version,u"C:\\")

   
    dstRst = {"Result":"OK","TotalNum":"1","DoneNum":"2","NotDoneNum":"3","OKNum":"4","NGNum":"5","Rate":"6"}
    dstReport = {"No":"1","Result":"OK","ScriptName":name,"ScriptRestName":"我的t.txt"}
    for i in range(0,3):
        myobj.ReportWt(strfileName,dstRst,dstReport)
        time.sleep(1)
    

#    myobj.funWtResultLine(strfileName,"MODEL","1","OK","#ftp")    
#    myobj.funWtResultLine(strfileName,"COMMAND","2","NG","mycommand$	root,cwcos login:,2")
    #myobj.Find_Replace(strfileName,"测试结束时间","20130315_192402",15)
#    myobj.funWtRetultTotal(strfileName,"NG","2","book not find")

    