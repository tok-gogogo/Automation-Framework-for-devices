#-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        read case excel
# Purpose:     
#
# Author:      gongke
#
# Created:     2014/01/15
# RCS-ID:      
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
import xlrd
import string
from public import * 
import types,os,sys,re

MODULE_FLAG = 'MODULE_'
CASE_FLAG = 'CASE'
SCRIPT_FLAG ='['
class readcase_excel():
    def __init__(self,filename = 'E:\\test_case_auto\\d\\t\\set_run.xls',sheetName = 'Sheet1'):
        self.filename = filename
        if self.filename.endswith('.xls')==True:
            self.path = os.path.dirname(self.filename)
        else:
            self.path = self.filename
        self.sheetName = sheetName
        self.dic_c = {}
        self.mod_name =''
        self.case_name=''
        self.script_name=''
        self.step_num = 0
        self.step_dic ={}
        self.loop_case = 0
        self.loop_mod = 0
        self.loop_srcipt = 0 
        
    def OpenexcelFile(self):
        obj_book = 0 
        file_exist(self.filename)
        try:
            obj_book = xlrd.open_workbook(self.filename)
            return obj_book
        except Exception,e:
            log_print(e)
            return obj_book
        
    def Excel_sheetName(self):
        obj_table = 0
        obj_book = 0 
        obj_book = self.OpenexcelFile()
        if obj_book == 0 :
            msg='Not find the excel:' + self.filename
            self.error = msg
            return obj_book
        for sheetname in obj_book.sheet_names():
            if self.sheetName == sheetname :
                obj_table = obj_book.sheet_by_name(sheetname)
                break
        return obj_table
    
    def Excel_read(self,filename_excel='',sheetName_excel=''):
        if filename_excel !='':
            self.filename = filename_excel
        if sheetName_excel!='':
            self.sheetName = sheetName_excel
        obj_table = self.Excel_sheetName()
        if obj_table == 0 :
            msg = 'find the excel: ' +self.filename +' but not find sheet name:' + self.sheetName
            log_print(msg)
            self.error = msg
            return None
        
        mod_num = -1
        case_num = -1
        script_num = -1
        tmp_mod_name = ''
        tmp_case_name =''
        tmp_script_name =''
        dic_run ={'DO':'Do','NO':'No'}
        
        #try:
        key_module = ''
        key_case =''
        key_script=''
        for row in range(1,obj_table.nrows):
                values =  {}
                for col in range(obj_table.ncols):
                    tmp_value = obj_table.cell(row,col).value
                    tmp_value =tmp_value.strip()
                    if len(tmp_value)==0:
                        continue
                    elif tmp_value.upper().startswith(MODULE_FLAG)==True:
                        #add module
                        mod_num = mod_num + 1
                        key_module = 'mod' + str(mod_num)
                        if self.dic_c.has_key(key_module)==False:
                            self.dic_c[key_module] ={tmp_value:{},'Loop':'1','Run':'Do','modname':tmp_value}
                            case_num = -1
                            tmp_mod_name = tmp_value
      
                    elif tmp_value.upper().startswith(CASE_FLAG)==True:
                        #add case
                        case_num = case_num + 1 
                        key_case ='case' + str(case_num)
                        if self.dic_c[key_module][tmp_mod_name].has_key(key_case)==False:
                            self.dic_c[key_module][tmp_mod_name][key_case] = {tmp_value:{},'Loop':'1','Run':'Do','casename':tmp_value}
                            tmp_case_name = tmp_value
                            script_num = -1
                            
                    elif tmp_value.upper().startswith(SCRIPT_FLAG)==True:
                        #add script
                        script_num = script_num + 1
                        key_script ='script' + str(script_num)
                        if self.dic_c[key_module][tmp_mod_name][key_case].has_key(key_script) ==False:
                            ab_path_script  = self.path +'\\'+tmp_mod_name+'\\'+tmp_case_name +'\\' + tmp_value +'.txt'
                            self.dic_c[key_module][tmp_mod_name][key_case][tmp_case_name][key_script] = {'scriptname':ab_path_script,'Loop':'1','Run':'Do'}
                            tmp_script_name = tmp_value
                            
                    elif dic_run.has_key(tmp_value.upper()) ==True:
                        if case_num==-1:
                            self.dic_c[key_module]['Run'] = tmp_value
                        elif script_num == -1:
                            self.dic_c[key_module][tmp_mod_name][key_case]['Run'] =tmp_value
                        else:
                            self.dic_c[key_module][tmp_mod_name][key_case][tmp_case_name][key_script]['Run'] =tmp_value
                            
                    elif len(re.findall('\d',tmp_value))>0:
                        if case_num==-1:
                            self.dic_c[key_module]['Loop'] = tmp_value
                        elif script_num == -1:
                            self.dic_c[key_module][tmp_mod_name][key_case]['Loop'] =tmp_value
                        else:
                            self.dic_c[key_module][tmp_mod_name][key_case][tmp_case_name][key_script]['Loop'] =tmp_value
                        break
                    else:
                        continue
        
        log_print(self.dic_c)
        return self.dic_c
    
        
    def mod_run(self):
        dic = self.dic_c
        num = 0
        while True:
            key ='mod' + str(num)
            self.loop_mod = 1 
            if dic.has_key(key)==True:
                name = dic[key]['modname'] 
                loop = string.atoi(dic[key]['Loop'])
                RunFlag = dic[key]['Run']
                self.mod_name = name
                if RunFlag.upper()=='NO':
                    num = num +1
                    continue 
                for x in range(loop):
                    print 'mod name:',name
                    self.case_run(dic[key][name])
                    self.loop_mod  = self.loop_mod  +1 
            else:
                break
            num = num +1
        
        
    def case_run(self,dic):
        num = 0
        while True:
            key = 'case' + str(num)
            self.loop_case = 1
            if dic.has_key(key)==True:
                name = dic[key]['casename'] 
                loop = string.atoi(dic[key]['Loop'])
                RunFlag = dic[key]['Run']
                self.case_name = name
                if RunFlag.upper()=='NO':
                    num = num +1
                    continue
                for x in range(loop):
                    print '        case name:',name
                    self.script_run(dic[key][name])
                    self.loop_case = self.loop_case  + 1
            else:
                break
            num = num + 1
        
    def script_run(self,dic):
        num = 0
        while True:
            key = 'script' + str(num)
            self.loop_srcipt = 1
            if dic.has_key(key)==True:
                print '                   script key:',key
                loop = string.atoi(dic[key]['Loop'])
                RunFlag=dic[key]['Run']
                filename = dic[key]['scriptname']
                if RunFlag.upper()=='NO':
                    num = num + 1
                    continue 
                for x in range(loop):
                    list_c =[]
                    list_c.append({'modname':self.mod_name})
                    list_c.append({'casename':self.case_name})
                    list_c.append({'scriptname':filename})
                    list_c.append({'loop_mod':self.loop_mod})
                    list_c.append({'loop_case':self.loop_case})
                    list_c.append({'loop_srcipt':self.loop_srcipt})
                    
                    step_key = 'Test_case' + str(self.step_num)
                    self.step_dic[step_key] = list_c
                    self.step_num = self.step_num  + 1
                    self.loop_srcipt = self.loop_srcipt + 1
                    #log_print(filename)
            else:
                break
            num = num + 1
                
    def find_path_excel(self,path='E:\\test_case_auto\\d\\t',excel_file='',sheetName = 'Sheet1'):
        cas_list = []
        if excel_file !='':
            cas_list.append(excel_file)
            cas_list.append(sheetName)
            return cas_list
        path_list = os.listdir(path)
        for x in path_list:
            if x.endswith('.xls')==True:
                excel_file = path + '\\' + x
                print '1111excel_file',excel_file
                cas_list.append(excel_file)
                cas_list.append(sheetName)
                break
        log_print(cas_list)
        return cas_list
        
    def dic_re(self,path='E:\\test_case_auto\\d\\t',excel_file='',sheetName = 'Sheet1'):
        case_list = self.find_path_excel(path,excel_file,sheetName)
        self.filename =case_list[0]
        self.sheetName = case_list[1]
        #log_print( '######### excel dic  start #########')
        self.Excel_read()
        #log_print( '######### excel dic end #########')
        self.mod_run()
        #log_print('********** dic testcase dic start **********')
        log_print(self.step_dic)
        #log_print('********** dic testcase dic end **********')
        return self.step_dic
        
if __name__ == "__main__":  
    filename = 'E:\\test_case_auto\\d\\t\\set_run.xls'
    testexcel = readcase_excel()
    testexcel.dic_re()