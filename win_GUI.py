#-*- coding: UTF-8 -*-  
import array
import ctypes
import struct

import win32api
import win32con
import win32gui
import win32ui
import os
import sys
import win32process
import win32con
#import win32api
import string
from ctypes import *
import pprint
import random

import time
from win_exec import *
from public import * 
#import commctrl
import types
import pyhk
#import re
import sys
sys.setdefaultencoding("utf-8") 
from pywinauto import *
#import pywinauto

KEY_TIME_FORMAT = "%Y%m%d_%H%M%S"

MAIN_HWND = 0

global_wind_list = [] 

global_all_list = []

def lst_add_all(list =[]):
    for x in list:
        if isinstance(x,type(list)):
            lst_add_all(x)
        else:
            global_all_list.append(x)
    return global_all_list

def hwd_get_pos(list,tuple):
    for x in list:
        if isinstance(x,(int)):
            print 'hwd:', x,' pos: ', win32gui.GetWindowRect(x)
            if win32gui.GetWindowRect(x) ==tuple:
                return x    
    return 0
 
        
def findTopWindow(wantedText=None, wantedClass=None, selectionFunction=None):
    '''Find the hwnd of a top level window.
    You can identify windows using captions, classes, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    wantedText          Text which the required window's captions must contain.
    wantedClass         Class to which the required window must belong.
    selectionFunction   Window selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of a desired window.
                    
    Raises:
    WinGuiAutoError     When no window found.

    Usage example:      optDialog = findTopWindow(wantedText="Options")
    '''
    topWindows = findTopWindows(wantedText, wantedClass, selectionFunction)
    if topWindows:
        
        return topWindows[0]
    else:
        raise WinGuiAutoError("No top level window found for wantedText=" +
                               repr(wantedText) +
                               ", wantedClass=" +
                               repr(wantedClass) +
                               ", selectionFunction=" +
                               repr(selectionFunction))

def findTopWindows(wantedText=None, wantedClass=None, selectionFunction=None):
    '''Find the hwnd of top level windows.
    You can identify windows using captions, classes, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    wantedText          Text which required windows' captions must contain.
    wantedClass         Class to which required windows must belong.
    selectionFunction   Window selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of a desired window.

    Returns:            A list containing the window handles of all top level
                        windows matching the supplied selection criteria.

    Usage example:      optDialogs = findTopWindows(wantedText="Options")
    '''
    results = []
    topWindows = []
    win32gui.EnumWindows(_windowEnumerationHandler, topWindows)
    for hwnd, windowText, windowClass in topWindows:
        if wantedText and not _normaliseText(wantedText) in _normaliseText(windowText):
            continue
        if wantedClass and not windowClass == wantedClass:
            continue
        if selectionFunction and not selectionFunction(hwnd):
            continue
        results.append(hwnd)
    return results

def dumpWindow_pos(hwnd):
    '''Dump all controls from a window into a nested list
    Useful during development, allowing to you discover the structure of the
    contents of a window, showing the text and class of all contained controls.

    Arguments:      The window handle of the top level window to dump.

    Returns         A nested list of controls. Each entry consists of the
                    control's hwnd, its text, its class, and its sub-controls,
                    if any.

    Usage example:  replaceDialog = findTopWindow(wantedText='Replace')
                    pprint.pprint(dumpWindow(replaceDialog))
    '''
    windows = []
    try:
        win32gui.EnumChildWindows(hwnd, _windowEnumerationHandler, windows)
    except win32gui.error:
        # No child windows
        return
    windows = [list(window) for window in windows]
    for window in windows:
        childHwnd, windowText, windowClass = window
        window_content = dumpWindow(childHwnd)
        if window_content:
            window.append(window_content)
            print '###################'
            print childHwnd,'pos:',win32gui.GetWindowRect(childHwnd),'window_content:',window_content
            tuple_t = win32gui.GetWindowRect(childHwnd)
            if tuple_t[0]==179 and tuple_t[2]==561:
                print window_content[0][0],'pos:',win32gui.GetWindowRect(window_content[0][0])
                if window_content[0][0]:
                    bufLen=1024
                    buf =win32gui.PyMakeBuffer(bufLen)
                    n = win32gui.SendMessage(window_content[0][0],win32con.WM_GETTEXT,bufLen,buf)
                    str = buf[:n]
                    print str
                    print getEditText(window_content[0][0])
                    time.sleep(1)
                    #win32gui.SendMessage(window_content[0][0],win32con.WM_SETTEXT,None,'Realtek 10/100/1000 Ethernet NIC')
            print '###################'
    return windows


def dumpWindow(hwnd):
    '''Dump all controls from a window into a nested list
    Useful during development, allowing to you discover the structure of the
    contents of a window, showing the text and class of all contained controls.

    Arguments:      The window handle of the top level window to dump.

    Returns         A nested list of controls. Each entry consists of the
                    control's hwnd, its text, its class, and its sub-controls,
                    if any.

    Usage example:  replaceDialog = findTopWindow(wantedText='Replace')
                    pprint.pprint(dumpWindow(replaceDialog))
    '''
    windows = []
    try:
        win32gui.EnumChildWindows(hwnd, _windowEnumerationHandler, windows)
    except win32gui.error:
        # No child windows
        return
    windows = [list(window) for window in windows]
    for window in windows:
        childHwnd, windowText, windowClass = window
        window_content = dumpWindow(childHwnd)
        if window_content:
            window.append(window_content)
    return windows

def findControl(topHwnd,
                wantedText=None,
                wantedClass=None,
                selectionFunction=None):
    '''Find a control.
    You can identify a control using caption, classe, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    topHwnd             The window handle of the top level window in which the
                        required controls reside.
    wantedText          Text which the required control's captions must contain.
    wantedClass         Class to which the required control must belong.
    selectionFunction   Control selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of the desired control.

    Returns:            The window handle of the first control matching the
                        supplied selection criteria.
                    
    Raises:
    WinGuiAutoError     When no control found.

    Usage example:      optDialog = findTopWindow(wantedText="Options")
                        okButton = findControl(optDialog,
                                               wantedClass="Button",
                                               wantedText="OK")
                        '''
    controls = findControls(topHwnd,
                            wantedText=wantedText,
                            wantedClass=wantedClass,
                            selectionFunction=selectionFunction)
    if controls:
        #print controls
        return controls[0]
    else:
        raise WinGuiAutoError("No control found for topHwnd=" +
                               repr(topHwnd) +
                               ", wantedText=" +
                               repr(wantedText) +
                               ", wantedClass=" +
                               repr(wantedClass) +
                               ", selectionFunction=" +
                               repr(selectionFunction))

def findControls(topHwnd,
                 wantedText=None,
                 wantedClass=None,
                 selectionFunction=None):
    '''Find controls.
    You can identify controls using captions, classes, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    topHwnd             The window handle of the top level window in which the
                        required controls reside.
    wantedText          Text which the required controls' captions must contain.
    wantedClass         Class to which the required controls must belong.
    selectionFunction   Control selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of a desired control.

    Returns:            The window handles of the controls matching the
                        supplied selection criteria.    

    Usage example:      optDialog = findTopWindow(wantedText="Options")
                        def findButtons(hwnd, windowText, windowClass):
                            return windowClass == "Button"
                        buttons = findControl(optDialog, wantedText="Button")
                        '''
    def searchChildWindows(currentHwnd):
        results = []
        childWindows = []
        try:
            win32gui.EnumChildWindows(currentHwnd,
                                      _windowEnumerationHandler,
                                      childWindows)
        except win32gui.error:
            # This seems to mean that the control *cannot* have child windows,
            # i.e. not a container.
            return
        for childHwnd, windowText, windowClass in childWindows:
            descendentMatchingHwnds = searchChildWindows(childHwnd)
            if descendentMatchingHwnds:
                results += descendentMatchingHwnds

            if wantedText and \
               not _normaliseText(wantedText) in _normaliseText(windowText):
                continue
            if wantedClass and \
               not windowClass == wantedClass:
                continue
            if selectionFunction and \
               not selectionFunction(childHwnd):
                continue
            results.append(childHwnd)
        return results
        
    return searchChildWindows(topHwnd)

def getTopMenu(hWnd):
    '''Get a window's main, top level menu.
    
    Arguments:
    hWnd            The window handle of the top level window for which the top
                    level menu is required.

    Returns:        The menu handle of the window's main, top level menu.

    Usage example:  hMenu = getTopMenu(hWnd)'''
    
    
    return ctypes.windll.user32.GetMenu(ctypes.c_long(hWnd))

