#-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        script_generator
# Purpose:     
#
# Author:      gongke
#
# Created:     2014/01/12
# RCS-ID:      
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
import xlrd
import string
from public import * 
import types,os,sys

class script_generator():
    def __init__(self,filename = 'E:\\test_case_auto\\d\\jiaoben.xls'):
        self.filename = filename
        self.path = os.path.dirname(self.filename)

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
            return None
        else:
            list_excel =[]
            list_excel.append(obj_book)
            list_excel.append(obj_book.sheet_names())
            return list_excel
    
    def generator(self,obj_table,sheetname):
        dic ={"#ftp":0,"#telnet":1,"#udp":2,"#cmd":3,"#loadrunner":4,"#sleep_p":5,"#sleep":5,"#ACWeb":6,
              "#Serial":7,"#Compare":8,'#winGUI':9,'#file_replay':10,'#rssid':11,'#sendemail':16,'#thread':12,
              '#waveQoE':13,'#omnipeek':14,'#waveApps':15,'#tar_cmp':16,'#TestCenter':17}
        tmpfile= self.path + '\\' + sheetname + '.txt'
        if file_exist(tmpfile):
            os.remove(tmpfile)
        file_ob_bacup = open(tmpfile,'a')
        for row in range(obj_table.nrows):
            str_v =''
            tmp_num = 0
            cmd_flag = False
            for  col in range(obj_table.ncols):
                tmp_str = obj_table.cell(row,col).value
                tmp_str = tmp_str.strip()
                if dic.has_key(tmp_str)==True or tmp_str.find('***')>-1:
                    str_v = tmp_str 
                else:
                    if tmp_str.endswith('$')==True:
                        str_v = str_v + '            ' + tmp_str
                        
                    else:
                        if tmp_num==0:
                            str_v = str_v + '      ' + tmp_str +'      '
                            tmp_num = tmp_num + 1 
                        elif len(tmp_str)==0:
                            continue
                        elif tmp_num ==1:
                            str_v = str_v  +'      '+ tmp_str + '      '
                            tmp_num = tmp_num +1
                        else:
                            str_v = str_v +',' + tmp_str + '      '
                    
            log_print(str_v)
            '''
            if str_v.find('\n')>-1:
                str_v = str_v.strip()
                for y in str_v.split('\n'):
                    y = '           ' + y
                    file_ob_bacup.writelines(y)
            else:    
                file_ob_bacup.writelines(str_v)
            '''
            file_ob_bacup.writelines(str_v)
            file_ob_bacup.writelines('\r\n')
        file_ob_bacup.close()
            
    def Excel_read(self):
        sheet_names = self.Excel_sheetName()[1]
        obj_book = self.Excel_sheetName()[0]
        print sheet_names
        if sheet_names==None:
            return 
        else:
            for sheetname in sheet_names:
                obj_table = obj_book.sheet_by_name(sheetname)
                self.generator(obj_table,sheetname)

if __name__ == "__main__":  
    param_cin = len(sys.argv)
    filename = 'E:\\test_case_auto\\d\\jiaoben.xls'
    if param_cin ==1:
        while 1:
            filename =raw_input("please input the script excel absolute file:")
            if filename.endswith('.xls')==True:
                break
    testexcel = script_generator(filename )
    testexcel.Excel_read()