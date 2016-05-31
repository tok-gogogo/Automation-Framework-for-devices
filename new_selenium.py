#-*- coding: gbk -*- 
from selenium import webdriver
from selenium import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import win32com.client
import unittest, time, re,random
import urllib
import chardet
from public import *
import shutil
from pywinauto import *
import win32com.client
from win_GUI import *
import win32gui
import win32api
import win32con

KEY_BABY = u"宝贝详情"
BABY_TOTAL = 6

class taobao():
    def __init__(self,url="http://langman123.taobao.com/"):
        self.base_url = url
        self.accept_next_alert = True
        
        
    def find_winhwd(self):
        for x in self.driver.window_handles:
            if x not in self.tmp_list:
                self.tmp_list.append(x)
                return x
        return 0
        
    def caozuo(self,driver,randnum):
        xpath_value =''
        try:
            #xpath_value ="//div[@id='shop5765730788']/div/div[2]/div[" + randnum + "]/div/div/div/a"
            xpath_value ="//div[@class='bb_list']["+randnum+"]/div/a"
            print 'xpath_value:',xpath_value
            driver.find_element_by_xpath(xpath_value).click()
        except Exception,e:
            print 'except:',e
            return False
        try:
            cur = self.find_winhwd()
            if cur ==0:
                return False
            driver.switch_to_window(cur)
            child = "//a[@class='tb-tab-anchor']"
            for x in driver.find_elements_by_xpath(child):
                x.click()
                time.sleep(1)
            js="var q=document.documentElement.scrollTop=10000"
            driver.execute_script(js)
            time.sleep(10)
            driver.close()
        except Exception,e:
            print 'except:',e
            pass
            return False
            
    def tmp_list_num(self,rang_len =6):
        self.tmp_list_n =[]
        for x in range(1,rang_len):
            self.tmp_list_n.append(x)
        random.shuffle(self.tmp_list_n)
        return self.tmp_list_n
            
    def op_web(self,total=4):
        run_total = 0
        while True:
            run_total = run_total + 1
            print 'run_total:',run_total
            app_f = findwindows.find_windows(class_name_re = "MainForm")
            print 'app_f:',app_f
            self.driver = webdriver.Firefox()
            try:
                for hwnd in app_f:
                    win32gui.MoveWindow(hwnd,0,0,1228,664,1)
                    win32gui.MoveWindow(hwnd,20,20,1248,684,1)
                    win32gui.SetWindowPos(hwnd,win32con.HWND_TOP,0,0,1228,664,win32con.HWND_TOP|win32con.SWP_SHOWWINDOW)
                    break
                self.driver.delete_all_cookies()
                self.driver.get(self.base_url)
                
                
                time.sleep(20)
                js="var q=document.documentElement.scrollTop=1500"
                self.driver.execute_script(js)
                self.main_win = self.driver.current_window_handle
                
                self.tmp_list=[]
                num_l = self.tmp_list_num(BABY_TOTAL)
                random.shuffle(num_l)
                self.tmp_list.append(self.main_win)
                tmpnum = 0
                while True:
                    num = random.randrange(0,len(num_l)-1)
                    tmpnum = num_l[num]
                    del num_l[num]
                    print 'num:',num ,'  tmpnum:',tmpnum
                    self.caozuo(self.driver,str(tmpnum))
                    self.driver.switch_to_window(self.main_win)
                    tmpnum = tmpnum +1
                    if tmpnum >total:
                        break
                self.driver.quit()
                
            except Exception,e:
                print 'except:',e
                time.sleep(60)
                self.driver.quit()
                pass
            time.sleep(20)
if __name__ == "__main__":
    test = taobao()
    test.op_web()
        
        
        