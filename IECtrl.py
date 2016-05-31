# -*- coding: UTF-8 -*-
import win32com
from PAM30 import PAMIE
import time
import winGuiAuto #popup window


"""
hwnd = winGuiAuto.findTopWindows("Windows Internet Explorer")
control_list=winGuiAuto.dumpWindow(hwnd[0])
for control_item in control_list:
    if control_item[1]='OK':
        winGuiAuto.clickButton(control_item[0])
"""
ret = False

ie = PAMIE()

#Open login page of AC
ret = ie.navigate('https://192.168.4.232')
if ret == False:
    ie.quit()
#ie.navigate('http://www.baidu.com')

#skip auth page
ie.clickLink('overridelink')
time.sleep(1)

#login AC

ie.setTextBox('UserName', 'icac')#set user name
ie.setTextBox('PassWord', 'icaclogin')#set user name

ie.clickButton('LoginChinese')
time.sleep(1)

#ret = ie.navigate('https://192.168.21.200/wlan/wlan_cfg_edit.php')

#Click WLAN menu
#print ie.clickMenu( 'a','Selector.php?MenuID=309', 'WLAN', event=None)
#print ie.clickElement( 'WLAN' )

#print ie.executeJavaScript('javascript:modify_Language(1)')

#btn = findElement('button', 'id', 'login_submit_btn')
#ie.clickElement(btn)
#ie.navigate('https://192.168.4.232/Selector.php?MenuID=306&MenuName=WLAN')
Page1 ='https://192.168.4.232/main.php'
Page2 ='https://192.168.4.232/Welcome.php'
Page3 ='https://192.168.4.232/Selector.php?MenuID=305&MenuName=无线安全'
Page4 = 'https://192.168.4.232/Welcome.php'
Page5 ='https://192.168.4.232/wlan/wlan_security_cfg_list.php'
Page6='https://192.168.4.232/wlan/wlan_security_cfg_edit.php?flag=insert&SecurityMode=please'

Page7= 'https://192.168.4.232/baseconf/ac_config.php'#AC配置
Page8='https://192.168.4.232/hotstandby/hotstandby_cfg.php'#AC热备配置

"""
ie.navigate(Page1)
time.sleep(1)
ie.navigate(Page2)
time.sleep(1)
ie.navigate(Page3)
time.sleep(1)
ie.navigate(Page4)
time.sleep(1)
ie.navigate(Page5)
"""
"""
time.sleep(1)
ie.navigate(Page6)
time.sleep(1)
ie.navigate(Page7)
"""

time.sleep(1)
ie.navigate(Page7)
#print ie.getListBox('Switch')
time.sleep(2)
 
#print ie.listBoxUnSelect('LoadBalance','2')
#time.sleep(2)
ie.selectListBox('LoadBalance', "1")
time.sleep(2)

print "pass"



"""
ie.setTextBox('PolicyID', '1')
time.sleep(1)
ie.setTextBox('SecurityName', 'wep1')
time.sleep(1)
print ie.getListBox('SecurityMode')

print ie.selectListBox('SecurityMode', '2',0)
time.sleep(1)
ie.listBoxUnSelect('KeyLength', '0')
time.sleep(1)
ie.listBoxUnSelect('KeyType', '0')
time.sleep(1)
ie.listBoxUnSelect('Encrypt', '0')
time.sleep(1)
ie.listBoxUnSelect('KeyIndex', '1')
time.sleep(1)
ie.setTextBox('Key1', '12345')
time.sleep(1)

ie.clickButton('save')
time.sleep(1)
"""

"""
Page1 ='https://192.168.4.232/Menu.php'
Page1 ='https://192.168.4.232/wlan/wlan_security_cfg_list.php'
Page1 ='https://192.168.4.232/wlan/wlan_security_cfg_edit.php?flag=insert&SecurityMode=please'
Page1 ='https://192.168.4.232/main.php'
Page1 ='https://192.168.4.232/main.php'
"""




#ie.quit()
#ie.clickButton('WLAN')
#write name
#name ='tj_setting'
#print ie.getTextBox(name)
#ie.buttonClick("Submit")
#ie.SetTextBox('John','text')
#print ie.getTextArea('wd')
#ie.clickButton("Submit")
#ie.Quit()