# -*- coding: gb18030 -*- 
#-----------------------------------------------------------------------------
# Name:        xlrt.py
# Purpose:     
#
# Author:      gongke
#
# Created:     2013/12/21
# RCS-ID:      $Id: SNMP_OPER.py $,USE FOR snmp operation
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
#Test_Result_Str ='娴嬭瘯缁撴灉'

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
KEY_TEST_LIST_SCPT_RST_NAME_1 = u"测试脚本"
KEY_TEST_LIST_SCPT_RST_NAME_2 = u"测试执行结果"
KEY_TEST_LIST_SCPT_RST_NAME_3 = u"测试步骤执行情况"
KEY_TEST_LIST_SCPT_RST_NAME_4 = u"测试详细结果"
KEY_TEST_LIST_SCPT_RST_NAME_5 = u"测试结果"
KEY_TEST_LIST_SCPT_RST_NAME_6 = u"失败原因"

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

KEY_END = u"-"
KEY_M  =u"："
import re,string,xlwt,public,codecs,sys,os
import locale
from public import *

class write_xlwt():
    def __init__(self,file_name ='',sheet='AutoTestResult',debug_flag='1'):
        self.wbk=xlwt.Workbook(encoding = 'gb18030')
        self.sheet = self.wbk.add_sheet(sheet,cell_overwrite_ok=True)
        self.filename = self.save_result(file_name)
        self.tmp_modulename = ''
        self.start_module_row = 13
        self.dstRst_total_mod ={'DoneNum':'0','OKNum':'0','NGNum':'0'}
        self.mod_row_offset = 0
        
        try:
            
            font1 = xlwt.Font()
            font1.name = 'Times New Roman'  
            font1.bold = True
            
            borders1 = xlwt.Borders()
            borders1.left = xlwt.Borders.DASHED 
            borders1.right = xlwt.Borders.DASHED 
            borders1.bottom = xlwt.Borders.DASHED 
            borders1.top = xlwt.Borders.DASHED 
            self.style1 = xlwt.XFStyle()
            self.style1.font = font1
            self.style1.borders  = borders1
        
            self.style2 = xlwt.easyxf('pattern: pattern solid, fore_colour sea_green;')
            font2 = xlwt.Font()
            font2.name = 'SimSun' 
            font2.height = 0x00E6
            font2.bold = True
            self.style2.font =  font2
            self.style2.borders = borders1
        
            self.style3 = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
            font3 = xlwt.Font()
            font3.bold = True
            font3.name = 'SimSun' 
            font3.height = 0x00C8
            self.style3.font = font3
            self.style3.borders = borders1
        
        
            self.style4 = xlwt.easyxf('pattern: pattern solid, fore_colour ice_blue;')
            font4 = xlwt.Font()
            font4.name = 'SimSun' 
            font4.height = 0x00C8
            font4.bold = True
            self.style4.font = font4
            self.style4.borders = borders1
        
            self.style5 = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;')
            self.style5.font = font4
            self.style5.borders = borders1
        
        
            self.style6 = xlwt.XFStyle()
            font5 = xlwt.Font()
            font5.name = 'Verdana' 
            font5.bold = True
            font5.underline = xlwt.Font.UNDERLINE_DOUBLE
            font5.colour_index = 4
            self.style6.font =font5
            self.style6.borders = borders1
        
            self.style7 = xlwt.XFStyle()
            font6 = xlwt.Font()
            font6.name = 'Verdana' 
            font6.bold = True
            font6.colour_index = 6
            self.style7.font =font6
            self.style7.borders = borders1
        
        
            self.style8 = xlwt.XFStyle()
            font7 = xlwt.Font()
            font7.name = 'Verdana' 
            font7.bold = True
            font7.colour_index = 8
            self.style8.font =font7
            self.style8.borders = borders1
        
            self.style9 = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
            borders2 = xlwt.Borders()
            borders2.left = xlwt.Borders.DASHED 
            borders2.right = xlwt.Borders.DASHED 
            borders2.bottom = xlwt.Borders.DASHED 
            borders2.top = xlwt.Borders.DASHED 
            borders2.bottom_colour = 0x40
            borders2.top_colour = 0x40
            self.style9.font = font1
            self.style9.borders = borders2
        
            self.style10 = xlwt.easyxf('pattern: pattern solid, fore_colour sea_green;')
            font8 = xlwt.Font()
            font8.height = 0x00E6
            font8.bold = True
            self.style10.font = font8
            self.style10.borders = borders2
            
            self.style11 = xlwt.XFStyle()
            font9 = xlwt.Font()
            font9.name = 'Verdana' 
            font9.bold = True
            font9.colour_index = 0x28
            self.style11.font =font9
            self.style11.borders = borders1
            
        except Exception,e:
            log_print(e)
            pass
    
        
        
        
    def write_excel_write_Title(self,version,keyword):
        for x in range(0,9):
            if x ==1:
                self.sheet.write(0,x,version + keyword,self.style2)
            else:
                self.sheet.write(0,x,'',self.style2)
                
                
    def write_excel_write_smallTitle(self,version,keyword,row):
        for x in range(0,9):
            if x==0:
                self.sheet.write(row,0,keyword,self.style3)
            else:
                self.sheet.write(row,x,'',self.style3)
        
    def write_excel_write_resultinfo(self,version,keyword,row,cell):
        for x in range(0,9):
            if x==cell:
                self.sheet.write(row,0,keyword,self.style1 )
            else:
                self.sheet.write(row,x,'',self.style1 )
                  
    def write_excel_write_cell(self,version,keyword,row,cell):
        for x in range(0,9):
            if x==cell:
                self.sheet.write(row,cell,keyword,self.style1 )
                break
                
                
    def write_model_title(self,mod_name,loop,dstReport):
        #print 'Fuction write_model_title'
        row = self.start_module_row
        for x in range(0,9):
            if x==0:
                keyword = 'MODNAME:'
            elif x==1:
                keyword = mod_name
            elif x ==3:
                keyword = loop 
            else:
                keyword =''
            try:
                self.sheet.write(row,x,keyword,self.style4)
            except Exception ,e:
                log_print(e)
                pass
        self.start_module_row = self.start_module_row + 1
        
        row = self.start_module_row
        for x in range(0,9):
            if x ==1:
                keyword = KEY_RESULT_DONE
            elif x ==2:
                keyword = KEY_RESULT_OK_NUM
            elif x ==3:
                keyword = KEY_RESULT_NG_NUM
            elif x ==2:
                keyword = KEY_RESULT_RATE
            else:
                keyword =' '
            try:
                self.sheet.write(row,x,keyword,self.style5)
            except Exception ,e:
                log_print(e)
                pass
        
        self.start_module_row = self.start_module_row + 1
        row = self.start_module_row
        self.dstRst_total_mod ={'DoneNum':'1','OKNum':'0','NGNum':'0'}
        rate ='100%'
        for x in range(0,9):
            if x ==1:
                keyword = self.dstRst_total_mod['DoneNum']
            elif x ==2:
                keyword = self.dstRst_total_mod['OKNum']
            elif x ==3:
                keyword = self.dstRst_total_mod['NGNum']
            elif x ==4:
                keyword = rate
            else:
                keyword =''
            try:
                self.sheet.write(row,x,keyword,self.style1)
            except Exception ,e:
                log_print(e)
        
        
        self.mod_row_offset  = 1 
        row = self.start_module_row + self.mod_row_offset
        for x in range(0,9):
            if x ==0:
                keyword = KEY_TEST_LIST_NO
            elif x ==1:
                keyword = KEY_TEST_LIST_SCPT_RST_NAME_1
            elif x ==2:
                keyword = KEY_TEST_LIST_SCPT_RST_NAME_2
            elif x ==3:
                keyword = KEY_TEST_LIST_SCPT_RST_NAME_3
            elif x ==4:
                keyword = KEY_TEST_LIST_SCPT_RST_NAME_4
            elif x ==5:
                keyword = KEY_TEST_LIST_SCPT_RST_NAME_5
            else:
                keyword =''
            self.sheet.write(row,x,keyword,self.style1)
        self.mod_row_offset =2
        self.write_model_value(mod_name,loop,dstReport)
        
    def excel_type3(self):
        return self.style5
    
    def excel_type2(self):
        return self.style4
    
    def excel_type1(self):
        return self.style1
    
    def excel_type4(self):
        return self.style6
    
    def excel_type5(self):
        return self.style7
    
    def excel_type6(self):
        return self.style8
    
    def fill_txt(self,txtfile):
        file_name = txtfile.split('\\')[-1]
        if file_name.endswith('.txt')==True:
            return file_name.strip('.txt')
        else:
            return file_name
        
    def get_log_file(self,file_case):
        
        path1 =  os.path.abspath(sys.argv[0])
        findstr = 'Simu_'
        path2 = Getfindpath(path1,findstr)
        file =''
        if path1.endswith('.exe')==False:
            file =path2 + '\\AutoTestLog.log'
        else:
            file =path2 +'\\dist\\AutoTestLog.log'
        tmp_file = file_case.strip('.txt')+ 'AutoTestLog.txt'
        os.rename(file,tmp_file)
        return tmp_file
    
    def write_model_done(self,row):
        keyword = None
        for x in range(0,9):
            if x==1:
                keyword = str(string.atoi(self.dstRst_total_mod['DoneNum'])-1)
            elif x==2:
                keyword = self.dstRst_total_mod['OKNum']
            elif x==3:
                keyword = self.dstRst_total_mod['NGNum']
            elif x==4:
                keyword = str(string.atoi(self.dstRst_total_mod['OKNum'])*100 / (string.atoi(self.dstRst_total_mod['DoneNum'])-1)) + '%'
            else:
                keyword =''
            self.sheet.write(row,x,keyword,self.style8)
        
    def write_model_value(self,mod_name,loop,dstReport):
        #print 'Fuction write_model_value'
        row = self.start_module_row + self.mod_row_offset
        keyword = None
        for x in range(0,9):
            Hylink_Flag = False
            if x ==0:
                keyword = self.dstRst_total_mod['DoneNum']
            elif x ==1:
                keyword = dstReport['ScriptName']
                #keyword = '.\\'+dstReport['ScriptName'].split('\\')[-2] + '\\'+self.fill_txt(dstReport['ScriptName'])
                Hylink_Flag = True
            elif x ==2:
                keyword = '.\\'+dstReport['ScriptRestName'].split('\\')[-2] + '\\'+self.fill_txt(dstReport['ScriptRestName'])
            elif x ==3:
                keyword = dstReport['ScriptRestName']
                Hylink_Flag = True
            elif x ==4:
                keyword = self.get_log_file(dstReport['ScriptRestName'])
                Hylink_Flag = True
            elif x ==5:
                keyword = dstReport['Result']
            else:
                keyword =''
            if Hylink_Flag==True:
                tmp_str_path ='\\\\'.join(keyword.split('\\'))
                if x==3:
                    tmp_st2 = self.fill_txt(dstReport['ScriptRestName'])
                    try:
                        self.sheet.write_merge(row,row,x,x,xlwt.Formula("HYPERLINK" +  '("'+tmp_str_path+'";"'+tmp_st2+'")'),self.style6)
                    except Exception ,e:
                        log_print(e)
                elif x ==1:
                    tmp_st2 = self.fill_txt(dstReport['ScriptName'])
                    try:
                        self.sheet.write_merge(row,row,x,x,xlwt.Formula("HYPERLINK" +  '("'+tmp_str_path+'";"'+tmp_st2+'")'),self.style11)
                    except Exception,e:
                        log_print(e)
                else:
                    tmp_st2 = self.fill_txt(dstReport['ScriptRestName'])
                    try:
                        self.sheet.write_merge(row,row,x,x,xlwt.Formula("HYPERLINK" +  '("'+tmp_str_path+'";"'+tmp_st2+'")'),self.style7)
                        
                    except Exception ,e:
                        log_print(e)
            else:
                self.sheet.write(row,x,keyword,self.style1)
        self.dstRst_total_mod['DoneNum'] = str(self.mod_row_offset)
        try:
            dstReport['Result'].find(KEY_RESULT_OK)
        except Exception,e:
            log_print(e)
            
        if (dstReport['Result'].find(KEY_RESULT_OK))>-1:
            self.dstRst_total_mod['OKNum'] = str(string.atoi(self.dstRst_total_mod['OKNum']) + 1)
        else:
            self.dstRst_total_mod['NGNum'] = str(string.atoi(self.dstRst_total_mod['NGNum']) + 1)
        self.write_model_done(row-self.mod_row_offset)
       
        
            
    def write_excel_model(self,strfileName,dstReport,case_name,log='',logbak='',strTime='2014-00-00-00',version=' manual_test'):
        #print 'Fuction write_excel_model'
        mod_name = ''
        loop = ''
        mod_all = ''
        for x in dstReport["ScriptRestName"].split('\\'):
            if x.upper().find('MODULE_')>-1:
                mod_name = x.split('_loop')[0]
                loop ='loop:'+ x.split('_loop')[-1]
                mod_all = x
                break
        if mod_all != self.tmp_modulename:
            self.start_module_row = self.start_module_row + 1 + self.mod_row_offset
            self.mod_row_offset = 0
            self.tmp_modulename = mod_all
            self.write_model_title(mod_name,loop,dstReport)
        else:
            self.mod_row_offset  = self.mod_row_offset + 1
            self.write_model_value(mod_name,loop,dstReport)
        self.save_result(strfileName)
 
        
        
    def write_ReportWt(self,strfileName,dstRst,dstReport,log='',logbak='',strTime='2014-00-00-00',version=' manual_test'):
        #print 'Fuction write_ReportWt'
        #print 'log,logbak:',log,logbak
        self.write_excel_write_cell(version,strTime,4,1)
        self.write_excel_write_cell(version,dstRst["Result"],8,1)
        self.write_excel_write_cell(version,dstRst["TotalNum"],10,0)
        self.write_excel_write_cell(version,dstRst["DoneNum"],10,1)
        self.write_excel_write_cell(version,dstRst["NotDoneNum"],10,2)
        self.write_excel_write_cell(version,dstRst["OKNum"],10,3)
        self.write_excel_write_cell(version,dstRst["NGNum"],10,4)
        self.write_excel_write_cell(version,dstRst["Rate"],10,5)
         
        self.write_excel_model(strfileName,dstReport,log,logbak,strTime,version)
        self.save_result(strfileName)
        
        
        
    def write_ReportInt(self,filename,folder,version=' manual_test',strTime='2014-00-00-00'):
        #print 'Fuction write_ReportInt'
        dstRst = {"TotalNum":"0","DoneNum":"0","NotDoneNum":"0","OKNum":"0","NGNum":"0","Rate":"0"}
        self.write_excel_write_Title(version,KEY_FILE_TITLE) 
        self.write_excel_write_smallTitle(version,KEY_TEST_INFO,1)
        self.write_excel_write_smallTitle(version,KEY_RESULT,7)
        self.write_excel_write_smallTitle(version,KEY_TEST_LIST,11)
        
        self.write_excel_write_resultinfo(version,KEY_TEST_INFO_VERSION,2,0)
        self.write_excel_write_resultinfo(version,KEY_TEST_INFO_TIME_ST,3,0)
        self.write_excel_write_resultinfo(version,KEY_TEST_INFO_TIME_END,4,0)
        self.write_excel_write_resultinfo(version,KEY_TEST_INFO_PATH_SCPT,5,0)
        self.write_excel_write_resultinfo(version,KEY_TEST_INFO_PATH_SCPT_RST,6,0)
        
        self.write_excel_write_cell(version,strTime,3,1) 
        self.write_excel_write_cell(version,version,2,1)
        self.write_excel_write_cell(version,strTime,4,1)
        
        self.write_excel_write_cell(version,folder,5,1)
        result_path =os.path.dirname( self.filename)
        self.write_excel_write_cell(version,result_path,6,1)
        
        
        self.write_excel_write_cell(version,KEY_RESULT_VALUE,8,0)
        self.write_excel_write_cell(version,KEY_RESULT_TOTAL,9,0)
        self.write_excel_write_cell(version,KEY_RESULT_DONE,9,1)
        self.write_excel_write_cell(version,KEY_RESULT_NOT_DONE,9,2)
        self.write_excel_write_cell(version,KEY_RESULT_OK_NUM,9,3)
        self.write_excel_write_cell(version,KEY_RESULT_NG_NUM,9,4)
        self.write_excel_write_cell(version,KEY_RESULT_RATE,9,5)
        
        self.write_excel_write_cell(version,dstRst["TotalNum"],10,0)
        self.write_excel_write_cell(version,dstRst["DoneNum"],10,1)
        self.write_excel_write_cell(version,dstRst["NotDoneNum"],10,2)
        self.write_excel_write_cell(version,dstRst["OKNum"],10,3)
        self.write_excel_write_cell(version,dstRst["NGNum"],10,2)
        self.write_excel_write_cell(version,dstRst["Rate"],10,3)
        
        self.save_result(self.filename)
        
        
        
    def write_result(self,filename):
        file_object = open(filename,"r")
        textlist = file_object.readlines()
        file_object.close()
        tmp_line = 0
        
        for x in textlist:
            tmp_str = ''
            split_str =' '
            tmp_str  = x.strip().strip("|").strip('>>>').strip('-').strip().strip(KEY_END.encode('gb18030'))
            if len(tmp_str)==0:
                continue
            if tmp_line == 0:
                t_row = xlwt.Row(tmp_line,self.sheet)
                t_row.set_cell_blank(10)
            if   tmp_str.find(' ')>-1:
               split_str = ' ' 
            elif tmp_str.find("|")>-1:
                split_str = "|"
            elif tmp_str.find(KEY_M.encode('gb18030'))>-1:
                split_str = KEY_M.encode('gb18030')
            tmp_cow = 0
            for y in tmp_str.split(split_str):
                y = y.strip("|").strip()
                if len(y)==0:
                    continue 
                if len(tmp_str.split(split_str))==1:
                    
                    if tmp_line==0:
                        self.sheet.write(tmp_line,0,'',self.style10)
                        self.sheet.write(tmp_line,1,y,self.style10)
                        
                    else:
                        self.sheet.write(tmp_line,tmp_cow,y,self.style9)
                        self.sheet.write(tmp_line,1,'',self.style9)
                    self.sheet.write(tmp_line,2,'',self.style9)
                    self.sheet.write(tmp_line,3,'',self.style9)
                    self.sheet.write(tmp_line,4,'',self.style9)
                    self.sheet.write(tmp_line,5,'',self.style9)
                else:
                    if y.find('\\')>-1:
                        if y.split('\\')[-1].find('.txt')>-1:
                            y = y.split('\\')[-1].split('.txt')[0]
                    self.sheet.write(tmp_line,tmp_cow,y,self.style9)
                
                tmp_cow = tmp_cow + 1
            tmp_line = tmp_line + 1
        
    def save_result(self,filename):
        #print 'Fuction save_result'
        #print 'filename:',filename
        if filename.endswith('.xls') == False:
            filename = filename.strip('.txt') + '_excel.xls'
        self.wbk.save(filename)
        return filename
                
    def write_save(self,filename):
        self.write_result(filename)
        filename = self.save_result(filename)
        return filename
        
if __name__ == "__main__":
    filename = 'E:\\Simu_server\\result\\result20140718_145504\\AUTO_TEST_REPORT_Manual_Test_20140718_145504.txt'
    print 'sys.getdefaultencoding:',sys.getdefaultencoding()
    print 'sys.getfilesystemencoding:',sys.getfilesystemencoding()
    print 'sys.getfilesystemencoding:',sys.getfilesystemencoding()
    #print 'locale.getpreferredencoding:',locale.getpreferredencoding()
    
    test_file = write_xlwt()
    test_file.write_save(filename)
    
        

