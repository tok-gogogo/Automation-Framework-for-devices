# -*- coding: gb18030 -*- 
#-----------------------------------------------------------------------------
# Name:        xlrt.py
# Purpose:     
# Created:     2013/12/21
# RCS-ID:      $Id: SNMP_OPER.py $,USE FOR snmp operation
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
import shutil
import os
import string

def cp_file(path1,num=200):
    
    for root,dir,files in os.walk(path1,False):
        for name in files:
            for x in range(1,5):
                new_file = os.path.join(root,name).split('.txt')[0] + str(x) + '.txt'
                shutil.copyfile(os.path.join(root,name),new_file)
                
    
    for root,dir,files in os.walk(path1,False):
        for name in dir:
            if name.find('Case')>-1:
                for x in range(1,4):
                    new_file = os.path.join(root,name) + str(x)
                    shutil.copytree(os.path.join(root,name),new_file)
    
    
    for root,dir,files in os.walk(path1,False):
        for name in dir:
            if name.find('Module')>-1:
                for x in range(1,num):
                    new_file = os.path.join(root,name) + str(x)
                    shutil.copytree(os.path.join(root,name),new_file)


if __name__ == "__main__":
    cp_file('E:\\debug\\test')
                    


        
    