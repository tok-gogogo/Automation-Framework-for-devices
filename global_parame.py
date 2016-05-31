#-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        udp_class.py
# Purpose:     
#
# Author:      gongke
#
# Created:     2013/01/15
# RCS-ID:      $Id: udp_class.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
import xlrd
import string
from public import * 
import types

class readexcel:
    
    def __init__(self,filename,sheetName):
        self.filename = filename
        self.sheetName = sheetName
        self.Dic_parame={}
        self.error = " "
        
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
    
    def Excel_read(self):
        obj_table = self.Excel_sheetName()
        if obj_table == 0 :
            msg = 'find the excel: ' +self.filename +' but not find sheet name:' + self.sheetName
            log_print(msg)
            self.error = msg
            return self.Dic_parame
        for row in range(obj_table.nrows):
            values =  []
            for  col in range(obj_table.ncols):
                values.append(obj_table.cell(row,col).value)
            #print ','.join(values)  
            key = values[0].strip()
            tmp_type='a'
            if(type(values[1]) == type(tmp_type)):
                self.Dic_parame[key] = values[1].strip()
            else:
                self.Dic_parame[key] = str(values[1]).strip()
                '''
                if (type(values[1]) == type(1.0)):
                    self.Dic_parame[key] = str(int(values[1])).strip()
                else:
                    self.Dic_parame[key] = str(values[1]).strip()
                '''
        return self.Dic_parame

if __name__ == "__main__":  
    #-----------------------------------------------------------------------------
    # Name:        instantiation of the ftp class
    # param:       
    # explain:     test the ftp class and fuction 
    # Author:      gongke
    #
    # Created:     2013/01/13
    #-----------------------------------------------------------------------------
    #testexcel = readexcel("E:\\Simu_server\\global\\global_param.xls",'global')
    testexcel = readexcel("E:\\Simu_server\\auto_conf\\stream_param.xls",'stream')
    
    print testexcel.Excel_read()