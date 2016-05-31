#-*- coding: UTF-8 -*-  
import os
import sys
import string

class checkscript:
    
    def __init__():
        self.fucdic ={}
        self.dic ={}
    
    def readfile(self,file):
        file_object = open(self.datafile,"r")
        textlist = file_object.readlines()
        file_object.close()
        
    def GetFucDic():
        file_object = open(self.datafile,"r")
        textlist = file_object.readlines()
        file_object.close()
        str_note_section = '****'
        str_note = '×¢ÊÍ'
        str_note_flag = False
        
        for line in textlist:
            if str_note_flag in line:
                if str_note_flag == False:
                     str_note_flag = True
                else:
                    str_note_flag =False
                continue
            if str_note_flag ==True:
                continue
            if len(line.split())==0:
                continue
            if str_note in line :
                continue
                