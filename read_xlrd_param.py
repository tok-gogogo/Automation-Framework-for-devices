#-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        read_xlrd_param.py
# Purpose:     
#
# Author:      gongke
#
# Created:     2013/11/18
# RCS-ID:      $Id: read_xlrd_param.py $,use for read param
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
    
    