def activateMenuItem(hWnd, menuItemPath):
    '''Activate a menu item
    
    Arguments:
    hWnd                The window handle of the top level window whose menu you 
                        wish to activate.
    menuItemPath        The path to the required menu item. This should be a
                        sequence specifying the path through the menu to the
                        required item. Each item in this path can be specified
                        either as an index, or as a menu name.
                    
    Raises:
    WinGuiAutoError     When the requested menu option isn't found.

    Usage example:      activateMenuItem(notepadWindow, ('file', 'open'))
    
                        Which is exactly equivalent to...
                    
                        activateMenuItem(notepadWindow, (0, 1))'''
    # By Axel Kowald (kowald@molgen.mpg.de)
    # Modified by S Brunning to accept strings in addition to indicies.

    # Top level menu    
    hMenu = getTopMenu(hWnd)
    
    #print 'activateMenuItem',hMenu
    #print '******menucount:',win32gui.GetMenuItemCount(hMenu)
    # Get top level menu's item count. Is there a better way to do this?
    
    #print 'wndtext:',win32gui.GetWindowText(hWnd)
    #print 'hmenu:',hMenu
    #print 'hmenu count',win32gui.GetMenuItemCount(hMenu)
    
    for hMenuItemCount in xrange(256):
        print 'activateMenuItem_hMenuItemCount:',hMenuItemCount
        try:
            getMenuInfo(hMenu, hMenuItemCount)
        except WinGuiAutoError:
            break
    hMenuItemCount -= 1
    
    # Walk down submenus
    for submenu in menuItemPath[:-1]:
        print 'submenu',submenu
        try: # submenu is an index
            0 + submenu
            submenuInfo = getMenuInfo(hMenu, submenu)
            hMenu, hMenuItemCount = submenuInfo.submenu, submenuInfo.itemCount
        except TypeError: # Hopefully, submenu is a menu name
            try:
                dump, hMenu, hMenuItemCount = _findNamedSubmenu(hMenu,
                                                                hMenuItemCount,
                                                                    submenu)
                
            except WinGuiAutoError:
                print 'menuItemPath1:',menuItemPath
                raise WinGuiAutoError("Menu path " +
                                      repr(menuItemPath) +
                                      " cannot be found.")
           
    # Get required menu item's ID. (the one at the end).
    menuItem = menuItemPath[-1]
    try: # menuItem is an index
        0 + menuItem
        menuItemID = ctypes.windll.user32.GetMenuItemID(hMenu,
                                                        menuItem)
    except TypeError: # Hopefully, menuItem is a menu name
        try:
            subMenuIndex, dump, dump = _findNamedSubmenu(hMenu,
                                        hMenuItemCount,
                                        menuItem)
        except WinGuiAutoError:
            #print 'menuItemPath2:',menuItemPath
            raise WinGuiAutoError("Menu path " +
                                  repr(menuItemPath) +
                                  " cannot be found.")
        # TODO - catch WinGuiAutoError. and pass on with better info.
        menuItemID = ctypes.windll.user32.GetMenuItemID(hMenu, subMenuIndex)

    # Activate    
    win32gui.PostMessage(hWnd, win32con.WM_COMMAND, menuItemID, 0)
    

def getMenuInfo(hMenu, uIDItem):
    #print "getMenuInfo fuction,hMenu,uIDItem",hMenu,uIDItem
    '''Get various info about a menu item.
    
    Arguments:
    hMenu               The menu in which the item is to be found.
    uIDItem             The item's index

    Returns:            Menu item information object. This object is basically
                        a 'bunch'
                        (see http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52308).
                        It will have useful attributes: name, itemCount,
                        submenu, isChecked, isDisabled, isGreyed, and
                        isSeperator
                    
    Raises:
    WinGuiAutoError     When the requested menu option isn't found.       

    Usage example:      submenuInfo = getMenuInfo(hMenu, submenu)
                        hMenu, hMenuItemCount = submenuInfo.submenu, submenuInfo.itemCount'''
    # An object to hold the menu info
    class MenuInfo(Bunch):
        pass
    menuInfo = MenuInfo()

    # Menu state    
    menuState = ctypes.windll.user32.GetMenuState(hMenu,
                                                  uIDItem,
                                                  win32con.MF_BYPOSITION)
                                                  
    
    #print "menuState_MF_BYPOSITION:",ctypes.windll.user32.GetMenuState(hMenu,uIDItem,win32con.MF_BYPOSITION)
    #print "menuState_MF_BYCOMMAND:",ctypes.windll.user32.GetMenuState(hMenu,uIDItem,win32con.MF_BYCOMMAND)
    if menuState == -1:
        raise WinGuiAutoError("No such menu item, hMenu=" +
                               str(hMenu) +
                               " uIDItem=" +
                               str(uIDItem))
    menuInfo.isChecked = bool(menuState & win32con.MF_CHECKED)
    menuInfo.isDisabled = bool(menuState & win32con.MF_DISABLED)
    menuInfo.isGreyed = bool(menuState & win32con.MF_GRAYED)
    menuInfo.isSeperator = bool(menuState & win32con.MF_SEPARATOR)
    # ... there are more, but these are the ones I'm interested in
    
    # Menu name
    menuName = ctypes.c_buffer("\000" * 32)
    ctypes.windll.user32.GetMenuStringA(ctypes.c_int(hMenu),
                                        ctypes.c_int(uIDItem),
                                        menuName, ctypes.c_int(len(menuName)),
                                        win32con.MF_BYPOSITION)
    menuInfo.name = menuName.value

    # Sub menu info
    menuInfo.itemCount = menuState >> 8
    if bool(menuState & win32con.MF_POPUP):
        menuInfo.submenu = ctypes.windll.user32.GetSubMenu(hMenu, uIDItem)
    else:
        menuInfo.submenu = None
    
    #print "menuInfo",menuInfo
    return menuInfo



def clickButton_Post(hwnd):
    _postNotifyMessage(hwnd, win32con.BN_CLICKED)
    
def clickButton(hwnd):
    '''Simulates a single mouse click on a button

    Arguments:
    hwnd    Window handle of the required button.

    Usage example:  okButton = findControl(fontDialog,
                                           wantedClass="Button",
                                           wantedText="OK")
                    clickButton(okButton)
    '''
    _sendNotifyMessage(hwnd, win32con.BN_CLICKED)


def  closeDialog(hwnd):
    win32gui.SendMessage(hwnd,win32con.WM_CLOSE,0,0)
    
def clickStatic(hwnd):
    '''Simulates a single mouse click on a static

    Arguments:
    hwnd    Window handle of the required static.

    Usage example:  TODO
    '''
    _sendNotifyMessage(hwnd, win32con.STN_CLICKED)

def doubleClickStatic(hwnd):
    '''Simulates a double mouse click on a static

    Arguments:
    hwnd    Window handle of the required static.

    Usage example:  TODO
    '''
    _sendNotifyMessage(hwnd, win32con.STN_DBLCLK)

def getComboboxItems(hwnd):
    '''Returns the items in a combo box control.

    Arguments:
    hwnd            Window handle for the combo box.

    Returns:        Combo box items.

    Usage example:  fontCombo = findControl(fontDialog, wantedClass="ComboBox")
                    fontComboItems = getComboboxItems(fontCombo)
    '''
    
    return _getMultipleWindowValues(hwnd,
                                     getCountMessage=win32con.CB_GETCOUNT,
                                     getValueMessage=win32con.CB_GETLBTEXT)

def selectComboboxItemThird(hwnd, item):
    try: # item is an index Use this to select
        0 + item
        win32gui.SendMessage(hwnd, win32con.CB_SHOWDROPDOWN, 1, 0)
        win32gui.SendMessage(hwnd, win32con.CB_SETCURSEL, item, 0)
        win32gui.SendMessage(hwnd, win32con.WM_SETFOCUS, 0, 0 )
        time.sleep(1)
        tmp=win32gui.GetWindowRect(hwnd)
        #print 'selectComboboxItemThird',tmp
        '''
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tmp[0]+1, tmp[1]+1) 
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tmp[0]+1, tmp[1]+1)
        '''
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, 13, 0 )
        time.sleep(0.1)
        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, 13, 0 )
        time.sleep(0.1)
        #_sendNotifyMessage(hwnd, win32con.CBN_SELCHANGE)
    except TypeError: # Item is a string - find the index, and use that
       
        items = getComboboxItems(hwnd)
        itemIndex = items.index(item)
        selectComboboxItem(hwnd, itemIndex)
        
def selectComboboxItem(hwnd, item):
    '''Selects a specified item in a Combo box control.

    Arguments:
    hwnd            Window handle of the required combo box.
    item            The reqired item. Either an index, of the text of the
                    required item.

    Usage example:  fontComboItems = getComboboxItems(fontCombo)
                    selectComboboxItem(fontCombo,
                                       random.choice(fontComboItems))
    '''
    try: # item is an index Use this to select
        0 + item
        win32gui.SendMessage(hwnd, win32con.CB_SETCURSEL, item, 0)
        #time.sleep(1)
        _sendNotifyMessage(hwnd, win32con.CBN_SELCHANGE)
    except TypeError: # Item is a string - find the index, and use that
        items = getComboboxItems(hwnd)
        itemIndex = items.index(item)
        selectComboboxItem(hwnd, itemIndex)

def getListboxItems(hwnd):
    '''Returns the items in a list box control.

    Arguments:
    hwnd            Window handle for the list box.

    Returns:        List box items.

    Usage example:  TODO
    '''
    
    return _getMultipleWindowValues(hwnd,
                                     getCountMessage=win32con.LB_GETCOUNT,
                                     getValueMessage=win32con.LB_GETTEXT)

