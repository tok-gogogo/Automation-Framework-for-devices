""" 
PAMIE Build 3.0a
Based on cPAMIE and PAM.py by RLM
Revised: March 03, 2009
Developers: Robert L. Marchetti
Description: This python class file allow you to write scripts to Automate the Internet Explorer Browser Client.


This software is provided 'as-is', without any express or implied warranty.
In no event will the authors be held liable for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not claim that you wrote the original software.
   If you use this software in a product, an acknowledgment in the product documentation would be appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.

Special Thanks to: All the Pamie Users and Developers for their time and effort, Steve M., Drunk Bum, Jeff H.,
Dave K., Henry W., Tom C., Scott W.,Margie M. and all others for there support and contributions.
See !whatsnew.txt for modification history.
"""

import sys
sys.path.append(r'c:\python27\lib')

import win32com.client 
import win32gui
import pywintypes
import time
import win32con
import pdb
import re
import random
import string
import pythoncom
import datetime,os,sys
import traceback
import win32com.client

class PAMIE:
    """
    cPAMIE is an automation object based on the work of PAMIE by RLM
    http://pamie.sourceforge.net/
    """
    __version__ = "3.0"

    def __init__(self, url=None, timeOut=3000):
        """ The class instantiation code. When the object is instantiated you can
        pass a starting URL. If no URL is passed then about:blank, a blank
        page, is brought up.
        parameters:
            [url]     - url to navigate to initially
            [timeOut] - how many 100mS increments to wait, 10 = 1sec, 100=10sec
        returns:
            Nothing
        """
        
        #pythoncom.CoInitialize()
        
        self.showDebugging = True           # Show debug print lines?
        self.colorHighlight = "#F6F7AD"     # Set to None to turn off highlighting
        self.frameName = None               # The current frame name or index. Nested frames are
                                            # supported in the format frame1.frame2.frame3
        self.formName = None                # The current form name or index
        self.busyTuner = 1                  # Number of consecutive checks to verify document is no longer busy.
        
        self._ie = win32com.client.dynamic.Dispatch('InternetExplorer.Application')
        if url:
            self._ie.Navigate(url)
        else:
            self._ie.Navigate('about:blank')
          
        self._timeOut = timeOut
        self._ie.Visible = 1
        #self._ie.resizable = 1
        #self._ie.fullscreen = 1
        self._ie.MenuBar=1 
        self._ie.ToolBar=1 
        self._ie.AddressBar=1
        
        self.timer = datetime.datetime.now()
    def pageGetText(self):
        """ Gets the URL, Title and outerHTML
            parameters:
                None
            returns:
                a string consisting of:
                URL,
                Title
                Body block
            as a string. Unfortunately, IE doesn't give a workable solution to 
            saving the complete source so this is as good as it gets until
            someone brighter comes along.  This is useful if you want to compare
            against a previous run for QCing purposes.
        """
        self._wait() 
        if self.frameName:
            return '%s\n%s\n%s'%(self._ie.LocationURL,
                                 self._ie.LocationName,
                                 self._ie.Document.frames[self.frameName].document.body.outerHTML)
        else:
            return '%s\n%s\n%s'%(self._ie.LocationURL,
                                 self._ie.LocationName,
                                 self._ie.Document.body.outerHTML)

    def _docGetReadyState(self, doc):
        """ Gets the readyState of a document.  This is a seperate function so
            the "Access Denied" error that IE throws up every once in a while can
            be caught and ignored, without breaking the timing in the wait() functions.
            parameters:
                doc     - The document
            returns:
                The readyState.
        """
        try:
            return doc.readyState
        except:
            return ""
        
    
    def _frameWait(self, frame=None):
        """ Waits for a page to be fully loaded. A completely soundproof method has yet to be found to accomplish
            this, but the function works in the majority of instances. The function waits for both the doc busy attribute
            to be False and the doc readyState to be 'complete'.  It will continue to wait until the maximim timeOut
            value has been reached. In addition, the busyTuner can be adjusted to force the function to verify the
            specified number of consecutive 'not busy and completed' checks before continuing.
            parameters:
                [frame]     - A frame element.
            returns:
                True if the wait was successful, else False
        """
        readyCount = 0
        timeLeft = self._timeOut

        try:
            if frame:
                myFrame = frame
            else:
                myFrame = self.getFrame(self.frameName)

            while readyCount < self.busyTuner and timeLeft > 0:
                try:
                    doc = myFrame.document
                except:
                    continue     # if the document never gets itself together this will timeout

                if self._ie.Busy == False and self._docGetReadyState(doc) == 'complete':
                    readyCount += 1
                else:
                    readyCount = 0

                time.sleep(0.05)
                timeLeft -= 1
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return False
        else:
            return True
        
    def _wait(self):
        """ Waits for a page to be fully loaded. A completely soundproof method has yet to be found to accomplish
            this, but the function works in the majority of instances. The function waits for both the doc busy attribute
            to be False and the doc readyState to be 'complete'.  It will continue to wait until the maximim timeOut
            value has been reached. In addition, the busyTuner can be adjusted to force the function to verify the
            specified number of consecutive 'not busy and completed' checks before continuing.
            parameters:
                None
            returns:
                True if the wait was successful, else False
        """
        readyCount = 0
        timeLeft = self._timeOut

        try:
            while readyCount < self.busyTuner and timeLeft > 0:
                try:
                    doc = self._ie.Document
                except:
                    continue     # if the document never gets itself together this will timeout

                if self._ie.Busy == False and self._docGetReadyState(doc) == 'complete':
                    readyCount += 1
                else:
                    readyCount = 0

                time.sleep(0.05)
                timeLeft -= 1
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return False
        else:
            return True
        

    def buttonExists(self, name):
        """ Checks to see if a button exists
            parameters:
                name   - The id, name, value or index of the button.
            returns:
                True if the button is found, else False
        """
        myElement = self.getButton(name)
        if myElement:
            return True
        else:
            return False

    def changeWindow(self, wintext):
        """  changeWindow()
        changes control to new or existing window
        Parms:
            wintext - title of window to control
        """
        # Grab the POP-UP Window
        newWin = self.windowFind(wintext)

        # Use Pamie for COM object for POP-UP Window
        self._ie = newWin
        return self._ie
      

    def checkBoxExists(self, name):
        """ Checks to see if a checkbox exists
            parameters:
                name   - The id, name, or value of the button.
            returns:
                True if the checkbox is found, else False
        """
        myElement = self.getCheckBox(name)
        if myElement:
            return True
        else:
            return False

    def clickButton(self, name):
        """ Clicks a button
            parameters:
                name        - The id, name, value or index of the button, or a button element.
            returns:
                True on success, else False
        """
        if isinstance(name, str) or isinstance(name, int):
            myButton = self.getButton(name)
        else:
            myButton = name

        return self.clickElement(myButton)

    def clickButtonImage(self, name):
        """ Click a button of input type "image"
            parameters:
                name   - The id, name, value or index of the button, or a button element.
            returns:
                True on success, else False
        """
        if isinstance(name, str) or isinstance(name, int):
            myElements = self.getElementsList("input", "type=image")
            foundElement = self.findElement("input", "id;name;value", name, myElements)
        else:
            foundElement = name

        return self.clickElement(foundElement)

    def clickElement(self, element):
        """ Clicks the passed element
            parameters:
                element       - the element to click
            returns:
                True on success, else False
        """
        try:
            if not element:
                if self.showDebugging: print ("** clickElement() was not passed a valid element")
                return False
            
            if self.colorHighlight: element.style.backgroundColor=self.colorHighlight
            element.focus()
            element.blur()
            element.click()
            return True
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return False
        else:
            return False

    def clickHiddenElement(self, element):
     
        """ Clicks the passed element
            parameters:
                element       - the element to click
            returns:
                True on success, else False
        """
        try:
            if not element:
                if self.showDebugging: print ("** clickElement() was not passed a valid element")
                return False
            
            if self.colorHighlight: element.style.backgroundColor=self.colorHighlight
            element.click()
            return True
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return False
        else:
            return False

    def clickHiddenLink(self, name):
        """ Clicks a hidden link.
            parameters:
                name   - The id or innerText of the link
            returns:
                True on success, else False
        """
        if isinstance(name, str) or isinstance(name, int):
            myLink = self.getLink(name)
        else:
            myLink = name
        return self.clickHiddenElement(myLink)

    def clickImage(self, name):
        """ Clicks an image
            parameters:
                name    The id, name, src or index of the image
            returns:
                True on success, else False
        """
        if isinstance(name, str) or isinstance(name, int):
            myImage = self.getImage(name)
        else:
            myImage = name
        return self.clickElement(myImage)
      

    def clickLink(self, name):
        """ Clicks a link.
            parameters:
                name   - The id or innerText of the link
            returns:
                True on success, else False
        """
        if isinstance(name, str) or isinstance(name, int):
            myLink = self.getLink(name)
        else:
            myLink = name
        return self.clickElement(myLink)

    def clickMenu(self, tag, className, controlname, event=None):
        """ Gets a div
            parameters:
                name   - The id, name, or index of the div
            returns:
                The div if found, else None
        """
        self._wait()
        try:
            doc = self._ie.Document.getElementsByTagName(tag)
            for element in doc:
                if element is None:break
                if element.className == className :
                   if element.id == name:
                    element.style.backgroundColor="cyan"
                    element.FireEvent(tag, controlname, event)
                    return True
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return None      
    
    
    def closeWindow(self, title=None):
        try:
            self._ie.Close()
            return True
        except:
            return False
         
    def divExists(self, name):
        """ Checks to see if a div exists
            parameters:
                name   - The id, name, or index of the button.
            returns:
                True if the div is found, else False
        """
        myElement = self.getDiv(name)
        if myElement:
            return True
        else:
            return False

    def elementExists(self, tag, att, val):
        """ Checks to see if an element exists.
            parameters:
                tag             - The HTML tag name
                att             - The tag attribute to search for
                val             - The attribute value to match
            returns:
                True if the element exists, else False
        """ 
        foundElement = self.findElement(tag, att, val)
        if foundElement == None:
            return False
        else:
            return True
    
    def getPageTextModify(self):
        self._wait() 
        try:
            doc = self._ie.Document
            pw = doc.parentWindow
            return self.pageGetText()
        except: 
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print 'GetPage'
            print (sys.exc_info())
            print self.pageGetText()
            traceback.print_exc(ErrorTB)
            return None
        
    def executeJavaScript_Get(self, name,objvalue=None,strassert=None):
        self._wait() 
        try:
            doc = self._ie.Document
            pw = doc.parentWindow
            return self.pageGetText()
        except: 
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print 'JavaError'
            print (sys.exc_info())
            print self.pageGetText()
            traceback.print_exc(ErrorTB)
            return None
        
    
    def executeJavaScript(self, name,objvalue=None,strassert=None):
        """ Executes a java script function
            parameters:
                name  - The name of the javascript function
            returns:
                True on success, else False
        """
        self._wait() 
        try:
            doc = self._ie.Document
            pw = doc.parentWindow
            script = name
            print ("script:"),script
            print self.pageGetText()
            print 'JavaOk'
            pw.execScript(script) 
            return True
        except: 
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print 'JavaError'
            print (sys.exc_info())
            print self.pageGetText()
            traceback.print_exc(ErrorTB)
            return False
            #sys.exit(2)
            #return False
        
            

    def findElement(self, tag, attributes, val, elementList=None):
        """ The main find function that hunts down an element on the page according
            to the specified parameters.  Tries to take into account class
            specified frames or forms.
            parameters:
                tag             - The HTML tag name.
                attributes      - The semi-colon seperated tag attribute to search for.
                val             - The attribute value to match.  Regular Expressions
                                  can be used by starting the val with an !
                [elementList]   - Find the element in the passed list.
            returns:
                The found element
        """ 
