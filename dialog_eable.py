#-*- coding: UTF-8 -*- 
from public import *
if __name__ == "__main__":
    filename = 'E:\\test_case_auto\\ems.ini'
    keyword = 'result'
    param ='EMS-client_unstall'
    value = 'True'
    print replaceini(filename,keyword,param,value)