def selectListboxItem(hwnd, item):
    '''Selects a specified item in a list box control.

    Arguments:
    hwnd            Window handle of the required list box.
    item            The reqired item. Either an index, of the text of the
                    required item.

    Usage example:  TODO
    '''
    try: # item is an index Use this to select
        0 + item
        win32gui.SendMessage(hwnd, win32con.LB_SETCURSEL, item, 0)
        _sendNotifyMessage(hwnd, win32con.LBN_SELCHANGE)
    except TypeError: # Item is a string - find the index, and use that
        items = getListboxItems(hwnd)
        itemIndex = items.index(item)
        selectListboxItem(hwnd, itemIndex)
                                    
def getEditText(hwnd):
    '''Returns the text in an edit control.

    Arguments:
    hwnd            Window handle for the edit control.

    Returns         Edit control text lines.

    Usage example:  pprint.pprint(getEditText(editArea))
    '''
    return _getMultipleWindowValues(hwnd,
                                    getCountMessage=win32con.EM_GETLINECOUNT,
                                    getValueMessage=win32con.EM_GETLINE)
    
def setEditText(hwnd, text, append=False):
    '''Set an edit control's text.
    
    Arguments:
    hwnd            The edit control's hwnd.
    text            The text to send to the control. This can be a single
                    string, or a sequence of strings. If the latter, each will
                    be become a a seperate line in the control.
    append          Should the new text be appended to the existing text?
                    Defaults to False, meaning that any existing text will be
                    replaced. If True, the new text will be appended to the end
                    of the existing text.
                    Note that the first line of the new text will be directly
                    appended to the end of the last line of the existing text.
                    If appending lines of text, you may wish to pass in an
                    empty string as the 1st element of the 'text' argument.

    Usage example:  print "Enter various bits of text."
                    setEditText(editArea, "Hello, again!")
                    time.sleep(.5)
                    setEditText(editArea, "You still there?")
                    time.sleep(.5)
                    setEditText(editArea, ["Here come", "two lines!"])
                    time.sleep(.5)
                    
                    print "Add some..."
                    setEditText(editArea, ["", "And a 3rd one!"], append=True)
                    time.sleep(.5)'''
    
    # Ensure that text is a list        
    try:
        text + ''
        text = [text]
    except TypeError:
        pass

    # Set the current selection range, depending on append flag
    if append:
        win32gui.SendMessage(hwnd,
                             win32con.EM_SETSEL,
                             -1,
                             0)
    else:
        win32gui.SendMessage(hwnd,
                             win32con.EM_SETSEL,
                             0,
                             -1)
                             
    # Send the text
    win32gui.SendMessage(hwnd,
                         win32con.EM_REPLACESEL,
                         True,
                         os.linesep.join(text))

def _getMultipleWindowValues(hwnd, getCountMessage, getValueMessage):
    '''A common pattern in the Win32 API is that in order to retrieve a
    series of values, you use one message to get a count of available
    items, and another to retrieve them. This internal utility function
    performs the common processing for this pattern.

    Arguments:
    hwnd                Window handle for the window for which items should be
                        retrieved.
    getCountMessage     Item count message.
    getValueMessage     Value retrieval message.

    Returns:            Retrieved items.'''
    result = []
    
    VALUE_LENGTH = 256
    bufferlength_int  = struct.pack('i', VALUE_LENGTH) # This is a C style int.
    
    valuecount = win32gui.SendMessage(hwnd, getCountMessage, 0, 0)
    for itemIndex in range(valuecount):
        valuebuffer = array.array('c',
                                  bufferlength_int +
                                  " " * (VALUE_LENGTH - len(bufferlength_int)))
        valueLength = win32gui.SendMessage(hwnd,
                                           getValueMessage,
                                           itemIndex,
                                           valuebuffer)
        result.append(valuebuffer.tostring()[:valueLength])
    return result

def _windowEnumerationHandler(hwnd, resultList):
    '''Pass to win32gui.EnumWindows() to generate list of window handle,
    window text, window class tuples.'''
    resultList.append((hwnd,
                       win32gui.GetWindowText(hwnd),
                       win32gui.GetClassName(hwnd)))
    
def _buildWinLong(high, low):
    '''Build a windows long parameter from high and low words.
    See http://support.microsoft.com/support/kb/articles/q189/1/70.asp
    '''
    # return ((high << 16) | low)
    return int(struct.unpack('>L',
                             struct.pack('>2H',
                                         high,
                                         low)) [0])
        

    
def _sendNotifyMessage(hwnd, nofifyMessage):
    '''Send a notify message to a control.'''
    win32gui.SendMessage(win32gui.GetParent(hwnd),
                         win32con.WM_COMMAND,
                         _buildWinLong(nofifyMessage,
                                       win32api.GetWindowLong(hwnd,
                                                              win32con.GWL_ID)),
                         hwnd)
    

def _postNotifyMessage(hwnd, nofifyMessage):
    '''Send a notify message to a control.'''
    win32gui.PostMessage(win32gui.GetParent(hwnd),
                         win32con.WM_COMMAND,
                         _buildWinLong(nofifyMessage,
                                       win32api.GetWindowLong(hwnd,
                                                              win32con.GWL_ID)),
                         hwnd)

def _normaliseText(controlText):
    '''Remove '&' characters, and lower case.
    Useful for matching control text.'''
    return controlText.lower().replace('&', '')

def _findNamedSubmenu(hMenu, hMenuItemCount, submenuName):
    '''Find the index number of a menu's submenu with a specific name.'''
    
    #print '_findNamedSubmenu fuction',hMenu,submenuName,hMenuItemCount
    for submenuIndex in range(hMenuItemCount):
        submenuInfo = getMenuInfo(hMenu, submenuIndex)
        #print 'submenuInfo',submenuInfo
        if _normaliseText(submenuInfo.name).startswith(_normaliseText(submenuName)):
            return submenuIndex, submenuInfo.submenu, submenuInfo.itemCount
    raise WinGuiAutoError("No submenu found for hMenu=" +
                          repr(hMenu) +
                          ", hMenuItemCount=" +
                          repr(hMenuItemCount) +
                          ", submenuName=" +
                          repr(submenuName))



                
                              
class Bunch(object):
    '''See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52308'''
    
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
        
    def __str__(self):
        state = ["%s=%r" % (attribute, value)
                 for (attribute, value)
                 in self.__dict__.items()]
        return '\n'.join(state)
    
class WinGuiAutoError(Exception):
    pass
        
                       

      
