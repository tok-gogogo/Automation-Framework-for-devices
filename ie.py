#-*- coding: UTF-8 -*-  
from selenium import webdriver
import time
import win32gui
import winGuiAuto
import win32con
import win32api
import win32ui
from win_GUI import * 
from pywinauto import *

win_title = "来自网页的消息"
button_name ="确定"
driver = webdriver.Ie()
tes_eoc  =  "http://192.168.22.170/vlan/vlan_parmSet.asp"
driver.get(tes_eoc )
driver.find_element_by_id("MagVlanId").clear()
driver.find_element_by_id("MagVlanId").send_keys("14")
driver.find_element_by_id("Button1").click()

time.sleep(10)
hwnds = findwindows.find_windows(class_name_re = "#32770")

print 'hwnd:',findwindows.find_windows(class_name_re = "#32770")
buttons =[]

for hwnd in hwnds:
    buttons = winGuiAuto.findControls(hwnd,
                    wantedClass="Button",
                    wantedText=button_name)
    print 'buttons:',buttons
    if len(buttons)>0:
        break
for x in buttons:
    winGuiAuto.clickButton(x)


#driver.execute_script('vlan_buildnew()')
time.sleep(1)
driver.find_element_by_name("b1").click()
driver.find_element_by_id("vlan_id").clear()
driver.find_element_by_id("vlan_id").send_keys("12")
driver.find_element_by_xpath("//button[@type='button']").click()