##        try:
        self._wait()
        atts = attributes.split(";")
        regEx = False

        if isinstance(val, str):
            if val[0] == "!":
                val = val.replace( "!", "", 1)
                myRE = re.compile(val)
                regEx = True
        
        if elementList:
            if tag:
                elements = self.getElementsList(tag, "tagName=" + tag, elementList)
                
            if isinstance(val, int):        # Do we want the index?
                return elements[val]
        else:
            elements = self.getElementsList(tag)
            
        for el in elements[:]:
            if regEx:
                for att in atts[:]:
                    valText = el.getAttribute(att)
                    if valText != None:
                        m = myRE.match(valText)
                        if m:
                            return el
            else:
                for att in atts[:]:
                    valText = el.getAttribute(att)
                    if valText != None:
                        if isinstance(valText, str):
                            valText = valText.strip()
                            
                        if valText == val:
                            return el

        if self.showDebugging: print ("** findElement() did not find " + tag + "-" + attributes + "-" + str(val))
        return None

    def findElementByIndex(self, tag, indexNum, filter=None, elementList=None):
        """ Find a specific element based on tag and the index number.
            parameters:
                tag             - The HTML tag name
                indexNum        - The index number of the element
                attributes      - The semi-colon seperated tag attribute to search for
                val             - The attribute value to match
                [elementList]   - Find the element in the passed list
            returns:
                The found element
        """ 
        try:
            myElements = self.getElementsList(tag, filter=None, elementList=None)
            return myElements[indexNum]
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return None
        else:
            return None

    def findText(self, text):
        """
            Searches for text on the Web Page
            parameters:
                text - text to search for
        """
        self._wait()
        pageText = self.outerHTML()
        #print pageText
        
        # Search the doc for the text    
        text_found = pageText.find(text)
        try:
            # A "-1" means nothing is found
            if text_found is not -1:
                return True
            else:
                print ("Text %s Not Found!" %(text))
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return None

    def fireElementEvent(self, tag, controlName, eventName):
        """ Fire a named event for a given control
            parameters:
                tag         - The HTML tag name
                controlName - the control to act on
                eventName   - the event name to signal
            returns:
                True on success, else False
        """
        foundElement = self.findElement(tag, "name", controlName)
        if foundElement:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            foundElement.FireEvent(eventName)
            return True
        else:
            if self.showDebugging: print ("fireEvent() did not find " + controlName + " control.")
            return False

    def findWindow(self, title, indexNum=1):
        """ Finds all ie open windows returns them if title matches.
        parameters:
            title         - The window title to find
            [indexNum]    - The index number of the window to find
        returns:
            The window if found, else None
        """
        thisCount = self._timeOut
        found = False
        while not found:
            shellWnd = win32com.client.DispatchEx('Shell.Application')
            wins = shellWnd.Windows()
            winsCount = wins.Count
            print 'winsCount:',winsCount
            indexCnt = 1

            time.sleep(.5)
            thisCount = thisCount - 5
            if thisCount < 1: break

            for index in range(winsCount):
                try:
                    ieObj = wins.Item(index)
                    doc = ieObj.Document
                    
                    if doc.title == title:
                        if indexCnt == indexNum:
                            return ieObj
                        indexCnt += 1
                    elif ieObj.LocationName == title:
                        if indexCnt == indexNum:
                            return ieObj
                        indexCnt += 1
                except:
                    pass

        if self.showDebugging: print ("** windowFind() did not find the " + title + "-" + str(indexNum) + " window.")
        return None
      

    def formExists(self, name):
        """ Checks to see if a form exists
            parameters:
                None
            returns:
                True if the form is found, else False
        """
        myElement = self.getForm(name)
        if myElement:
            return True
        else:
            return False

    def frameExists(self, name):
        """ Checks to see if a frame exists
            parameters:
                name   - The id or name of the frame
            returns:
                True if the frame is found, else False
        """
        self._wait()
        
        try:
            frames = self._ie.Document.frames
            for i in range(frames.length):
                if frames[i].name == name:
                    return True
            return False
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return False
        else:
            return False         

    def getBodyValue(self, attribute):
        """ Gets the value of an attribute on the document.
            parameters:
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
            examples:
                val = getBodyValue("id")
        """
        self._wait() 
        if self.frameName:
            myDoc = self._ie.Document.frames[self.frameName].Document.body 
        else:
            myDoc = self._ie.Document.body 
        
        return self.getElementValue(myDoc, attribute)         

    def getButton(self, name):
        """ Gets a button
            parameters:
                name   - The id, name, value or index of the button.
            returns:
                The button if found, else None
        """
        myElements = self.getElementsList("input", "type=submit;type=button")

        if isinstance(name, int):
            foundElement = self.findElementByIndex("input", name, None, myElements)
        else:
            foundElement = self.findElement("input", "id;name;value", name, myElements)
        
        if foundElement == None:
            if self.showDebugging: print ("** getButton() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement

    def getButtonValue(self, name, attribute):
        """ Gets the value of an attribute on a button
            parameters:
                name        - The id, name, value or index of the button, or a button element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.getButton(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print ("** getButtonValue() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.getElementValue(foundElement, attribute)


    def getButtons(self, filter=None):
        """ Gets all the buttons
            parameters:
                [filter]    - Get only buttons specified by the filter
            returns:
                A list of buttons
        """
        if filter:
            filter = "type=submit;" + filter
        else:
            filter = "type=submit"
        return self.getElementsList("input", filter)

    def getButtonsValue(self, attribute, filter=None):
        """ Gets a list of values for the specified attribute
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only buttons specified by the filter
            returns:
                A list of the specified value of the attribute
        """
        myValues=[]
        myButtons = self.getButtons()
        for button in myButtons[:]:
            myValues.append(button.getAttribute(attribute))
        return myValues

    def getCheckBox(self, name):
        """ Gets a checkbox
            parameters:
                name   - The id, name, or value of the checkbox.
            returns:
                The checkbox if found, else None
        """
        myElements = self.getElementsList("input", "type=checkbox")
        foundElement = self.findElement("input", "id;name;value", name, myElements)
        if foundElement == None:
            if self.showDebugging: print ("** getCheckBox() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement
        
    def getCheckBoxValue(self, name, attribute):
        """ Gets a checkbox
            parameters:
                name        - The id, name, or value of the checkbox, or a checkbox element.
                attribute   - The name of the attribute to get the value for
            returns:
                The checkbox if found, else None
        """
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.getCheckBox(name)
        else:
            foundElement = name
        
        if foundElement == None:
            if self.showDebugging: print ("** getCheckBoxValue() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.getElementValue(foundElement, attribute)

   
    def getCheckBoxes(self, filter=None):
        """ Gets all the checkboxes
            parameters:
                [filter]    - Get only checkboxes specified by the filter
            returns:
                A list of checkboxes
        """
        print '****************************getCheckBoxesfilter:',filter
        if filter:
            filter = "type=checkbox;" + filter
        else:
            filter = "type=checkbox"
        return self.getElementsList("input", filter)

    def getCheckBoxesChecked_Cykj_onu(self,name,StringFlag):
        list_check = self.getCheckBoxes("type=checkbox;name=" + name)
        cmp_str =''
        if self.getElementValue(list_check[string.atoi(re.findall('\d',name)[0])-1],'checked')==True:
            cmp_str='TRUE'
        else:
            cmp_str='FALSE'
        if cmp_str==StringFlag.upper():
            return True
        else:
            return False
        
    def getCheckBoxesChecked(self, name):
        """ Gets a list of checked checkbox values for a specified checkbox name
            parameters:
                name - checkbox name
            returns:
                A list of checked values for the checkbox group
        """
        return self.getCheckBoxes("type=checkbox;checked=True;name=" + name)
    
    def getCheckBoxesValue(self, attribute, filter=None):
        """ Gets the value of an attribute for all the checkboxes
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only checkboxes specified by the filter
            returns:
                A list of the specified value of the attribute
        """
        myValues=[]
        myCheckBoxes = self.getCheckBoxes()
        for checkbox in myCheckBoxes[:]:
            myValues.append(checkbox.getAttribute(attribute))
        return myValues

    def getConfig(self,cfpath):
       """ Set the config path"""
       
       pathname = os.path.dirname(sys.argv[0])        
       pathname = os.chdir('..')
       path = os.path.abspath(pathname) 
       path = path + cfpath
       return path 


    def getCookie(self):
        """ Gets the Cookie information for the current page
            parameters:
                None
            returns:
                The Cookie information of the current page
        """
        self._wait() 
        return self._ie.Document.cookie
        
    def getDiv(self, name):
        """ Gets a div
            parameters:
                name   - The id, name, or index of the div
            returns:
                The div if found, else None
        """
        if isinstance(name, int):
            foundElement = self.findElementByIndex("div", name)
        else:
            foundElement = self.findElement("div", "id;name", name)

        if foundElement == None:
            if self.showDebugging: print ("** getDiv() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement

    def getDivValue(self, name, attribute):
        """ Gets the value of an attribute on a div.
            parameters:
                name        - The id, name, or index of the div, or a div element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.getDiv(name)
        else:
            foundElement = name
            
        if foundElement == None:
            if self.showDebugging: print ("** getDivValue() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.getElementValue(foundElement, attribute)

    def getDivs(self, filter=None):
        """ Gets a list of divs
            parameters:
                [filter]    - Get only buttons specified by the filter
            returns:
                A list of divs
        """
        return self.getElementsList("div", filter)
            
    def getDivsValue(self, attribute, filter=None):
        """ Gets a list of values for the specified attribute.
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only divs specified by the filter
            returns:
                A list of images
        """
        myValues=[]
        myDivs = self.getDivs(filter)
        for div in myDivs[:]:
            myValues.append(div.getAttribute(attribute))
        return myValues
                
    def getElementChildren(self, element, all=True):
        """ Gets a list of children for the specified element
            parameters:
                element       - The element
                elementList   - The attribute name
                [all]         - True gets all descendants, False gets direct children only
            returns:
                The value of the attribute.
        """         
        try:
            count = 0
            myElements = []
            if all:
                elements = element.all
            else:
                elements = element.childNodes

            while count < elements.length:
                myElements.append(elements[count])
                count +=1
            
            return myElements
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return None
        else:
            return None
        
    def getElementParent(self, element):
        """ Gets the parent of the passed element.
            parameters:
                element       - The element
            returns:
                The parent element
        """         
        try:
            return element.parentElement
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return None
        else:
            return None
       
    def getElementValue(self, element, attribute):
        """ Gets the value of the attribute from the element.
            parameters:
                element       - The element
                elementList   - The attribute name
            returns:
                The value of the attribute.
        """         
        try:
            return element.getAttribute(attribute)
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return None
        else:
            return None
        
    
    def button_clicktagkeyword(self,parent_tag,keyword,Level='0'):
        print parent_tag,keyword
        Element = self.find_getElement_List(parent_tag,keyword,Level)
        if Element==None:
            return False
        else:
            return self.clickElement(Element)
        
    '''
    def elementClick(self, element):
        """ Clicks the passed element
            parameters:
                element       - the element to click
            returns:
                True on success, else False
        """
        try:
            if not element:
                if self.showDebugging: print "** elementClick() was not passed a valid element"
                return False
            
            if self.colorHighlight: element.style.backgroundColor=self.colorHighlight
            element.focus()
            element.blur()
            element.click()
            return True
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return False
        else:
            return False
    '''
    def find_getElement_List(self,parent_tag,keyword,Level='0',filter=None,elementList=None):
        Element_list = self.getElementsList(parent_tag)
        #print 'Element_list:',Element_list
        #time.sleep(40)
        find_Flag = False
        for x in Element_list:
            try:
                tmp_node = x
                tmp_num = 0 
                while True:
                    #print 'tmp_node.nodeType:',tmp_node.nodeType
                    #print time.sleep(10)
                    if tmp_node.nodeType == 3:
                        if tmp_node.nodeValue == keyword:
                            find_Flag = True
                        break
                    else:
                        tmp_node = tmp_node.childNodes[0]
                    if string.atoi(Level)==0:
                        continue
                    tmp_num +=1
                    if tmp_num> string.atoi(Level):
                        break
                if find_Flag == True:
                    return x
            except Exception,e:
                print 'Not find the tag:%s ,keyword:%s'%parent_tag%keyword
                return None
                
        
    def getElementsList(self, tag, filter=None, elementList=None):
        """ Sets the specified attribute of any element
            parameters:
                tag        - The HTML tag name
                [filter]   - Only return elements that match this filter in format
                             (att1=val1;att2=val2), ie. "type=checkbox;checked=True"
            returns:
                A filtered list of the found elements
        """ 
        self._wait()

        if elementList:
            allElements = elementList
        else:
            if self.frameName:
                myFrame = self.getFrame(self.frameName) 
                
                if self.formName:
                    elements = myFrame.Document.forms[self.formName].getElementsByTagName(tag)
                else:
                    elements = myFrame.Document.getElementsByTagName(tag)
            else:
                if self.formName:
                    elements = self._ie.Document.forms[self.formName].getElementsByTagName(tag)
                else:
                    elements = self._ie.Document.getElementsByTagName(tag)
                    
            # Convert the IE COM object to a list
            count = 0
            allElements = []
            while count < elements.length:
                allElements.append(elements[count])
                count +=1

        try:
            if filter:
                myElements = []
                filters = filter.split(";")
                for el in allElements:
                    match = False 
                    for f in filters[:]:
                        atts = f.split("=")
                        valText = el.getAttribute(atts[0])
                        if valText != None:
                            valText = str(valText)
                            valText = valText.strip()
                            valText = valText.lower()
                            wantText = atts[1].lower()
                            if valText == wantText:
                                match = True
                    if match:
                        myElements.append(el)
            else:
                myElements = allElements
                
            return myElements
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return None
        else:
            return None
        

    def getErrorText(self, className):
        """ Gets the Error Text
        This is only an example you may need to tweak for you needs
            parameters:
                redTxtSmall   - This is the class name for the error text
            returns:
                The the innerText of that class, else None
        """
        pass
      
##      EXAMPLE Below
##        self._wait()
##        className = className
##        try:
##            doc = self._ie.Document.getElementsByTagName("SPAN")
##            for element in doc:
##                if element is None:break
##                if element.className == className :
##                    element.style.backgroundColor="cyan"
##                    val = element.innertext
##                    # stripout any spaces
##                    val = val.strip()
##                    return val
##        except:
##            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
##            print (sys.exc_info())
##            traceback.print_exc(ErrorTB)
##            return None
     
    def getForm(self, name=None):
        """ Gets a form
            parameters:
                [name]    - The name, id or index of the form.
            returns:
                The form if found, else None
        """
        if name == None: name = self.formName 
        if isinstance(name, int):
            foundElement = self.findElementByIndex("form", name)
        else:
            foundElement = self.findElement("form", "id;name", name)
        
        if foundElement == None:
            if self.showDebugging: print ("** getForm() did not find " + name)
            return None
        else:
            return foundElement

    def getFormControlNames(self, name=None): 
        """ Gets a list of controls for a given form
            parameters:
                [name]   - the form name
            returns:
                a list of control names located in the form
        """
        if name == None: name = self.formName 
        self._wait()
        d=[]
        if self.frameName:
            self._frameWait()
            thisForm = self._ie.Document.frames[self.frameName].Document.forms[self.formName]
        else:            
            thisForm = self._ie.Document.forms[self.formName]
        if thisForm!= None:
            for control in thisForm:
                if control == None: break        # Some browser bug
                d.append(control.name)
        return d
    
    def getFormValue(self, name, attribute):
        """ Gets the value of an attribute on a form
            parameters:
                name        - The id, name or index of the form, or a form element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if name == None: name = self.formName 
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.getForm(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print ("** getFormValue() did not find " + name)
            return None
        else:
            return self.getElementValue(foundElement, attribute)

    def getFormVisibleControlNames(self, name=None):
        """ Gets a list of controls for a given form
            parameters:
                [name]   - the form name
            returns:
                a list of visible control names located in the form
        """
        if name == None: name = self.formName 
        self._wait()
        d=[]
        if self.frameName:
            thisForm = self._ie.Document.frames[self.frameName].Document.forms[self.formName]
        else:            
            thisForm = self._ie.Document.forms[self.formName]
        if thisForm!= None:
            for control in thisForm:
                if control == None: break        #some browser bug
                if control.type != 'hidden':
                    if control.id == None or control.id == '':
                        d.append(control.name)
                    else:
                        d.append(control.id)
        return d
    

    def getForms(self, filter=None):
        """ Gets a list of forms
            parameters:
                [filter]    - Get only buttons specified by the filter
            returns:
                A list of forms
        """
        return self.getElementsList("form", filter)

    def getFormsValue(self, attribute, filter=None):
        """ Use this to get the form object names on the page
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only forms specified by the filter
            returns:
                a list of form names
        """
        myValues=[]
        myForms = self.getForms(filter)
        for form in myForms[:]:
            myValues.append(form.getAttribute(attribute))
        return myValues
        
        
    def getFrame(self, name):
        """ Gets a a frame
            parameters:
                name  - The name or index of the frame
            returns:
                a frame element
        """
        self._wait()
        frames = self._ie.Document.frames
        destFrames = name.split(".")
        
        if isinstance(name, int):
            return frames[name]
        else:
            j = 0
            for destFrame in destFrames:
                j += 1
                for i in range(frames.length):
                    fName = frames[i].name
                    if fName == destFrame:
                        if j == len(destFrames):
                            myFrame = frames[i]
                            self._frameWait(myFrame)
                            return myFrame
                        else:
                            frames = frames[i].document.frames
            return None

    def getFrameValue(self, name, attribute):
        """ Gets the value of an attribute on a frame
            parameters:
                name        - The name of the frame
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        foundElement = self.getFrame(name)
        if foundElement == None:
            if self.showDebugging: print ("** getFrameValue() did not find " + name)
            return None
        else:
            return foundElement.name # can't call getElementValue() here

    def getFramesValue(self):
        """ Gets the value of an attribute on a frame
            parameters:
                none
            returns:
                The list of frame values
        """
        self._wait()
        l=[]
        frames = self._ie.Document.frames
        for i in range(frames.length):
            l.append(frames[i].name)    # can't call getAttribute() here
        return l
        
      
    
    def getIE(self):
        """ Get the current IE Application
            parameters:
                None
            returns:
                The current IE document
        """
        return self._ie

    def getImage(self, name):
        """ Gets an image
            parameters:
                name  - The id, name, src or index of the image
            returns:
                an image
        """
        if isinstance(name, int):
            foundElement = self.findElementByIndex("img", name)
        else:
            foundElement = self.findElement("img", "id;name;nameProp;src", name)
                
        if foundElement == None:
            if self.showDebugging: print ("** getImage() did not find " + str(name))
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement

    def getImageValue(self, name, attribute):
        """ Gets the value of an attribute on a image
            parameters:
                name        - The id, name, value or index of the image, or image element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.getImage(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print ("** getImageValue() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.getElementValue(foundElement, attribute)

    def getImages(self, filter=None):
        """ Gets a list of images
            parameters:
                [filter]    - Get only buttons specified by the filter
            returns:
                A list of images
        """
        return self.getElementsList("img", filter)


    def getImagesValue_CYKJ_onu(self,Name,Findstr,attribute='src',filter=None):
        list_Image = self.getImagesValue(attribute,filter)
        Result = list_Image[string.atoi(Name)-1]
        print 'GetImageResult:',Result
        if Result.upper().find(Findstr.upper())>-1:
            return True
        else:
            return False
                
    def getImagesValue(self, attribute, filter=None):
        """ Gets a list of the specified value for the images
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only images specified by the filter
            returns:
                A list of image values.
        """
        myValues=[]
        myImages = self.getImages(filter)
        for image in myImages[:]:
            myValues.append(image.getAttribute(attribute))
        return myValues

    def getInputElements(self, filter=None):
        """ Get all the input elements
            parameters:
                [filter]    - Get only buttons specified by the filter
            returns:
                A list of input elements
        """
        return self.getElementsList("input", filter)

      
    def getLink(self, name):
        """ Gets a link
            parameters:
                name  - The id, innerText or index of the link
            returns:
                an image
        """
        if isinstance(name, int):
            foundElement = self.findElementByIndex("a", name)
        else:
            foundElement = self.findElement("a", "id;innerText", name)
        
        if foundElement == None:
            if self.showDebugging: print ("** getLink() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement
        

    def getLinkValue(self, name, attribute):
        """ Gets the value of an attribute on a link
            parameters:
                name        - The id, innerText or index of the link, or a link element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.getLink(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print ("** getLinkValue() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.getElementValue(foundElement, attribute)

    def getLinks(self, filter=None):
        """ Gets a list of links
            parameters:
                [filter]    - Get only links specified by the filter
            returns:
                A list of links
        """
        return self.getElementsList("a", filter)
    
    def getLinksValue(self, attribute, filter=None):
        """ Gets a list of the specified value for the links
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only links specified by the filter
            returns:
                A list of link values.
        """
        myValues=[]
        myLinks = self.getLinks(filter)
        for link in myLinks[:]:
            myValues.append(link.getAttribute(attribute))
        return myValues
    
      
    def getListBox(self, name):
        """ Gets a list box.
            parameters:
                name    - The name or index of the listbox
            returns:
                A list box
        """
        if isinstance(name, int):
            foundElement = self.findElementByIndex("select", name)
        else:
            foundElement = self.findElement("select", "name;id", name)

        if foundElement == None:
            if self.showDebugging: print ("** getListBox() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement

    def getListBoxItemCount(self,name):
        """ Gets a count of selected options associated with a listbox.
            parameters:
                The name or id of the list box
            returns:
                The selected text
        """
        foundElement = self.findElement("select", "name;id", name)
        if foundElement == None:
            if self.showDebugging: print ("** getListBoxSelected() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            myValues = []
            
            myElements = foundElement.options
            count = 0
            while count < myElements.length:
                count += 1
            return count         

    def getListBoxOptions(self, name):
        """ Gets the list of options associated with a listbox.
            parameters:
                The name or id of the list box
            returns:
                A list of options
        """
        foundElement = self.findElement("select", "name;id", name)
        if foundElement == None:
            if self.showDebugging: print ("** getListBoxOptions() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            myValues = []
            count = 0
            myElements = foundElement.options
            while count < myElements.length:
                myValues.append(myElements[count].innerText)
                count += 1
            return myValues

    def getListBoxSelected(self, name):
        """ Gets the list of selected options associated with a listbox.
            parameters:
                The name or id of the list box
            returns:
                The selected text
        """
        foundElement = self.findElement("select", "name;id", name)
        if foundElement == None:
            if self.showDebugging: print ("** getListBoxSelected() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            myValues = []
            
            myElements = foundElement.options
            count = 0
            while count < myElements.length:
                if myElements[count].selected:               
                    myValues.append(myElements[count].innerText)
                count += 1
            return myValues

    def getListBoxValue(self, name, attribute):
        """ Gets the value of an attribute on a listbox
            parameters:
                name        - The id, innerText or index of the listbox, or a listbox element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.getListBox(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print ("** getListBoxValue() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.getElementValue(foundElement, attribute)
        

    
        
    def getPageText(self):
        """ Gets the URL, Title and outerHTML
            parameters:
                None
            returns:
                a string consisting of:
                URL,
                Title
                Body block
            as a string. Unfortunately, IE doesn't give a workable solution to 
            saving the complete source so this is as good as it gets until
            someone brighter comes along.  This is useful if you want to compare
            against a previous run for QCing purposes.
        """
        self._wait() 
        if self.frameName:
            return '%s\n%s\n%s'%(self._ie.LocationURL,
                                 self._ie.LocationName,
                                 self._ie.Document.frames[self.frameName].document.body.outerHTML)
        else:
            return '%s\n%s\n%s'%(self._ie.LocationURL,
                                 self._ie.LocationName,
                                 self._ie.Document.body.outerHTML)        

                            
    def getRadioButton(self, name):
        """ Gets a radio button by the name.  If there are multiple radio buttons
            with the same name, the first one found is returned.
            parameters:
                name - radio button group name or index
            returns:
                a list values for the group
        """
        myElements = self.getElementsList("input", "type=radio")
        if isinstance(name, int):
            foundElement = self.findElementByIndex("input", name, None, myElements)
        else:
            foundElement = self.findElement("input", "name", name, myElements)

        if foundElement == None:
            if self.showDebugging: print ("** getRadioButton() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement
  
    def getRadioButtonSelected(self, name):
        """ Gets a list of selected radio button values for a Radio Button group
            parameters:
                name - radio button group name
            returns:
                a list of selected buttons from the group
        """
        myValues = []
        myElements = self.getElementsList("input", "type=radio;checked=True;name=" + name)
        for el in myElements[:]:
            myValues.append(el.value)
        return myValues
    
    def getRadioButtonValues(self, name):
        """ Gets a list of selected radio button values for a Radio Button group
            parameters:
                name - radio button group name
            returns:
                a list of selected buttons from the group
        """
        myValues = []
        myElements = self.getElementsList("input", "type=radio;checked=False;name=" + name)
        for el in myElements[:]:
            myValues.append(el.value)
        return myValues


    def getRadioButtons(self, filter=None):
        """ Gets all the radio buttons
            parameters:
                [filter]    - Get only radio buttons specified by the filter
            returns:
                A list of checkboxes
        """
        if filter:
            filter = "type=radio;" + filter
        else:
            filter = "type=radio"
        return self.getElementsList("input", filter)

    def getTable(self, name):
        """ Gets a table
            parameters:
                name  - The id or name of the table
            returns:
                a table
        """
        if isinstance(name, int):
            foundElement = self.findElementByIndex ("table", name, name)
        else:
            foundElement = self.findElement("table", "id;name", name)

        if foundElement == None:
            if self.showDebugging: print ("** getTable() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement
        
    def getTableData(self, name):
        """ Gets the data from a table
            parameters:
                name  - The id, name or index of the table, or a table element.
            returns:
                a string containing all the table data
        """
        if isinstance(name, str) or isinstance(name, int):
            myTable = self.getTable(name)
        else:
            myTable = name

        myCells = myTable.cells

        try:
            myData = ""
            lastIndex = -1
            for myCell in myCells:
                if myCell.cellIndex <= lastIndex: myData += "\n"
                myData += str(myCell.innerText.strip()) + " "
                lastIndex = myCell.cellIndex
            return myData
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return None
        else:   return None

    def getTableRowIndex(self, name, row):
        """ Gets the index of a row in a table.
            parameters:
                Name        - The id, name or index of the table
                row[]       - The row to search for. Use * to ignore cell.
            returns:
                index of the row if found
        """
        if isinstance(name, str) or isinstance(name, int):
            myTable = self.getTable(name)
        else:
            myTable = name
        myCells = myTable.cells

        try:
            myData = ""
            colIndex = 0
            cIndex = -1
            matches = True
            rowIndex = 0
            
            for myCell in myCells:
                if myCell.cellIndex <= cIndex:
                    if matches == True:
                        return rowIndex
                    else:
                        matches = True
                        rowIndex += 1
                    colIndex = 0
                    
                if row[colIndex] != "*":
                    foundVal = myCell.innerText.strip()
                    if foundVal != row[colIndex]:
                        matches = False

                cIndex = myCell.cellIndex
                colIndex += 1
            return matches
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return None
        else:   return None
        
        
    def getTableText_Cykj(self,tableNum,rownum,cellnum,frameName=None):
        self._wait()
        table = self._ie.Document.getElementsByTagName('table')
        print table
        return table
        
    def getTableText(self,tableName,rownum,cellnum, frameName=None):
        """ getTableData - returns data from a cell in a table
            parms:
                tableName - name of table
                rownum - row number
                cellnum - cell number       
        
        """
        self._wait() 
        table = self._ie.Document.getElementsByTagName('table')
        
        
        if table.length >0:    
            
            table[tableName].rows[rownum].cells[cellnum].style.backgroundColor= 'cyan'
            data = table[tableName].rows[rownum].cells[cellnum].innerText
            #print "Here:",data
            data = data.strip()# strip off any spaces 
            return data 
            #except: print "Failed not get the text from the Cell"
        else:
            print ("No Table Found")
            



        
    def getTables(self, filter=None):
        """ Gets a list of tables
            parameters:
                [filter]    - Get only tables specified by the filter
            returns:
                A list of tables
        """
        return self.getElementsList("table", filter)
    
    def getTextArea (self, name):
        """ Gets a text area.
            parameters:
                name    - The name, id or index of the textarea
            returns:
                The text area if found.
        """
        if isinstance(name, int):
            foundElement = self.findElementByIndex ("textarea", name)
        else:
            foundElement = self.findElement("textarea", "name;id", name)
      
        if foundElement == None:
            if self.showDebugging: print ("** getTextArea () did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement

    def getTextAreaValue(self, name, attribute):
        """ Gets the value of an attribute on a textarea
            parameters:
                name        - The id, name or index of the textarea, or a textarea element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.getTextArea (name)
        else:
            foundElement = name
            
        if foundElement == None:
            if self.showDebugging: print ("** getTextArea Value() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.getElementValue(foundElement, attribute)
        

    def getTextAreas(self, filter=None):
        """ Gets a list of textareas
            parameters:
                [filter]    - Get only textareas specified by the filter
            returns:
                A list of textareas
        """
        return self.getElementsList("textarea")

    def getTextAreasValue(self, attribute, filter=None):
        """ Gets a list of the specified value for the textareas
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only textareas specified by the filter
            returns:
                A list of link values.
        """
        myValues=[]
        myAreas = self.getTextAreas(filter)
        for area in myAreas[:]:
            myValues.append(area.getAttribute(attribute))
        return myValues
    

    def getTextBox(self, name):
        """ Gets a text box.
            parameters:
                name    - The name, id or index of the textbox
            returns:
                The text area if found.
        """
        if isinstance(name, int):
            foundElement = self.findElementByIndex("input", name)
        else:
            foundElement = self.findElement("input", "id;name;value", name)
        
        if foundElement == None:
            if self.showDebugging: print ("** getTextBox () did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement

    def getTextBoxValue(self, name, attribute):
        """ Gets the value of an attribute on a textbox
            parameters:
                name        - The id, name or index of the textbox, or a textbox element
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.getTextBox(name)
        else:
            foundElement = name
            
        if foundElement == None:
            if self.showDebugging: print ("** getTextBox Value() did not find " + name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.getElementValue(foundElement, attribute)


    def getTextBoxes(self, filter=None):
        """ Gets all the textboxes
            parameters:
                [filter]    - Get only textboxes specified by the filter
            returns:
                A list of textboxes
        """
        if filter:
            filter = "type=text;" + filter
        else:
            filter = "type=text"
        return self.getElementsList("input", filter)

    def getTextBoxesValue(self, attribute, filter=None):
        """ Gets a list of values for the specified attribute
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only textboxes specified by the filter
            returns:
                A list of the specified value of the attribute
        """
        myValues=[]
        myBoxes = self.getTextBoxes()
        for box in myBoxes[:]:
            myValues.append(box.getAttribute(attribute))
        return myValues

    def goBack(self):
        """
            Navigates backward one item in the history list
        """
        self._wait()
        self._ie.GoBack()


    def imageExists(self, name):
        """ Checks to see if a image exists in the HTML document.  It does not
            check to see if the image actually exists on the server.
            parameters:
                name   - The id, name, src or index of the image.
            returns:
                True if the image is found, else False
        """
        myElement = self.getImage(name)
        if myElement:
            return True
        else:
            return False

    def linkExists(self, name):
        """ Checks to see if a link exists
            parameters:
                name   - The id or innerText of the link.
            returns:
                True if the link is found, else False
        """
        myElement = self.getLink(name)
        if myElement:
            return True
        else:
            return False

    def listBoxUnSelect(self, name, value):
        """ Selects an item in a list box.
            parameters:
                name    - The name or id of the listbox
                value   - The value of the item to select in the list
            returns:
                True on success, else False
        """
        self._wait()
        foundElement = self.findElement("select", "name;id", name)
        if foundElement == None:
            if self.showDebugging: print ("** selectListBox() did not find " + name + "-" + str(value))
            return False
        else:
            for el in foundElement:
                if el.text == value:
                    if self.colorHighlight: el.style.backgroundColor=self.colorHighlight
                    el.selected = False
                    #foundElement.FireEvent("onChange")
                    bResult = True
            return True

    def locationName(self):
        """ Gets the location name of the current page. If the resource is an HTML page on the World Wide Web, the name is the title of that page.
            If the resource is a folder or file on the network or local computer, the name is the
            full path of the folder or file in Universal Naming Convention (UNC) format.
            
            **NOTE** If you have "Hide extensions for known file types" enabled, then of course that is not
            returned.
            parameters:
                None
            returns:
                The name of the location
        """
            
        self._wait()
        return self._ie.LocationName


    def locationURL(self):
        """ Gets the URL of the current page
            parameters:
                None
            returns:
                The URL of the page
        """
        self._wait() 
        return self._ie.LocationURL


    def navigate(self, url):
        """ Go to the specified URL.
            parameters:
                url - URL to navigate to
            returns:
                True on success, else False
        """
        try:
            self._wait() 
            self._ie.Navigate(url)
            return True
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return False

    def outerHTML(self):
        """ Gets the  outerHTML
            parameters:
                None
            returns:
                a string consisting of:
                Body block as a string.
        """
        self._wait() 
        
        if self.frameName:
            return '%s'%(self._ie.Document.frames[self.frameName].document.body.outerHTML)
        else:
            return '%s'%(self._ie.Document.body.outerHTML)

    def pause(self, string = "Click to Continue test"):
        """ Wait for the user to click a button to continue testing.
            parameters:
                [string]  = Message to display to user
            returns:
                None
        """
        self._wait()
        try:
           win32gui.MessageBox(0, string, "Pausing test...", 0)
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
        else:   return True         

    def quit(self):
        """ Quit the IE browser and close it.
            parameters:
                None
            returns:
                True on success, else False
        """
        self._wait()
        try:    self._ie.Quit()
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return False
        else:   return True      


    def randomDigits(self, length): 
        """ Creates a string of random digits.
            parameters:
                length  - The length of the number to be created
            returns:
                The string of random digits
        """
        a = "".join([random.choice(string.digits) for _ in range(length)])
        count = a.count(a)
        count = 0
        while count <= length:
            return ''.join(a)
        
    def randomString(self, length): 
        """ Creates a string of random upper and lower case characters
            parameters:
                length  - The length of the string to be created
            returns:
                The string of random characters
        """
        a = "".join([random.choice(string.letters) for _ in range(length)])
        count = a.count(a)
        count = 0
        while count <= length:
            return ''.join(a)
        
    def refresh(self):
        """ Refresh the current page in the broswer
            parameters:
                None
            returns:
                True on success, else False
        """
        self._wait()
        try:    self._ie.Refresh()
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return False
        else:   return True

    def resize(self, iWidth, iHeight):
    	"Resize the window"
    	self._ie.resizeTo(iWidth, iHeight)


    def selectListBox(self, name, value):
        """ Selects an item in a list box.
            parameters:
                name    - The name or id of the listbox
                value   - The value of the item to select in the list
            returns:
                True on success, else False
        """
        self._wait()
        foundElement = self.findElement("select", "name;id", name)
        if foundElement == None:
            if self.showDebugging: print ("** selectListBox() did not find " + name + "-" + str(value))
            return False
        else:
            for el in foundElement:
                if el.text == value:
                    if self.colorHighlight: el.style.backgroundColor=self.colorHighlight
                    el.selected = True
                    foundElement.FireEvent("onChange")
                    bResult = True
            return True

    def setCheckBox(self, name, value):
        """ Sets the value of a check box.
            parameters:
                name   - The id, name, or value of the checkbox.
                value  - 0 for false (not checked)
                         1 for true (checked)
            returns:
                True on success, else False
        """
        myElements = self.getElementsList("input", "type=checkbox")
        return self.setElement("input", "id;name;value", name, "checked", value, None, myElements)

      
    def setElement(self, tag, att, val, setAtt, setVal, element=None, elementList=None):
        """ Sets the specified attribute of any element
            parameters:
                tag             - The HTML tag name
                att             - The tag attribute to search for
                val             - The attribute value to match
                setAtt          - The attribute to set
                setVal          - The values you are setting
                [element]       - Specify a specific element
                [elementList]   - Find the element in the passed list
            returns:
                True on success, else False
        """ 
        if element:
            foundElement = element
        else:
            foundElement = self.findElement(tag, att, val, elementList)
            
        if foundElement == None:
            if self.showDebugging: print ("** setElement() did not find " + tag + "-" + att + "-" + str(val))
            return False
        else:
            try:
                if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
                foundElement.focus()
                foundElement.blur()
                foundElement.setAttribute(setAtt, setVal)
                return True
            except:
                (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
                print (sys.exc_info())
                traceback.print_exc(ErrorTB)
                return False
            else:
                return False

    def setRadioButton(self, name, value, checked=True):
        """ Sets a Radio Button value
            parameters:
                name        - radio button group name
                value       - Which item to pick by name
                [checked]   - Check the button, True or False
            returns:
                True on success, else False
        """
        #TODO: Find way to get innerText
        myElements = self.getElementsList("input", "type=radio;name=%s" % (name))
        for el in myElements[:]:
            if el.value == value:
                if self.colorHighlight: el.style.backgroundColor=self.colorHighlight
                el.checked = checked
                el.FireEvent("onClick")
                return True

        if self.showDebugging: print ("** setRadioButton() did not find %s" % (name))
        return False

    def setTextArea(self, name, value):
        """ Sets the text in a textarea.
            parameters:
                name    - The id, name or index of the text area, or a textarea element.
                value   - The value to set the text area to.
            returns:
                True on succes, else False
        """
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.findElement("textarea", "name;id", name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print ("** setTextArea() did not find " + name + "-" + str(value))
            return False
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            foundElement.value = value
            return True

    def setTextBox(self, name, value):
        """ Sets the text in a text box.
            parameters:
                name    - The id, name or index of a textbox, or a textbox element.
                value   - The value to set the textbox to.
            returns:
                True on succes, else False
        """
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.getTextBox(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print ("** setTextBox() did not find " + name + "-" + str(value))
            return False
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            foundElement.value = value
            return True

    def showAllTableText(self):
        """ verifies text in a table
        """
        self._wait() 
        # Get tags names table
        table = self._ie.Document.getElementsByTagName('table')
        
        # loop thru all the tables
        for i in range(table.length):
            tablecnt = 0
            errortxt = table[i].rows[0].cells[0].innerText
            tablecnt = i +1
            errortxt= errortxt.strip()
            print ("tableNum:%s and Text: %s" % (tablecnt, errortxt) ) 


    def showTableText(self,tableName,rownum,cellnum ):
        """ Print out table index and the innertext
        """
        
        self._wait() 
        table = self._ie.Document.getElementsByTagName('table')
        table[tableName].rows[rownum].cells[cellnum].style.backgroundColor= 'red'
        print (table[tableName].rows[rownum].cells[cellnum].innerText)
         
    def showlinkByIndex(self):
        
        links = self._ie.Document.links.length
        for i in range(links):
            print (i, self._ie.Document.links[i].innertext)


    def startTimer(self):
        """
            Start time for this timer
        """
        self.timer = datetime.datetime.now()

    def stop(self):
        """
            Cancels any in process navigation 
        """
        self._wait()
        self._ie.Stop()
      

    def stopTimer(self):
        """
            Stop timer and calc the time difference
        """
        # Wait is very important - wait for the doc to complete
        self._wait() 
        td = datetime.datetime.now() - self.timer
       

        # Calc in seconds, days, and microseconds
        # Change to seconds
        seconds = td.seconds + td.days*24*60*60

        # return time
        return 'Total time:%s - The time for this script to run was aprox. %s seconds' % (td, seconds)


    def submitForm(self, name=None):
        """ Submits a form. For proper testing you should submit a form as a user
            would, such as clicking the submit button.
            parameters:
                [name] - name of form
            returns:
                True on success, else False
        """
        try:
            if name == None: name = self.formName 
            foundElement = self.findElement("form", "id;name", name)
            if foundElement:
                foundElement.submit()
                return True
            else:
                if self.showDebugging: print ("** submitForm() did not find the " + name + " form")
                return False
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return False
        else:
            return True          

    def tableCellExists(self, tableName, cellText):
        """ Checks to see if a cell in a table exists
            parameters:
                tableName   - The id, name or index of the table, or a table element.
                cellText    - The cell text to search for
            returns:
                True if the table is found, else False
        """
        if isinstance(tableName, str) or isinstance(tableName, int):
            myTable = self.getTable(tableName)
        else:
            myTable = tableName
        myCells = myTable.cells

        try:
            myData = ""
            for myCell in myCells:
                if myCell.innerText.strip() == cellText:
                    return True
            return False
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print (sys.exc_info())
            traceback.print_exc(ErrorTB)
            return False
        else:   return False
        
    def tableExists(self, name):
        """ Checks to see if a table exists
            parameters:
                name   - The id or name of the table
            returns:
                True if the table is found, else False
        """
        myElement = self.getTable (name)
        if myElement:
            return True
        else:
            return False

    def tableRowExists(self, name, row):
        """ Checks to see if a row in a table exists
            parameters:
                Name        - The id, name or index of the table, or a table element.
                row[]       - The row to search for. Use * to ignore cell.
            returns:
                True if the table is found, else False
        """
        if self.getTableRowIndex (name, row):
            return True
        else:
            return False

    def textAreaExists(self, name):
        """ Checks to see if a textarea exists
            parameters:
                name   - The name, id or index of the textarea
            returns:
                True if the textarea is found, else False
        """
        myElement = self.getTextArea  (name)
        if myElement:
            return True
        else:
            return False         
         

    def textBoxExists(self, name):
        """ Checks to see if a textbox exists
            parameters:
                name   - The name or id of the textbox
            returns:
                True if the textbox is found, else False
        """
        myElement = self.getTextBox(name)
        if myElement:
            return True
        else:
            return False

    def textBoxValue(self, name):
        """ Sets the text in a text box.
            parameters:
                name    - The id, name or index of a textbox, or a textbox element.
                value   - The value to set the textbox to.
            returns:
                True on succes, else False
        """
        if isinstance(name, str) or isinstance(name, int):
            foundElement = self.getTextBox(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print ("** setTextBox() did not find " + name )
            return False
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            foundElement.value 
            return foundElement.value

    def textFinder(self,text):
        """
            Find text on a page then highlites it. It also returns a tru/false
        parameters:
            text    - text to search for
        """
        self._wait()
        
        rng = self._ie.Document.body.createTextRange();
        
        if rng.findText(text.strip())==True:
            rng.select()
            rng.scrollIntoView()
            return True
        else:
            return False        



      
    ##  New Stuff as of Dec 2006
    def writeAttrs(self):
        """ WriteScript - Writes out a element attrs.
            
            Parmeters:
                frmName - form name
                frameName - frame name defaults to none
        """
        
        self._wait()
        items = ["input", "select"]
        for i in items:
                        
            doc = self._ie.Document.getElementsByTagName(i)
                
            for i in range(doc.length):
                x = doc[i] 
                etype = getattr(x,"type")
                # Check for Name, ID or value
                name = getattr(x,"name",None)  
                id = getattr(x,"id",None)
                value = getattr(x,"value",None) 
                
                if etype ==  "select-one":
                    print ("Type:%s, ID:%s, Value:%s" % (etype,name,value) )
                
                elif etype ==  "select-multiple":
                    print ("Type:%s, ID:%s, Value:%s" % (etype,name,value))
                
                else:
                    print ("Type:%s, ID:%s, Value:%s" % (etype,name,value))

    def searchKeyword(self,keyword):
        #self=PAMIE(url)
        text_string=self.getPageText()
        pagetext=text_string.encode('gb18030')
        keyword=keyword.encode('gb18030')
        p=re.compile(keyword)
        if p.search(pagetext):
            #print pagetext
            print 'Success! there is '+keyword+' exist.'
            #log_print(msg)
            #print p.search(pagetext)
            return True
        else:
            #print pagetext
            print 'Fail! the keyword '+keyword+' is not exist.'
            #log_print (msg)
            return False
        
