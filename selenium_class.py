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
KEY_IMG1 = u"img[alt=\"简约时尚 钢化玻璃 茶几 电视柜 套装 现代\"]"
KEY_IMG2 = u"img[alt=\"现代 钢化玻璃 茶几 储物茶桌 客厅茶几 电视柜 套装\"]"
KEY_IMG3 = u"img[alt=\"钢化玻璃 钢琴烤漆 黑白 简约 时尚 带抽屉茶几 电视柜套装\"]"
KEY_IMG4 = u"img[alt=\"现代 简约时尚 不锈钢 茶几 大理石 电视柜 套装\"]"
KEY_IMG5 = u"img[alt=\"现代 时尚 简约 白色烤漆 黑色钢化 玻璃 长方形 茶几 电视柜套装\"]"
KEY_IMG6 = u"img[alt=\"简约 现代 大理石 茶几 时尚 豪华大气 不锈钢 电视柜 组合套装\"]"
KEY_IMG7 = u"img[alt=\"旋转全烤漆 玻璃茶桌 简约时尚 圆形茶几 小户型 茶几!\"]"
KEY_IMG8 = u"img[alt=\"简约时尚 钢琴烤漆 镶钻 钢化玻璃 面白色 黑色 茶几 电视柜套装\"]"

KEY_PINJIA1 = u"评价详情(0)"
KEY_BABY1 = u"宝贝详情"
KEY_DIANPU = u"金瞬时尚家居进入店铺"

DO_LIST = [KEY_IMG1,KEY_IMG2,KEY_IMG3,KEY_IMG4,KEY_IMG5,KEY_IMG6,KEY_IMG7,KEY_IMG8]
WAITTIME = 1

def del_file_path(path='C:\\Documents and Settings\\dell\\Local Settings\\Temp',start ='tmp'):
    rootdir=path
    for f in os.listdir(rootdir):
        if f.startswith(start)==True:
            filepath = os.path.join( rootdir, f )
            if os.path.isfile(filepath):
                os.remove(filepath)
                print filepath+" removed!"
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath,True)
                print "dir "+filepath+" removed!"
def caozuo(driver,cur_w,tmp_list):
    
    cur = None
    list_w = driver.window_handles
    for x in list_w:
        if x not in tmp_list:
            cur = x 
            tmp_list.append(cur)
            
        if cur!=None:
            try:
                driver.switch_to_window(cur)
                time.sleep(WAITTIME)
                #driver.find_element_by_link_text(KEY_PINJIA1).click()
                driver.find_element_by_css_selector("em.J_ReviewsCount").click()
                time.sleep(WAITTIME)
                driver.find_element_by_link_text(KEY_BABY1).click()
                time.sleep(WAITTIME)
                js="var q=document.documentElement.scrollTop=10000"
                driver.execute_script(js)
                time.sleep(WAITTIME)
                driver.close()
                driver.switch_to_window(cur_w)
                time.sleep(WAITTIME)
            except Exception,e:
                print 'except',e
                pass
    return tmp_list
        
base_url = "http://langman123.taobao.com/"
try:
    tmpdate = urllib.urlopen(base_url).info()
    WEB_CODE_GET = tmpdate.getparam('charset')
except Exception,e:
    print 'except',e
    pass
#print tmpdate
num = 0 
while True:
    num = num +1
    print 'Run ',num,'  times' 
    driver = webdriver.Firefox()
    
    try:
        driver.delete_all_cookies()
    except Exception,e:
        print 'except',e
        pass
    
    try:
        driver.get(base_url)
        js="var q=document.documentElement.scrollTop=1000"
        driver.execute_script(js)
        cur_win = driver.current_window_handle
        random.shuffle(DO_LIST)
        time.sleep(10)
        for y in DO_LIST:
            driver.find_element_by_css_selector(y).click()
            tmp_list =[]
            tmp_list = caozuo(driver,cur_win,tmp_list)
    except Exception,e:
        print 'except',e
        pass
    '''
    driver.find_element_by_css_selector(KEY_IMG1).click()
    time.sleep(5)
    list_w = driver.window_handles
    print 'op IMG1,LIST_W:',list_w
    tmp_list = []
    tmp_list.append(cur_win)
    cur_t= None
    for handle in list_w:
        if handle not in tmp_list:
            cur_t = handle
            tmp_list.append(handle)
            break
    if cur_t!=None:
        driver.switch_to_window(cur_t)
        time.sleep(1)
        time.sleep(2)
        driver.find_element_by_link_text(KEY_PINJIA1).click()
        time.sleep(1)
        driver.find_element_by_link_text(KEY_BABY1).click()
        time.sleep(1)
    
        js="var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
        time.sleep(5)
        driver.switch_to_window(cur_win)
    driver.find_element_by_css_selector(KEY_IMG2).click()
    list_w = driver.window_handles
    print 'op IMG2,LIST_W:',list_w
    time.sleep(3)
    cur_t= None
    for handle in list_w:
        if handle not in tmp_list:
            cur_t = handle
            tmp_list.append(handle)
            break
    if cur_t!=None:
        driver.switch_to_window(cur_t)
        time.sleep(1)
        driver.find_element_by_link_text(KEY_PINJIA1).click()
        time.sleep(1)
        driver.find_element_by_link_text(KEY_BABY1).click()
        time.sleep(5)
        js="var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
    '''
    try:
        driver.delete_all_cookies()
        driver.close()
        os.popen('taskkill /F /im  firefox.exe').read()
        del_file_path()
    except Exception,e:
        print 'except',e
        pass
    time.sleep(20)
    
    #print os.popen('ipconfig /renew').read()
    #time.sleep(50)

#dialog = browser.switch_to_alert()
#dialog.accept()

'''
login_username='admin'
login_password ='admin'

now_handle = browser.current_window_handle
hwnd = win32gui.FindWindow('#32770',None)
if hwnd < 1:
    print 'not find login windows'
else:
    win32api.Sleep(100)
    win32api.keybd_event(18,0,0,0);
    win32api.keybd_event(85,0,0,0);
    win32api.Sleep(100)
    win32api.keybd_event(85,0,win32con.KEYEVENTF_KEYUP,0);
    win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
    win32api.Sleep(100)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys(login_username)
            
    win32api.Sleep(100)
    win32api.keybd_event(18,0,0,0);
    win32api.keybd_event(80,0,0,0);
    win32api.Sleep(100)
    win32api.keybd_event(80,0,win32con.KEYEVENTF_KEYUP,0);
    win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0);
    win32api.Sleep(300)
    shell.SendKeys(login_password)
    win32api.Sleep(100)
    win32api.keybd_event(13,0,0,0);   
    win32api.Sleep(100)
    win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0);
    win32api.Sleep(100)
#browser.switch_to_window(now_handle)
time.sleep(10)
browser.get("http://192.168.22.130/index.html")
'''
'''
clas_menu = browser.find_element_by_class_name('menulist6')
clas_menu.click()
print clas_menu.get_attribute('href')
clas_menu.click()
'''
'''
class selenium_mine():
    def __init__(self,host='192.168.22.169',port=4444,commandexcel='*firefox',browserURL='http://langman123.taobao.com'):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = browserURL
        self.verificationErrors = []
        self.accept_next_alert = True

'''


