#-*- coding: UTF-8 -*- 
#import thread
import time
import threading
import Testcase_exec
import os
import sys
sys.coinit_flags = 0
import pythoncom
#import xlwt

class Thread_multiple(object):
    def __init__(self, func, args, name=''):
        self.name = name
        self.func = func
        self.args = args
        #self.testcasearg = testcasearg
        
    def __call__(self):
        print "the thread name:",self.name
        apply(self.func, self.args)
    
    def stop(self):
        self.thread_stop =True
        
def My_testcase(filepath,log ="log.text"):
    test_exec = Testcase_exec.exec_case()
    log_result = "E:\\Simu_server\\ac_test_result\\" + log
    test_exec.operate_exec(filepath,log_result)
    print "filepath :",filepath
    
def test_exec():
        flag_dic={'Y':1,'y':1,'N':0,'n':0}
        flag_loop = 0
        TestPath =raw_input("please input the Testcase Path:")
        while True:
            Flag_key = raw_input("Do you want the testcase loop,Y/N,y/n : ")
            if flag_dic.has_key(Flag_key):
                flag_loop = flag_dic[Flag_key]
                break
            print "you input wrong ,please input again"   
        listpath=os.listdir(TestPath)
        ac_case_path=[]
        threads = []
        path_threads = []
        for i in listpath:
            str_dir = TestPath +"\\" + i
            log = i+".log"
            if os.path.isdir(str_dir):
                testtuple=(str_dir,log)
                test_thread = threading.Thread(target=Thread_multiple(My_testcase,testtuple,TestPath))
                path_threads.append((testtuple,TestPath))
                threads.append(test_thread)
        while True:
            for i in range(len(threads)):
                #print ".............i=",i
                #print threads[i].isAlive()
                if threads[i].isAlive()==False:
                    del threads[i]
                    test_thread = threading.Thread(target=Thread_multiple(My_testcase,path_threads[i][0],path_threads[i][1]))
                    threads.insert(i,test_thread)
                    threads[i].start()
                time.sleep(5)
            if flag_loop == 0:
                break
            time.sleep(1)
            
        
'''
if __name__=='__main__':
    test_exec()
'''
        
        
        
    
        