class win_gui(Structure):
    def __init__(self,win_dx='905',win_dy='660',control_dx='869',control_dy='38'):
        self.wdx = string.atoi(win_dx)
        self.wdy = string.atoi(win_dy)
        self.cdx = string.atoi(control_dx)
        self.cdy = string.atoi(control_dy)
        self.lin_hwnd =None
        self.ld_x=0
        self.ld_y=0
        self.error_NG=''
        global MAIN_HWND
        global global_wind_list
        global global_all_list
        MAIN_HWND = 0
        del global_wind_list[:] 
        del global_all_list[:]
    
    def shortcut_keys(self,list_key=[]):
        for x in list_key:
            tmp = self.dic_keycode(x)
            win32api.keybd_event(tmp,0,0,0)
        for x in reversed(list_key):
            tmp = self.dic_keycode(x)
            win32api.keybd_event(tmp,0,win32con.KEYEVENTF_KEYUP,0)
            
    def app_first(self,str_app):
        hwnd = win32gui.FindWindow(None, str_app)
        print hwnd
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
        if hwnd>0:
            win32gui.SetForegroundWindow(hwnd)
            #win32gui.ShowWindow(hwnd,win32con.SW_SHOWMAXIMIZED)
            return True
        return False
    
    
    def app_Move(self,str_app):
        #tmp=(string.atoi(lb_dx),string.atoi(lb_dy))
        hwnd = win32gui.FindWindow(None, str_app)
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
        if hwnd>1:
            win32gui.MoveWindow(hwnd,0,0,self.wdx,self.wdy,1)
        else:
            return False
        return True
    
    
    def findTopWindow(self,wantedText=None, wantedClass=None, selectionFunction=None):
        '''Find the hwnd of a top level window.
        You can identify windows using captions, classes, a custom selection
        function, or any combination of these. (Multiple selection criteria are
        ANDed. If this isn't what's wanted, use a selection function.)

        Arguments:
        wantedText          Text which the required window's captions must contain.
        wantedClass         Class to which the required window must belong.
        selectionFunction   Window selection function. Reference to a function
                            should be passed here. The function should take hwnd as
                            an argument, and should return True when passed the
                            hwnd of a desired window.
                    
        Raises:
        WinGuiAutoError     When no window found.

        Usage example:      optDialog = findTopWindow(wantedText="Options")
        '''
        topWindows = self.findTopWindows(wantedText, wantedClass, selectionFunction)
        if topWindows:
            win32gui.MoveWindow(topWindows[0],0,0,self.wdx,self.wdy,1)
            return topWindows[0]
        else:
            raise WinGuiAutoError("No top level window found for wantedText=" +
                                repr(wantedText) +
                                ", wantedClass=" +
                                repr(wantedClass) +
                                ", selectionFunction=" +
                                repr(selectionFunction))
                               
    def findTopWindows(self,wantedText=None, wantedClass=None, selectionFunction=None):
        '''Find the hwnd of top level windows.
        You can identify windows using captions, classes, a custom selection
        function, or any combination of these. (Multiple selection criteria are
        ANDed. If this isn't what's wanted, use a selection function.)

        Arguments:
        wantedText          Text which required windows' captions must contain.
        wantedClass         Class to which required windows must belong.
        selectionFunction   Window selection function. Reference to a function
                            should be passed here. The function should take hwnd as
                            an argument, and should return True when passed the
                            hwnd of a desired window.

        Returns:            A list containing the window handles of all top level
                            windows matching the supplied selection criteria.

        Usage example:      optDialogs = findTopWindows(wantedText="Options")
        '''
        results = []
        topWindows = []
        win32gui.EnumWindows(_windowEnumerationHandler, topWindows)
        for hwnd, windowText, windowClass in topWindows:
            if wantedText and not _normaliseText(wantedText) in _normaliseText(windowText):
                continue
            if wantedClass and not windowClass == wantedClass:
                continue
            if selectionFunction and not selectionFunction(hwnd):
                continue
            results.append(hwnd)
        return results

    def GetChildapp(self,str_app):
        print '******** GetChildapp fuction ********'
        hwnd = win32gui.FindWindow(None, str_app)
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
        if hwnd>1:
            hChild =  win32gui.GetWindow(hwnd,win32con.GW_CHILD)
            bufLen=1024
            buf =win32gui.PyMakeBuffer(bufLen)
            totalnum = 1 
            while hChild :
                hChild = win32gui.GetWindow(hChild,win32con.GW_HWNDNEXT)
                n = win32gui.SendMessage(hChild,win32con.WM_GETTEXT,bufLen,buf)
                str = buf[:n]
                print '@@@@@@@@@@@'
                print win32gui.GetWindowText(hChild)
                print str
                '''
                if totalnum ==3:
                    win32gui.SendMessage(hChild,win32con.WM_SETTEXT,None,'Realtek 10/100/1000 Ethernet NIC')
                '''
                print  totalnum,hChild
                totalnum = totalnum + 1
                
        print '******** GetChildapp fuction ********',totalnum
    
    def Mousepos_print(self,count='20'):
        
        total = 0
        while True:
            time.sleep(3)
            tmp = win32gui.GetCursorPos()
            #self.ld_x = tmp[0]
            #self.ld_y = tmp[1]
            print "GetCursorPos tmp:", tmp 
            total = total +1 
            if string.atoi(count) == 0:
                continue
            if total>string.atoi(count):
                break
        return True
    
    def Mousepos_set(self,lb_dx='224',lb_dy='366'):
        time.sleep(1)
        tmp=(string.atoi(lb_dx),string.atoi(lb_dy))
        win32api.SetCursorPos(tmp)
        
    def Mouseclick_lb(self,tmp=(220,230)):
        win32api.SetCursorPos(tmp)
        print 'Mouseclick_lb tmp:',tmp
        time.sleep(1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tmp[0], tmp[1]) 
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tmp[0], tmp[1])
        time.sleep(0.1)
        return True
    
    def Find_Gui_Tree(self,str_app='New Scenario',control_class='Button',filename='test_baidu',control_name='AfxOleControl'):
       
        print "*********Find_Gui_Tree function**********"
        time.sleep(1)
        #self.Mousepos_print()
        print 'str_app',str_app
        hwnd = win32gui.FindWindow(None, str_app)
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
        print 'hwnd',hwnd
        win32gui.SetForegroundWindow(hwnd)
        
        print 'hwnd :',hwnd,str_app
        win32gui.SetForegroundWindow(hwnd)
        
        #self.Mousepos_print('5')
        comboHwnd = win32gui.FindWindowEx(hwnd,0,control_class,None)
        print '111111111111comboHwnd',comboHwnd
        while comboHwnd:
            print "control_class:",comboHwnd
            cla =  win32gui.GetClassName(comboHwnd)
            print "control_class_NAME:",cla
            bufLen=1024
            buf =win32gui.PyMakeBuffer(bufLen)
            n = win32gui.SendMessage(comboHwnd,win32con.WM_GETTEXT,bufLen,buf)
            str = buf[:n]
            print str
            '''
            if control_class in cla:
                n = win32gui.SendMessage(comboHwnd,win32con.WM_GETTEXT,bufLen,buf)
                str = buf[:n]
                print str
                if (len(control_name ) ==0 and n==0)  or ((len(control_name )>0 and  str.find(control_name)>-1 )):
                    win32gui.SendMessage(comboHwnd,win32con.WM_LBUTTONDOWN,0)
                    time.sleep(0.05)
                    win32gui.SendMessage(comboHwnd,win32con.WM_LBUTTONUP,0)
                    time.sleep(0.05)
                    win32gui.SendMessage(win32con.WM_CLOSE,0,0)
                    break
            '''
            comboHwnd = win32gui.GetWindow(comboHwnd,win32con.GW_HWNDNEXT)
        time.sleep(1)
        
        
        return True
    
    def Find_Gui_key_run(self,str_app='´ò¿ª'):
        time.sleep(1)
        print "*********Find_Gui_button function**********"
        #self.Mousepos_print()
        print 'control_name:',str_app
        hwnd = win32gui.FindWindow(None, str_app)
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
        print 'hwnd :',hwnd,str_app
        win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F5, 0)
        return True
    
    def Find_Gui_window(self,str_app='LoadRunner Controller'):
        list_a=[]
        hwnd = win32gui.FindWindow(None, str_app)
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
        if hwnd<1:
            return list_a
        else:
            list_a.append(str_app)
        self.lin_hwnd  = hwnd
            #tuple.append(hwnd)
        return list_a
    
    def Find_Gui_title(self,str_app='Edit Action',find_control_class='0',control_class='WindowsForms10.Window.8.app.0.2e0c681',text='10',control_name=''):
        time.sleep(1)
        print "*********Find_Gui_title function**********"
        #self.Mousepos_print()
        print 'control_name:',str_app,find_control_class
        hwnd = win32gui.FindWindow(None, str_app)
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
        print 'hwnd :',hwnd,str_app
        win32gui.SetForegroundWindow(hwnd)
        comboHwnd = win32gui.FindWindowEx(hwnd,0,control_class,None)
        print 'comboHwnd',comboHwnd
        while comboHwnd:
            cla =  win32gui.GetClassName(comboHwnd)
            print "control_class_name:",cla
            bufLen=1024
            buf =win32gui.PyMakeBuffer(bufLen)
            n = win32gui.SendMessage(comboHwnd,win32con.WM_GETTEXT,bufLen,buf)
            str = buf[:n]
            print 'buf:',str
            if str.find(find_control_class)>-1:
                win32gui.PostMessage(comboHwnd,win32con.WM_LBUTTONDOWN,0)
                time.sleep(0.05)
                #win32gui.SendMessage(comboHwnd,win32con.WM_LBUTTONUP,0)
                win32gui.PostMessage(comboHwnd,win32con.WM_LBUTTONUP,0)
                time.sleep(0.05)
                time.sleep(1)
                break
            comboHwnd = win32gui.GetWindow(comboHwnd,win32con.GW_HWNDNEXT)
        return True
        
    
    def Find_Gui_button_hwnd(self,str_app='´ò¿ª',control_class='Button',control_name='´ò¿ª(&O)'):
        time.sleep(1)
        result = False
        print "*********Find_Gui_button function**********"
        #self.Mousepos_print()
        #print 'control_name:',str_app,',',control_name
        hwnd = win32gui.FindWindow(None, str_app)
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
        comboHwnd = win32gui.FindWindowEx(hwnd,0,control_class,None)
        #print 'comboHwnd',comboHwnd
        
        while comboHwnd:
            #print "control_class:",comboHwnd,control_name
            cla =  win32gui.GetClassName(comboHwnd)
            #print 'cla:' ,cla
            bufLen=1024
            buf =win32gui.PyMakeBuffer(bufLen)
            if control_class in cla:
                n = win32gui.SendMessage(comboHwnd,win32con.WM_GETTEXT,bufLen,buf)
                str = buf[:n]
                #print 'buttonname ,len,n,find :',str,len(control_name ),n,str.find(control_name)
                if str.find(control_name)>-1:
                    result = True
                    win32gui.PostMessage(comboHwnd,win32con.WM_LBUTTONDOWN,0)
                    time.sleep(0.05)
                    #win32gui.SendMessage(comboHwnd,win32con.WM_LBUTTONUP,0)
                    win32gui.PostMessage(comboHwnd,win32con.WM_LBUTTONUP,0)
                    time.sleep(0.05)
                    time.sleep(1)
                    print 'find control_name',result
                    break
            comboHwnd = win32gui.GetWindow(comboHwnd,win32con.GW_HWNDNEXT)
        if result ==False:
            comboHwnd = -1
        return comboHwnd
    
    def Find_Gui_button(self,str_app='´ò¿ª',control_class='Button',control_name='´ò¿ª(&O)'):
        time.sleep(1)
        result = False
        print "*********Find_Gui_button function**********"
        #self.Mousepos_print()
        #print 'control_name:',str_app,',',control_name
        hwnd = win32gui.FindWindow(None, str_app)
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
        #print 'hwnd :',hwnd,str_app
        win32gui.SetForegroundWindow(hwnd)
        comboHwnd = win32gui.FindWindowEx(hwnd,0,control_class,None)
        #print 'comboHwnd',comboHwnd
        
        while comboHwnd:
            print "control_class:",comboHwnd,control_name
            cla =  win32gui.GetClassName(comboHwnd)
            print 'cla:' ,cla
            bufLen=1024
            buf =win32gui.PyMakeBuffer(bufLen)
            if control_class in cla:
                n = win32gui.SendMessage(comboHwnd,win32con.WM_GETTEXT,bufLen,buf)
                str = buf[:n]
                print 'buttonname ,len,n,find :',str,len(control_name ),n,str.find(control_name)
                if (len(control_name ) ==0 and n==0)  or ((len(control_name )>0 and  str.find(control_name)>-1 )):
                    #win32gui.SendMessage(comboHwnd,win32con.WM_LBUTTONDOWN,0)
                    win32gui.PostMessage(comboHwnd,win32con.WM_LBUTTONDOWN,0)
                    time.sleep(0.05)
                    #win32gui.SendMessage(comboHwnd,win32con.WM_LBUTTONUP,0)
                    win32gui.PostMessage(comboHwnd,win32con.WM_LBUTTONUP,0)
                    time.sleep(0.05)
                    #win32gui.SendMessage(win32con.WM_CLOSE,0,0)
                    #print '111'
                    result = True
                    break
            comboHwnd = win32gui.GetWindow(comboHwnd,win32con.GW_HWNDNEXT)
        time.sleep(1)
        return result
        
    def Find_Gui_edit(self,str_app='´ò¿ª',control_class='ComboBox',filename='wtp_cuo1.pcap',control_name='',stop_flag='0'):
       
        print "*********Find_Gui_edit function**********",str_app
        time.sleep(1)
        #self.Mousepos_print()
        print 'str_app',str_app
        hwnd = win32gui.FindWindow(None, str_app)
        print 'hwnd',hwnd
        win32gui.SetForegroundWindow(hwnd)
        comboHwnd = win32gui.FindWindowEx(hwnd,0,control_class,None)
        bufLen=256
        buf =win32gui.PyMakeBuffer(bufLen)
        while comboHwnd:
            if stop_flag=='1':
                win32gui.SendMessage(comboHwnd,win32con.WM_SETTEXT,bufLen,filename)
                time.sleep(1)
                break
            print "control_class:",comboHwnd
            cla =  win32gui.GetClassName(comboHwnd)
            print cla
            
            if control_class in cla:
                n = win32gui.SendMessage(comboHwnd,win32con.WM_GETTEXT,bufLen,buf)
                str = buf[:n]
                if (len(control_name ) ==0 and n==0)  or (len(control_name )>0 and  str.find(control_name)>-1 ):
                    win32gui.SendMessage(comboHwnd,win32con.WM_SETTEXT,bufLen,filename)
                    time.sleep(1)
                    break
            comboHwnd = win32gui.GetWindow(comboHwnd,win32con.GW_HWNDNEXT)
        time.sleep(1)
        return True
    
    def Mouse_LB_Double(self,str_app,lb_dx,lb_dy,Flag='1'):
        time.sleep(1)
        tmp=(string.atoi(lb_dx),string.atoi(lb_dy))
        hwnd = win32gui.FindWindow(None, str_app)
        print 'Mouse_RB str_app,hwnd ',str_app,hwnd
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
            
        win32api.SetCursorPos(tmp)
        
        time.sleep(1)
        #win32api.SetDoubleCIckTime()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tmp[0], tmp[1]) 
        time.sleep(0.005)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tmp[0], tmp[1])
        time.sleep(0.005)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tmp[0], tmp[1]) 
        time.sleep(0.005)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tmp[0], tmp[1])
        time.sleep(0.005)
        return True
    
    
    def Mouse_LB_D(self,str_app,lb_dx,lb_dy,Flag='1'):
        time.sleep(1)
        tmp=(string.atoi(lb_dx),string.atoi(lb_dy))
        hwnd = win32gui.FindWindow(None, str_app)
        print 'Mouse_RB str_app,hwnd ',str_app,hwnd
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
            
        win32api.SetCursorPos(tmp)
        
        time.sleep(1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tmp[0], tmp[1]) 
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tmp[0], tmp[1])
        time.sleep(0.05)
        return True
    
    
    def Mouse_RB(self,str_app,lb_dx,lb_dy,Flag='1'):
        print "*********Mouse_RB function**********"
        time.sleep(1)
        tmp=(string.atoi(lb_dx),string.atoi(lb_dy))
        hwnd = win32gui.FindWindow(None, str_app)
        print 'Mouse_RB str_app,hwnd ',str_app,hwnd
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
            #win32gui.ShowWindow(hwnd, 0)
        win32api.SetCursorPos(tmp)
        print 'Mouse_RB tmp =',tmp
        if Flag == '1':
            time.sleep(1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,tmp[0], tmp[1]) 
            time.sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,tmp[0], tmp[1])
            time.sleep(0.05)
        return True
    
    def Mouse_LB(self,str_app,lb_dx,lb_dy,Flag='1'):
        print "*********Mouse_LB function**********"
        time.sleep(1)
        tmp=(string.atoi(lb_dx),string.atoi(lb_dy))
        hwnd = win32gui.FindWindow(None, str_app)
        if hwnd < 1:
            hwnd = self.find_main_window(str_app)
            #win32gui.ShowWindow(hwnd, 0)
            win32api.SetCursorPos(tmp)
            print 'Mouse_LB tmp =',tmp
            if Flag == '1':
                time.sleep(1)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tmp[0], tmp[1]) 
                time.sleep(0.05)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tmp[0], tmp[1])
                time.sleep(0.05)
        return True
        
    def is_win_ok(self,hwnd,starttext,lb_dx='869',lb_dy='38',win_dx='',win_dy=''):
        #print "*********is_win_ok function**********"
        #print "*********is_win_ok function starttext**********",starttext
        if len(win_dx)>0:
            self.wdx = string.atoi(win_dx)
        if len(win_dy)>0:
            self.wdy = string.atoi(win_dy)
        s = win32gui.GetWindowText(hwnd)
        #print s
        if s.startswith(starttext):
            #print "*********is_win_ok function s**********",s
            #print (s)
            dlg=win32gui.FindWindow(None,s)
            time.sleep(1)
            #win32gui.ShowWindow(dlg,win32con.SW_SHOWMAXIMIZED)
            win32gui.ShowWindow(dlg,win32con.SW_SHOW)
            time.sleep(1)
            #print 'self.wdx,self.wdy:',self.wdx,self.wdy
            #win32gui.MoveWindow(dlg,0,0,self.wdx,self.wdy,1)
            time.sleep(1)
            win32gui.SetForegroundWindow(dlg)
            time.sleep(1)
            #win32gui.ShowWindow(dlg,win32con.SW_SHOWMAXIMIZED)
            win32gui.ShowWindow(dlg,win32con.SW_SHOW)
            time.sleep(1)
            
            #self.Mouse_LB(lb_dx,lb_dy)
            global MAIN_HWND
            MAIN_HWND = hwnd
            return None
        return 1
        
    
    def find_main_window(self,starttxt):
        print "*********find_main_window function**********"
        global MAIN_HWND
        MAIN_HWND = 0
        win32gui.EnumChildWindows(0, self.is_win_ok, starttxt)
        return MAIN_HWND
    
    def sleep(self,TIME):
        time.sleep(string.atoi(TIME))
        return True
    
    
    def winfun(self, hwnd,lparam):
        print "*********winfun function**********"
        s = win32gui.GetWindowText(hwnd)
        if len(s) > 3:
            print("winfun, child_hwd: %d   txt: %s" % (hwnd, s))
        return 1
    
    def startapp(self,filename='F:\\anysend\\anysend.exe'):
        pid_name = filename.split('\\')[-1]
        kill_program(pid_name,pid_name)
        do_exec = do_win_exec(filename)
        do_exec.sub_ac_upgrade_exec()
        time.sleep(1)
        REC_read= 'wmic process where caption="'+pid_name+'" get caption,commandline /value'
        print_mes = os.popen(REC_read).read() 
        print print_mes
        info_public(print_mes)
        if print_mes.find(pid_name)>-1:
            return True
        else:
            return False
        
   
        
    
    def startapp_chdir(self,filename='F:\\anysend\\anysend.exe'):
        pid_name = filename.split('\\')[-1]
        kill_program(pid_name,pid_name)
        do_exec = do_win_exec(filename)
        do_exec.sub_do_exe()
        time.sleep(1)
        REC_read= 'wmic process where caption="'+pid_name+'" get caption,commandline /value'
        print_mes = os.popen(REC_read).read() 
        print print_mes
        info_public(print_mes)
        if print_mes.find(pid_name)>-1:
            return True
        else:
            return False
        
        
        
        
    def anysend(self,win_exe='F:\\anysend\\anysend.exe',mes_send='wtp_cuo1.pcap'):
        print "*********main function**********"
        self.startapp(win_exe)
        str_app = 'AnySend'
        lb_dx='14'
        lb_dy='38'
        self.Mouse_LB(str_app,lb_dx,lb_dy)
        
        str_app2='´ò¿ª'
        control_class='ComboBox'
        control_name=''
        #filename='event_wtp_request_send1.pcap'
        #filename1='wtp_cuo1.pcap'
        
        self.Find_Gui_edit(str_app2,control_class,mes_send,control_name)
        self.Find_Gui_button()
    
        
        self.wdx=508
        self.wdy=250
        str_app1 ='Read'
        control_class = 'TBitBtn'
        control_name ='OK'
        lb_dx='194'
        lb_dy='225'
        self.Mouse_LB(str_app1,lb_dx,lb_dy,'1')
    
        self.wdx=905
        self.wdy=660
        str_app = 'AnySend'
        lb_dx='869'
        lb_dy='38'
        self.Mouse_LB(str_app,lb_dx,lb_dy)
        return True
    
    def loadrunner_Scenario(self,app = 'D:\\Program Files\\HP\\LoadRunner\\bin\\Wlrun.exe',scriptname ='Scenario1.lrs'):
        count = '2'
        #app = 'D:\\Program Files\\HP\\LoadRunner\\bin\\Wlrun.exe'
        self.startapp(app)
        self.sleep(count)
        str_app = 'New Scenario'
        list = [] 
        result = False
        try:
            list = self.Find_Gui_window(str_app)
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        if len(list)>0:
            print list
            control_name = 'Cancel'
            control_class = 'Button'
            self.Find_Gui_button(str_app,control_class,control_name)
        str_app = 'HP LoadRunner Controller'
        self.app_first(str_app)
        self.shortcut_keys(['Ctrl','O'])
        
        str_app = 'Open Scenario'
        self.Find_Gui_edit(str_app,control_class='Edit',filename=scriptname,stop_flag='1')
        time.sleep(2)
        self.app_first(str_app)
        control_name = '´ò¿ª(&O)'
        control_class = 'Button'
        self.Find_Gui_button(str_app,control_class,control_name)
        
        time.sleep(10)
        str_app = 'HP LoadRunner Controller'
        self.app_first(str_app)
        self.shortcut_keys(['F5'])
        
        time.sleep(1)
        list_a = self.Find_Gui_window()
        if len(list_a)>0:
            control_class = 'Button'
            control_name = 'ÊÇ(&Y)'
            try:
                result = self.Find_Gui_button(list_a[0],control_class,control_name)
            except:
                return False
        else:
            result = True
        return result
            
            
        
        #self.shortcut_keys(['Ctrl','O'])
        
        '''
        win32api.keybd_event(17,0,0,0)   #ctrl¼üÎ»ÂëÊÇ17
        win32api.keybd_event(79,0,0,0)  #o¼üÎ»ÂëÊÇ86
        win32api.keybd_event(79,0,win32con.KEYEVENTF_KEYUP,0) #ÊÍ·Å°´¼ü
        win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
        '''
        #str_app = 'New Scenario'
        
        
    
    def loadrunner_control(self,app = 'D:\\Program Files\\HP\\LoadRunner\\bin\\Wlrun.exe',scriptname ='test_c'):
        
        count = '2'
        #app = 'D:\\Program Files\\HP\\LoadRunner\\bin\\Wlrun.exe'
        self.startapp(app)
        self.sleep(count)
        str_app = 'New Scenario'
        self.wdx=586
        self.wdy=442
        self.app_Move(str_app)
        self.Mousepos_print(count)
        self.Mouse_RB(str_app,'94','234')
        self.Mouse_LB_D(str_app,'125','246')
        control_name = '&Browse...'
        control_class = 'Button'
        self.Find_Gui_button(str_app,control_class,control_name)
        self.wdx=243
        self.wdy=350
    
        self.Mousepos_print(count)
        self.Find_Gui_edit('Open Test','Edit',scriptname,'','1')
        self.sleep('5')
        self.Find_Gui_button('Open Test','Button','´ò¿ª(&O)')
        self.Mousepos_print(count)
        
        control_class = 'Button'
        control_name = 'OK'
        self.Find_Gui_button(str_app,control_class,control_name)
        
        self.Mousepos_print(count)
        
        self.wdx=1300
        self.wdy=800
        str_app = 'HP LoadRunner Controller'
        self.Mouse_LB_Double(str_app,'175','595')
        self.Mousepos_print(count)
        
        str_app = 'Edit Action'
        
        self.wdx =460
        self.wdy = 220
        self.app_Move(str_app)
        self.Mousepos_print(count)
        self.Mouse_LB_D(str_app,'50','80')
        
        self.Mousepos_print(count)
        
        find_control_class='OK'
        self.Find_Gui_title(str_app,find_control_class)
        self.Mousepos_print(count)
        
        self.wdx=560
        self.wdy=150
        str_app ='Scheduler actions'
        list_a =[]
        list_a = self.Find_Gui_window(str_app)
        if len(list_a)>0:
            control_class = 'Button'
            control_name = 'ÊÇ(&Y)'
            self.Find_Gui_button(list_a[0],control_class,control_name)
            
        self.wdx=1076
        self.wdy=660
        self.sleep(count)
        str_app = 'HP LoadRunner Controller'
        self.Find_Gui_key_run(str_app)
        self.sleep(count)
        
        list_a =[]
        list_a = self.Find_Gui_window()
        if len(list_a)>0:
            control_class = 'Button'
            control_name = 'ÊÇ(&Y)'
            self.Find_Gui_button(list_a[0],control_class,control_name)
        
        return True
       
    def IxChariot_Start(self,app = 'D:\\Program Files\\Ixia\\IxChariot\\IxChariot.exe',scriptname ='test1.tst'):
        count = '2'
        try:
            self.startapp(app)
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        self.sleep(count)
        str_app = 'IxChariot Test'
        list = [] 
        result = False
        try:
            list = self.Find_Gui_window(str_app)
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        
        print list
        print self.app_first(str_app)
        time.sleep(1)
        try:
            self.shortcut_keys(['Ctrl','O'])
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        time.sleep(1)
        #self.shortcut_keys(['O'])
        #time.sleep(1)
        print 'here***************************'
        str_app1 = 'Open a Test File'
        try:
            self.Find_Gui_edit(str_app1,control_class='Edit',filename=scriptname,stop_flag='1')
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        time.sleep(2)
        try:
            self.app_first(str_app1)
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        control_name = '´ò¿ª(&O)'
        control_class = 'Button'
        try:
            self.Find_Gui_button(str_app1,control_class,control_name)
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        time.sleep(1)
        #self.app_first(str_app)
        try:
            self.shortcut_keys(['Ctrl','R'])
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        return True
        
    
    
    def IxChariot_Start_Configure(self,app = 'D:\\Program Files\\Ixia\\IxChariot\\IxChariot.exe',address1='192.168.4.29',address2='192.168.4.29',pair_comment ='aaaa',protocol='TCP',service='G711',script='High_Performance_Throughput.scr'):
        count = '2'
        try:
            self.startapp(app)
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        self.sleep(count)
        str_app = 'IxChariot Test'
        list = [] 
        result = False
        try:
            list = self.Find_Gui_window(str_app)
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        
        #print list
        self.app_first(str_app)
        time.sleep(1)
        try:
            self.shortcut_keys(['Ctrl','P'])
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        time.sleep(1)
        #self.shortcut_keys(['O'])
        #time.sleep(1)
        #print 'here***************************'
        self.wdx=450
        self.wdy=290
        
        str_app_point = 'Add an Endpoint Pair'
        hwnd = findTopWindow(wantedText=str_app_point)
        phwnd  = hwnd
        win32gui.MoveWindow(hwnd,0,0,self.wdx,self.wdy,1)
        time.sleep(1)
        list = []
        #pprint.pprint(dumpWindow(hwnd))
        list = lst_add_all(dumpWindow(hwnd))
        time.sleep(1)
        hwnd = hwd_get_pos(list,(89,33,415,51))
        print 'pair_comment hwd_get_pos',hwnd
        setEditText(hwnd,pair_comment)
        
        hwnd = hwd_get_pos(list,(125,78,412,91))
        print 'address1 hwd_get_pos',hwnd
        setEditText(hwnd,address1)
        
        hwnd = hwd_get_pos(list,(125,103,412,116))
        print 'address2 hwd_get_pos',hwnd
        setEditText(hwnd,address2)
        
        hwnd = hwd_get_pos(list,(12,142,208,161))
        print 'protocol hwd_get_pos',hwnd
        setEditText(hwnd,protocol)
        
        hwnd = hwd_get_pos(list,(219,145,392,158))
        print 'service hwd_get_pos',hwnd
        setEditText(hwnd,service)
        time.sleep(1)
        clickButton(findControl(phwnd,wantedText='Select &Script'))
        
        str_app ='Open a Script File'
        self.app_first(str_app)
        time.sleep(1)
        phwnd1 = findTopWindow(wantedText=str_app)
        
        hwnd = findControl(phwnd1,wantedClass='Edit')
        setEditText(hwnd,script)
        time.sleep(1)
        hwnd = findControl(phwnd1,wantedText='´ò¿ª(&O)')
        clickButton(hwnd)
        
        
        str_app_point = 'Add an Endpoint Pair'
        self.app_first(str_app_point)
        time.sleep(1)
        clickButton(findControl(phwnd,wantedText='&OK'))
        
        time.sleep(1)
        try:
            self.shortcut_keys(['Ctrl','R'])
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        
        #time.sleep(1)
        #self.Find_Gui_button(str_app=str_app_point,control_class='Button',control_name='Select &Script')
        #self.Mousepos_print('0')
        return True
    
    
    
    def wireshark_stop(self,num_total='1',pid_n='EPA',filename=''):
        
        count ='2'
        app = 'Capturing from'
        list = [] 
        num = string.atoi(num_total)
        tmp_file = ''
        try:
            list = self.Find_Gui_window(app)
            if len(list) == 0 :
                log_print('Not find wireshark Capturing ')
                return False
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        
        self.app_first(app)
        self.shortcut_keys(['Ctrl','E'])
        time.sleep(1)
        self.shortcut_keys(['Shift','Ctrl','S'])
        time.sleep(2)
        try:
            hwd = findTopWindow(wantedText='Wireshark: Save file as')
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        if hwd :
            #print hwd
            
            
            edit_list = findControls(hwd,wantedClass='Edit')
            t_hwnd = 0 
            for x in edit_list:
                rect_list = win32gui.GetWindowRect(x)
                t_dx = rect_list[2]-rect_list[0]
                t_dy = rect_list[3]-rect_list[1]
                t_tuple = (t_dx ,t_dy)
                if t_tuple ==(224,13):
                    t_hwnd = x
                    break
            if t_hwnd == 0:
                return False
            
            #setEditText(t_hwnd,filename)
            if filename =='':
                path1 = os.path.abspath(sys.argv[0])
                findstr = 'Simu'
                path_parent = Getfindpath(path1,findstr)
                filename = path_parent + '\\tmp_result'
            
            tmp_file = filename +'\\' +time.strftime(KEY_TIME_FORMAT) +'.log'
            setEditText(t_hwnd,tmp_file)
            time.sleep(1)
            #print 'findControls,ComboBox:',findControls(hwd,wantedClass='ComboBox')
            ComboBox_list = findControls(hwd,wantedClass='ComboBox')
            c_list = self.list_find_combo(ComboBox_list)
            if c_list[0]==True:
                print 'findControls,ComboBox:',c_list
                #selectComboboxItem(c_list[2],c_list[1])  
                #clickButton(c_list[2])
                selectComboboxItemThird(c_list[2],c_list[1])
            time.sleep(1) 
            hcwnd = findControl(hwd,wantedText='Displayed',wantedClass='Button')
            print 'Displayed:',hcwnd
            tmp=win32gui.GetWindowRect(hcwnd)
            t_dx =  tmp[0]+20
            t_dy =  tmp[1]+10
            t_tuple = (t_dx,t_dy)
            self.Mouseclick_lb(t_tuple) 
        else:
            return False
        
        time.sleep(2)
        hcwnd = findControl(hwd,wantedText='±£´æ(&S)',wantedClass='Button')
        print 'button :',hcwnd
        tmp=win32gui.GetWindowRect(hcwnd)
        print tmp
        t_dx =  tmp[0]+10
        t_dy =  tmp[1]+10
        t_tuple = (t_dx,t_dy)
        self.Mouseclick_lb(t_tuple) 
        #clickButton(hwd)
        if tmp_file =='':
            return False
        file_object1 = open(tmp_file,'r')
        
        FINDSTR = '+---------+---------------+----------+'
        tmp_total_find = 0 
        for line in file_object1:
            if line.find(FINDSTR)>-1:
                tmp_total_find= tmp_total_find +1
        file_object1.close()
        msg = 'capult ' + str(tmp_total_find) + ' packets' 
        log_print(msg)
        
        
        pid_name = pid_n + '.exe'
        kill_program(pid_name,pid_name)
        
        if tmp_total_find >=num:
            return True
        else:
            return False
                
        
    def list_find_combo(self,ComboBox_list = [],tmp_str ='K12'):
        find_flag = False
        item = 0
        list = [False, 0,0]
        for x in ComboBox_list:
            comlist =  getComboboxItems(x)
            item = 0
            for y in comlist:
        
                if y.find(tmp_str)>-1:
                    find_flag = True
                    list = (find_flag,item,x)
                    return list
                item  = item  + 1
        return list 
    
    
    
    
    def Proc_Run(self,app='E:\\produc_test\\Release2\\Release\\factorytool.exe',timesleep='2'):
        count = '2'
        try:
            self.startapp(app)
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        self.sleep(timesleep)
        i=0
        hwnd = 0
        while i<15:
           
            win_text = '��ӭʹ�ø����⹤��'
            try:
                #print 233442,self.findTopWindows()
                hwnd = win32gui.FindWindow(None, win_text)
                #hwnd = self.findTopWindow(wantedText=win_text,wantedClass = win_name)
                if hwnd>1:
                    break
            except Exception ,e:
               
                i+=1
                time.sleep(1)
       
        win_name ='abcd'
        win_ctrl ='Edit'
        
        hwnd_ctrl = findControls(hwnd,wantedClass=win_ctrl)[0]
        
        setEditText(hwnd_ctrl,win_name)
       
        win_ctrl ='Button'
        
        hwnd_ctrl = findControls(hwnd,wantedClass=win_ctrl)[0]
       
        clickButton(hwnd_ctrl)
        
        
        i = 0 
        hwnd = 0
        while i<15:
           
            win_text = '���Ե���'
            try:
                #print 233442,self.findTopWindows()
                hwnd = win32gui.FindWindow(None, win_text)
                #hwnd = self.findTopWindow(wantedText=win_text,wantedClass = win_name)
                if hwnd>1:
                    break
            except Exception ,e:
               
                i+=1
                time.sleep(1)
                
        time.sleep(1)
        
        win32api.keybd_event(13,0,0,0)
        win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
        
        i = 0 
        hwnd = 0
        while i<15:
            win_text = 'MAC���������'
            try:
                #print 233442,self.findTopWindows()
                hwnd = win32gui.FindWindow(None, win_text)
                #hwnd = self.findTopWindow(wantedText=win_text)
                if hwnd>1:
                    break
            except Exception ,e:
                i+=1
                time.sleep(1)
                
        time.sleep(1)
        
        i = 0
        j = 0
        win_ctrl = 'ComboBox'
        hwnd_ctrl = findControls(hwnd,wantedClass=win_ctrl)[0]
            
        #value11 = getComboboxItems(hwnd_ctrl)
        #print '11111:',value11,value11[1]
        com_item = 1 
        try:
            find_str1 ='Simu'
            path1 = os.path.abspath(sys.argv[0])
            path_parent1 = Getfindpath(path1,find_str1)
            readini_path  =  path_parent1 + '\\auto_conf\\version.ini'
            if read_ini(readini_path,'MAC_WRITE','Produc_test').startswith('ONU')==True:
                com_item = 1
            else:
                com_item = 2
        except Exception,e:
            pass
        print 'combox_item:',com_item
        selectComboboxItemThird(hwnd_ctrl,com_item)
            
        time.sleep(3)
        value11 = getComboboxItems(hwnd_ctrl)
        print '11111:',value11,value11[1]
            
        while True:
            i+=1
            j+=1
            win_ctrl ='RichEdit20A'
            hwnd_ctrl = findControls(hwnd,wantedClass=win_ctrl)[0]
            print 23121,hwnd_ctrl
            if i%2==0:
                tex='001913000102'
            else:
                tex='001913000103'
            setEditText(hwnd_ctrl, tex)
            print 23121,hwnd
    
            
            
            win_ctrl ='Button'
            hwnd_ctrl = findControls(hwnd,wantedClass=win_ctrl)
            print  'hwnd_ctrl:',hwnd_ctrl
            
            winname ='ONUtest'
            hwnd_error = win32gui.FindWindow(None, win_text)
            print 'hwnd_error:',hwnd_error
                    
            while True:
                time.sleep(1)
                
                try:
                    hwnd_error = 0
                    winname ='factorytool'
                    
                    #app=application.Application().connect_(title_re=winname )
                    #app.window_(title_re = winname).window_(title_re = u'确定').Click()
                    
                    hwnd_error = win32gui.FindWindow(None, winname)
                    print 'hwnd_error111:',hwnd_error
                    if hwnd_error>1:
                        win_ctrl ='Button'
                        hwnd_ctrl_error = findControls(hwnd_error,wantedClass=win_ctrl)
                        print 'hwnd_ctrl_error:',hwnd_ctrl_error
                        clickButton(hwnd_ctrl_error[0])
                        i =i -1
                except Exception ,e:
                    log_print(e,True)
                    pass
                #bStatus = pywinauto.controls.win32_controls.ButtonWrapper(hwnd_ctrl[1]).GetProperties()['IsEnabled']
                bStatus = controls.win32_controls.ButtonWrapper(hwnd_ctrl[1]).GetProperties()['IsEnabled']
                print 'mac_buttons stauts:',bStatus
                if bStatus ==True:
                    time.sleep(3)
                    break
                
            clickButton(hwnd_ctrl[1])
            print 'success : ', i ,' times',' ,do total: ' ,j,' times'
            
            time.sleep(15)
            
            
                
            #time.sleep(60)
            
        
        
    def wireshark_Start(self,app = 'C:\\Program Files\\EPA\\EPA.exe',eth='1',mode='no_promiscuous',filter='( frame[1:2]==6d:04 ) and ( ip.addr ==192.168.11.28 )',save_name ='test1',timesleep='6'):
        count = '2'
        try:
            self.startapp(app)
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        self.sleep(timesleep)
        
        try:
            self.shortcut_keys(['Ctrl','I'])
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        tmp = 0
        time.sleep(1)
        while True:
            tmp = tmp + 1
            if tmp> string.atoi(eth):
                try :
                    self.findTopWindow(wantedText='Wireshark: Capture Interfaces')
                    self.shortcut_keys(['Enter'])
                    time.sleep(2)
                except Exception ,exc_str:
                    log_print(exc_str)
                break
            else:
                try:
                    self.shortcut_keys(['Alt','O'])
                except Exception ,exc_str:
                    log_print(exc_str)
            time.sleep(1)
        self.wdx=600
        self.wdy=500
        #str_app = 'EPA.exe'
        #print self.app_Move(str_app)
        
        self.sleep('1')
        t_app = 'Easy Protocol Analyzer'
        hwd = findTopWindow(wantedText='Wireshark: Capture Options')
        #hwd =self.Find_Gui_window(t_app)
        win32gui.MoveWindow(hwd,0,0,self.wdx,self.wdy,1)
        #print hwd
        self.sleep('1')
        
        if mode == 'no_promiscuous':
            tmp=(74,128)
            win32api.SetCursorPos(tmp)
            time.sleep(1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tmp[0], tmp[1]) 
            time.sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tmp[0], tmp[1])
            time.sleep(0.05)
            time.sleep(1)
        try:
            self.shortcut_keys(['Alt','S'])
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        self.sleep('1')
        self.wdx = 1400
        self.wdy = 860
        t_list_w = self.Find_Gui_window('Capturing from')
        #win32gui.MoveWindow(hwd,0,0,self.wdx,self.wdy,1)
        tmp_str_window_text =''
        hwnd = self.lin_hwnd
        print 'hwd_get_pos',hwnd
        for x in t_list_w:
            if x.find('Capturing from')>-1:
                tmp_str_window_text = x
                break
        if len(tmp_str_window_text)>0:
            hwd = findTopWindow(wantedText=tmp_str_window_text)
            print 'findTopWindow',hwd
            self.sleep('1')
            #win32gui.ShowWindow(hwd,win32con.SW_SHOWMAXIMIZED)
        
            list = []
            pprint.pprint(dumpWindow(hwd))
            list = lst_add_all(dumpWindow(hwd))
            hwnd = hwd_get_pos(list,(61,88,432,104))
            print 'hwd_get_pos',hwnd
            
            
            text = '( frame[1:2]==6d:04 ) and ( ip.addr ==192.168.11.28 )'
            
            #setEditText(hwnd,'ip.addr == 192.168.4.29')
        
            bufLen=1024
            for x in  filter:
                print 'x,ord(x):',x,ord(x)
              
                tmp = ord(x)
                if tmp>=97:
                    tmp = tmp-32
                try:
                    if tmp == 46:
                        win32api.keybd_event(110,0,0,0)
                        win32api.keybd_event(110,0,win32con.KEYEVENTF_KEYUP,0)
                    elif tmp==61:
                        win32api.keybd_event(187,0,0,0)
                        win32api.keybd_event(187,0,win32con.KEYEVENTF_KEYUP,0)
                    elif tmp==128:
                        win32api.keybd_event(187,0,0,0)
                        win32api.keybd_event(187,0,win32con.KEYEVENTF_KEYUP,0)
                    elif tmp ==58:
                        win32api.keybd_event(16,0,0,0)
                        win32api.keybd_event(186,0,0,0)
                        win32api.keybd_event(186,0,win32con.KEYEVENTF_KEYUP,0)
                        win32api.keybd_event(16,0,win32con.KEYEVENTF_KEYUP,0)
                    elif tmp == 91 :
                        win32api.keybd_event(219,0,0,0)
                        win32api.keybd_event(219,0,win32con.KEYEVENTF_KEYUP,0)
                    elif tmp == 93 :
                        win32api.keybd_event(221,0,0,0)
                        win32api.keybd_event(221,0,win32con.KEYEVENTF_KEYUP,0)
                    elif tmp ==41:
                        win32api.keybd_event(16,0,0,0)
                        win32api.keybd_event(48,0,0,0)
                        win32api.keybd_event(48,0,win32con.KEYEVENTF_KEYUP,0)
                        win32api.keybd_event(16,0,win32con.KEYEVENTF_KEYUP,0)  
                    elif tmp ==40:
                        win32api.keybd_event(16,0,0,0)
                        win32api.keybd_event(57,0,0,0)
                        win32api.keybd_event(57,0,win32con.KEYEVENTF_KEYUP,0)
                        win32api.keybd_event(16,0,win32con.KEYEVENTF_KEYUP,0)      
                    else :
                        self.shortcut_keys([chr(tmp)])
                    
                except Exception ,exc_str:
                    log_print(exc_str)
                    
            self.shortcut_keys(['Alt','A'])
            time.sleep(0.05)
            self.shortcut_keys(['D'])
            time.sleep(1)
            self.shortcut_keys(['Alt','O'])
        return True
    
    
    def SVlanFrame_Start(self,app = 'D:\\tool\\Áú¾í·ç3.02.exe',file_name ='TEST.ini',type='DHCP',startapp = 'Áú¾í·ç'):
        self.lin_hwnd = -1
        try:
            self.startapp(app)
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        try:
            tophwnd = findTopWindow(startapp)
            activateMenuItem(tophwnd,('±¨ÎÄ',type))
            activateMenuItem(tophwnd,('ÎÄ¼þ','µ¼ÈëÅäÖÃ'))
            str_app ='´ò¿ª'
            self.Find_Gui_edit(str_app='´ò¿ª',control_class='Edit',filename=file_name)
            time.sleep(2)
            click_hwnd = self.Find_Gui_button_hwnd(str_app='´ò¿ª',control_class='Button',control_name='´ò¿ª(&O)')
            time.sleep(2)
            t_list = findControl(tophwnd,wantedText='·¢ËÍ(&P)',wantedClass='Button')
            clickButton(t_list)
           
        except Exception ,exc_str:
            log_print(exc_str)
            return False
        return True
    
    def dic_keycode(self,str_s='A'):
        dic={'Backspace':8,'Tab':9,'Enter':13,'Shift':16,'Ctrl':17,'Alt':18,\
        'Caps Lock':20,'Esc':27,'Spacebar':32,'Page Up':33,'Page Down':34,\
        'End':35,'Home':36,'Left':37,'Up':38,'Right':39,'Down':40,'Insert':45,\
        'Delete':46,'Help':47,'Num Lock':144,\
        'F1':112,'F2':113,'F3':114,'F4':115,'F5':116,'F6':117,'F7':118,'F8':119,'F9':120,'F10':121,'F11':122,'F12':123}
        if len(str_s) == 1:
            #print '\n str_s:',str_s,ord(str_s)
            return ord(str_s)
        elif len(str_s)>1:
            if dic.has_key(str_s):
                #print '\n str_s:',str_s,dic[str_s]
                return dic[str_s]
    
    def kill_ie(self,t='test'):
        kill_program('iexplore.exe','Explorer')
        return True
    
if __name__ == "__main__":  
    
    
    test_win = win_gui()
    
    #test_win.Proc_Run()
    #print win32gui.GetProcessHandle(3164)
    #print win32gui.GetModuleHandle('cyt-server.exe')
    #time.sleep(5)
    #print findTopWindow()
    #test_win.Mousepos_print('0')
    
    #print getListboxItems(1706298)
    #test_win.IxChariot_Start()
    #test_win.wireshark_Start()
    #time.sleep(2)
    #test_win.wireshark_stop('1','E:\\Simu_server\\tmp_result')
    #os.startfile('notepad')
    #test_win.SVlanFrame_Start()
    #test_win.Mousepos_print('0')
    #test_win.startapp('E:\\tools\\07-PortalServer\\PortalServer\\ZXISAMWAS\\StartZXISAM.bat')
    #test_win.startapp_chdir('E:\\tools\\07-PortalServer\\PortalServer\\ZXISAMWAS\\StartZXISAM.bat')
    
    
    

