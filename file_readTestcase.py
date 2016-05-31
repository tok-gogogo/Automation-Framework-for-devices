import re
import os
import sys
import Testcase_exec

class Testallcase:
    def __init__(self,path,logfile):
        self.TestcasePath = path
        self.casepathDic = {}
        
    def filetocasepathDic(self):
        listpath=os.listdir(self.TestcasePath)
        tmp = 1
        for i in listpath:
            filename = self.TestcasePath + i
            print filename
            key='case' + str(tmp)
            self.casepathDic[key]=filename
            tmp= tmp + 1
        print self.casepathDic
        return True
    
if __name__=='__main__':
    
    test_file = Testallcase("E:\\Simu_server\\test_case_dir","logfile")
    test_file.filetocasepathDic()
    
    """
    def do_testcase(self):
        tmp = 1
        while True:
            str_tmp='case'+ str(tmp)
            if casepathDic.has_key(str_tmp):
                test_exec = exec_case("E:\\Simu_server\\test_case.txt","log.text")
                test_exec.fileread()
                test_exec.exec_data()
                tmp = tmp + 1
            else:
                break
        return True
    """