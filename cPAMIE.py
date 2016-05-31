""" 
cPAMIE Build 2.0
Based on PAM.py by RLM
Revised: Feb 13th 2006
Developers: Robert L. Marchetti, Drunk Bum
Description: This python class file allow you to write scripts to Automate the Internet Explorer Browser Client.

Licence: GNU General Public License (GPL)
This software is provided 'as-is', without any express or implied warranty.
In no event will the authors be held liable for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not claim that you wrote the original software.
   If you use this software in a product, an acknowledgment in the product documentation would be appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.

Special Thanks to: All the Pamie Users, Steve M., Drunk Bum, Jeff H., Dave K., Henry W., Tom C., Scott W.,
Margie M. and all others for there support and contributions.  See !whatsnew.txt for modification history.
"""

import sys
sys.path.append(r'c:\python27\lib')

from win32com.client import DispatchEx
import win32gui
import pywintypes
import time
import win32con
import pdb
import re
import random
import string
import pythoncom
import datetime
import traceback

class PAMIE:
    """
    cPAMIE is an automation object based on the work of PAMIE by RLM
    http://pamie.sourceforge.net/
    """
    __version__ = "2.0"

    def __init__(self, url=None, timeOut=300):
        """ The class instantiation code. When the object is instantiated you can
        pass a starting URL. If no URL is passed then about:blank, a blank
        page, is brought up.
        parameters:
            [url]     - url to navigate to initially
            [timeOut] - how many 100mS increments to wait, 10 = 1sec, 100=10sec
        returns:
            Nothing
        """
        self.showDebugging = True           # Show debug print lines?
        self.colorHighlight = "#F6F7AD"     # Set to None to turn off highlighting
        self.frameName = None               # The current frame name or index. Nested frames are
                                            # supported in the format frame1.frame2.frame3
        self.formName = None                # The current form name or index
        self.busyTuner = 1                  # Number of consecutive checks to verify document is no longer busy.

        self._ie = DispatchEx('InternetExplorer.Application')
        if url:
            self._ie.Navigate(url)
        else:
            self._ie.Navigate('about:blank')
          
        self._timeOut = timeOut
        self._ie.Visible = 1
        self.timer = datetime.datetime.now()


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
                myFrame = self.frameGet (self.frameName)

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
            print sys.exc_info()
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
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return False
        else:
            return True
        
    def bodyGetValue(self, attribute):
        """ Gets the value of an attribute on the document.
            parameters:
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
            examples:
                val = bodyGetValue ("id")
        """
        self._wait() 
        if self.frameName:
            myDoc = self._ie.Document.frames[self.frameName].Document.body 
        else:
            myDoc = self._ie.Document.body 
        
        return self.elementGetValue (myDoc, attribute)

    def buttonClick(self, name):
        """ Clicks a button
            parameters:
                name        - The id, name, value or index of the button, or a button element.
            returns:
                True on success, else False
        """
        if isinstance(name, basestring) or isinstance(name, int):
            myButton = self.buttonGet(name)
        else:
            myButton = name

        return self.elementClick(myButton)

    def buttonExists(self, name):
        """ Checks to see if a button exists
            parameters:
                name   - The id, name, value or index of the button.
            returns:
                True if the button is found, else False
        """
        myElement = self.buttonGet (name)
        if myElement:
            return True
        else:
            return False

    def buttonGet(self, name):
        """ Gets a button
            parameters:
                name   - The id, name, value or index of the button.
            returns:
                The button if found, else None
        """
        myElements = self.elementsGetList ("input", "type=submit;type=button")

        if isinstance(name, int):
            foundElement = self.elementFindByIndex ("input", name, None, myElements)
        else:
            foundElement = self.elementFind ("input", "id;name;value", name, myElements)
        
        if foundElement == None:
            if self.showDebugging: print "** buttonGet() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement

    def buttonGetValue(self, name, attribute):
        """ Gets the value of an attribute on a button
            parameters:
                name        - The id, name, value or index of the button, or a button element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, basestring) or isinstance(name, int):
            foundElement = self.buttonGet(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print "** buttonGetValue() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.elementGetValue (foundElement, attribute)

    def buttonImageClick(self, name):
        """ Click a button of input type "image"
            parameters:
                name   - The id, name, value or index of the button, or a button element.
            returns:
                True on success, else False
        """
        if isinstance(name, basestring) or isinstance(name, int):
            myElements = self.elementsGetList ("input", "type=image")
            foundElement = self.elementFind ("input", "id;name;value", name, myElements)
        else:
            foundElement = name

        return self.elementClick (foundElement)
       
    def buttonsGet(self, filter=None):
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
        return self.elementsGetList ("input", filter)

    def buttonsGetValue(self, attribute, filter=None):
        """ Gets a list of values for the specified attribute
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only buttons specified by the filter
            returns:
                A list of the specified value of the attribute
        """
        myValues=[]
        myButtons = self.buttonsGet()
        for button in myButtons[:]:
            myValues.append (button.getAttribute(attribute))
        return myValues

    def checkBoxExists(self, name):
        """ Checks to see if a checkbox exists
            parameters:
                name   - The id, name, or value of the button.
            returns:
                True if the checkbox is found, else False
        """
        myElement = self.checkBoxGet (name)
        if myElement:
            return True
        else:
            return False

    def checkBoxGet(self, name):
        """ Gets a checkbox
            parameters:
                name   - The id, name, or value of the checkbox.
            returns:
                The checkbox if found, else None
        """
        myElements = self.elementsGetList ("input", "type=checkbox")
        foundElement = self.elementFind ("input", "id;name;value", name, myElements)
        if foundElement == None:
            if self.showDebugging: print "** checkBoxGet() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement
        
    def checkBoxGetValue(self, name, attribute):
        """ Gets a checkbox
            parameters:
                name        - The id, name, or value of the checkbox, or a checkbox element.
                attribute   - The name of the attribute to get the value for
            returns:
                The checkbox if found, else None
        """
        if isinstance(name, basestring) or isinstance(name, int):
            foundElement = self.checkBoxGet(name)
        else:
            foundElement = name
        
        if foundElement == None:
            if self.showDebugging: print "** checkBoxGetValue() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.elementGetValue (foundElement, attribute)

    def checkBoxSet(self, name, value):
        """ Sets the value of a check box.
            parameters:
                name   - The id, name, or value of the checkbox.
                value  - 0 for false (not checked)
                         1 for true (checked)
            returns:
                True on success, else False
        """
        myElements = self.elementsGetList ("input", "type=checkbox")
        return self.elementSet("input", "id;name;value", name, "checked", value, None, myElements)
    
    def checkBoxesGet(self, filter=None):
        """ Gets all the checkboxes
            parameters:
                [filter]    - Get only checkboxes specified by the filter
            returns:
                A list of checkboxes
        """
        if filter:
            filter = "type=checkbox;" + filter
        else:
            filter = "type=checkbox"
        return self.elementsGetList ("input", filter)

    def checkBoxesGetChecked(self, name):
        """ Gets a list of checked checkbox values for a specified checkbox name
            parameters:
                name - checkbox name
            returns:
                A list of checked values for the checkbox group
        """
        return self.checkBoxesGet ("type=checkbox;checked=True;name=" + name)
    
    def checkBoxesGetValue(self, attribute, filter=None):
        """ Gets the value of an attribute for all the checkboxes
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only checkboxes specified by the filter
            returns:
                A list of the specified value of the attribute
        """
        myValues=[]
        myCheckBoxes = self.checkBoxesGet()
        for checkbox in myCheckBoxes[:]:
            myValues.append (checkbox.getAttribute(attribute))
        return myValues

    def cookieGet(self):
        """ Gets the Cookie information for the current page
            parameters:
                None
            returns:
                The Cookie information of the current page
        """
        self._wait() 
        return self._ie.Document.cookie
        
    def dateGet(self):
        """ Gets the current date
            parameters:
                None
            returns:
                Returns the current date in XX/XX/XXXX format (month,day,year)
        """
        month = datetime.date.today().month
        day = datetime.date.today().day
        year = datetime.date.today().year

        if month <10:
          month =  "0%s" % (month)
        if day <10:
          day =  "0%s" % (day)

        return "%s/%s/%s" % (month,day,year) 

    def dayGetNext(self):
        """ Gets the next day
            parameters:
                None
            returns:
                Returns the next day in XX/XX/XXXX format (month,day,year)
        """
        month = datetime.date.today().month
        day = datetime.date.today().day
        year = datetime.date.today().year
        day = 1 + day

        if month <10:
          month =  "0%s" % (month)
        if day <10:
          day =  "0%s" % (day)

        return "%s/%s/%s" % (month,day,year) 
        
    def divExists(self, name):
        """ Checks to see if a div exists
            parameters:
                name   - The id, name, or index of the button.
            returns:
                True if the div is found, else False
        """
        myElement = self.divGet (name)
        if myElement:
            return True
        else:
            return False

    def divGet(self, name):
        """ Gets a div
            parameters:
                name   - The id, name, or index of the div
            returns:
                The div if found, else None
        """
        if isinstance(name, int):
            foundElement = self.elementFindByIndex ("div", name)
        else:
            foundElement = self.elementFind ("div", "id;name", name)

        if foundElement == None:
            if self.showDebugging: print "** divGet() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement

    def divGetValue(self, name, attribute):
        """ Gets the value of an attribute on a div.
            parameters:
                name        - The id, name, or index of the div, or a div element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, basestring) or isinstance(name, int):
            foundElement = self.divGet(name)
        else:
            foundElement = name
            
        if foundElement == None:
            if self.showDebugging: print "** divGetValue() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.elementGetValue (foundElement, attribute)

    def divsGet(self, filter=None):
        """ Gets a list of divs
            parameters:
                [filter]    - Get only buttons specified by the filter
            returns:
                A list of divs
        """
        return self.elementsGetList ("div", filter)
            
    def divsGetValue(self, attribute, filter=None):
        """ Gets a list of values for the specified attribute.
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only divs specified by the filter
            returns:
                A list of images
        """
        myValues=[]
        myDivs = self.divsGet(filter)
        for div in myDivs[:]:
            myValues.append (div.getAttribute(attribute))
        return myValues

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
       
    def elementExists(self, tag, att, val):
        """ Checks to see if an element exists.
            parameters:
                tag             - The HTML tag name
                att             - The tag attribute to search for
                val             - The attribute value to match
            returns:
                True if the element exists, else False
        """ 
        foundElement = self.elementFind (tag, att, val)
        if foundElement == None:
            return False
        else:
            return True
    
    def elementFind(self, tag, attributes, val, elementList=None):
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
        try:
            self._wait()
            atts = attributes.split(";")
            regEx = False

            if isinstance(val, basestring):
                if val[0] == "!":
                    val = val.replace ("!", "", 1)
                    myRE = re.compile(val)
                    regEx = True
            
            if elementList:
                if tag:
                    elements = self.elementsGetList (tag, "tagName=" + tag, elementList)
                    
                if isinstance(val, int):        # Do we want the index?
                    return elements[val]
            else:
                elements = self.elementsGetList (tag)
                
            for el in elements[:]:
                if regEx:
                    for att in atts[:]:
                        valText = el.getAttribute(att)
                        if valText <> None:
                            m = myRE.match(valText)
                            if m:
                                return el
                else:
                    for att in atts[:]:
                        valText = el.getAttribute(att)
                        if valText <> None:
                            if isinstance(valText, basestring):
                                valText = valText.strip()
                                
                            if valText == val:
                                return el
    
            if self.showDebugging: print "** elementFind() did not find " + tag + "-" + attributes + "-" + str(val)
            return None
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return None
        else:
            return None

    def elementFindByIndex (self, tag, indexNum, filter=None, elementList=None):
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
            myElements = self.elementsGetList (tag, filter=None, elementList=None)
            return myElements[indexNum]
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return None
        else:
            return None
        
    def elementFireEvent(self, tag, controlName, eventName):
        """ Fire a named event for a given control
            parameters:
                tag         - The HTML tag name
                controlName - the control to act on
                eventName   - the event name to signal
            returns:
                True on success, else False
        """
        foundElement = self.elementFind (tag, "name", controlName)
        if foundElement:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            foundElement.FireEvent(eventName)
            return True
        else:
            if self.showDebugging: print "fireEvent() did not find " + controlName + " control."
            return False
                
    def elementGetChildren (self, element, all=True):
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
                myElements.append (elements[count])
                count +=1
            
            return myElements
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return None
        else:
            return None
        
    def elementGetParent (self, element):
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
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return None
        else:
            return None
       
    def elementGetValue (self, element, attribute):
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
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return None
        else:
            return None
    
    def elementSet(self, tag, att, val, setAtt, setVal, element=None, elementList=None):
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
            foundElement = self.elementFind (tag, att, val, elementList)
            
        if foundElement == None:
            if self.showDebugging: print "** elementSet() did not find " + tag + "-" + att + "-" + str(val)
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
                print sys.exc_info()
                traceback.print_exc(ErrorTB)
                return False
            else:
                return False

    def elementsGetList(self, tag, filter=None, elementList=None):
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
                myFrame = self.frameGet(self.frameName) 
                
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
                allElements.append (elements[count])
                count +=1

        try:
            if filter:
                myElements = []
                filters = filter.split(";")
                for el in allElements:
                    match = True
                    for f in filters[:]:
                        atts = f.split("=")
                        valText = el.getAttribute(atts[0])
                        if valText <> None:
                            valText = str(valText)
                            valText = valText.strip()
                            valText = valText.lower()
                            wantText = atts[1].lower()
                            if valText != wantText:
                                match = False
                    if match:
                        myElements.append (el)
            else:
                myElements = allElements
                
            return myElements
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print sys.exc_info()
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
        
        # Search the doc for the text    
        text_found = pageText.find(text)
        try:
            # A "-1" means nothing is found
            if text_found is not -1:
                return True
            else:
                print "Text %s Not Found!" %(text)
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return None

    def formExists(self, name):
        """ Checks to see if a form exists
            parameters:
                None
            returns:
                True if the form is found, else False
        """
        myElement = self.formGet (name)
        if myElement:
            return True
        else:
            return False
       
    def formGet(self, name=None):
        """ Gets a form
            parameters:
                [name]    - The name, id or index of the form.
            returns:
                The form if found, else None
        """
        if name == None: name = self.formName 
        if isinstance(name, int):
            foundElement = self.elementFindByIndex ("form", name)
        else:
            foundElement = self.elementFind ("form", "id;name", name)
        
        if foundElement == None:
            if self.showDebugging: print "** formGet() did not find " + name
            return None
        else:
            return foundElement

    def formGetControlNames(self, name=None): 
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
    
    def formGetValue(self, name, attribute):
        """ Gets the value of an attribute on a form
            parameters:
                name        - The id, name or index of the form, or a form element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if name == None: name = self.formName 
        if isinstance(name, basestring) or isinstance(name, int):
            foundElement = self.formGet(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print "** formGetValue() did not find " + name
            return None
        else:
            return self.elementGetValue (foundElement, attribute)

    def formGetVisibleControlNames(self, name=None):
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
    
    def formSubmit(self, name=None):
        """ Submits a form. For proper testing you should submit a form as a user
            would, such as clicking the submit button.
            parameters:
                [name] - name of form
            returns:
                True on success, else False
        """
        try:
            if name == None: name = self.formName 
            foundElement = self.elementFind ("form", "id;name", name)
            if foundElement:
                foundElement.submit()
                return True
            else:
                if self.showDebugging: print "** formSubmit() did not find the " + name + " form"
                return False
        except:
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return False
        else:
            return True         

    def formsGet(self, filter=None):
        """ Gets a list of forms
            parameters:
                [filter]    - Get only buttons specified by the filter
            returns:
                A list of forms
        """
        return self.elementsGetList ("form", filter)

    def formsGetValue(self, attribute, filter=None):
        """ Use this to get the form object names on the page
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only forms specified by the filter
            returns:
                a list of form names
        """
        myValues=[]
        myForms = self.formsGet(filter)
        for form in myForms[:]:
            myValues.append (form.getAttribute(attribute))
        return myValues
        
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
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return False
        else:
            return False
        
    def frameGet(self, name):
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
                            self._frameWait (myFrame)
                            return myFrame
                        else:
                            frames = frames[i].document.frames
            return None

    def frameGetValue(self, name, attribute):
        """ Gets the value of an attribute on a frame
            parameters:
                name        - The name of the frame
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        foundElement = self.frameGet(name)
        if foundElement == None:
            if self.showDebugging: print "** frameGetValue() did not find " + name
            return None
        else:
            return foundElement.name # can't call elementGetValue() here

    def framesGetValue(self, attribute):
        """ Gets the value of an attribute on a image
            parameters:
                attribute   - The name of the attribute to get the value for
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
    
    def goBack(self):
        """
            Navigates backward one item in the history list
        """
        self._wait()
        self._ie.GoBack()
    
    def imageClick(self, name):
        """ Clicks an image
            parameters:
                name    The id, name, src or index of the image
            returns:
                True on success, else False
        """
        if isinstance(name, basestring) or isinstance(name, int):
            myImage = self.imageGet(name)
        else:
            myImage = name
        return self.elementClick(myImage)
        
    def imageExists(self, name):
        """ Checks to see if a image exists in the HTML document.  It does not
            check to see if the image actually exists on the server.
            parameters:
                name   - The id, name, src or index of the image.
            returns:
                True if the image is found, else False
        """
        myElement = self.imageGet (name)
        if myElement:
            return True
        else:
            return False

    def imageGet(self, name):
        """ Gets an image
            parameters:
                name  - The id, name, src or index of the image
            returns:
                an image
        """
        if isinstance(name, int):
            foundElement = self.elementFindByIndex ("img", name)
        else:
            foundElement = self.elementFind ("img", "id;name;nameProp;src", name)

        if foundElement == None:
            if self.showDebugging: print "** imageGet() did not find " + str(name)
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement
        
    def imageGetValue(self, name, attribute):
        """ Gets the value of an attribute on a image
            parameters:
                name        - The id, name, value or index of the image, or image element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, basestring) or isinstance(name, int):
            foundElement = self.imageGet(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print "** imageGetValue() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.elementGetValue (foundElement, attribute)

    def imagesGet(self, filter=None):
        """ Gets a list of images
            parameters:
                [filter]    - Get only buttons specified by the filter
            returns:
                A list of images
        """
        return self.elementsGetList ("img", filter)
    
    def imagesGetValue(self, attribute, filter=None):
        """ Gets a list of the specified value for the images
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only images specified by the filter
            returns:
                A list of image values.
        """
        myValues=[]
        myImages = self.imagesGet(filter)
        for image in myImages[:]:
            myValues.append (image.getAttribute(attribute))
        return myValues

    def inputElementsGet(self, filter=None):
        """ Get all the input elements
            parameters:
                [filter]    - Get only buttons specified by the filter
            returns:
                A list of input elements
        """
        return self.elementsGetList ("input", filter)

    def javaScriptExecute(self, name):
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
            pw.execScript(script) 
        except: 
            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
            print sys.exc_info()
            traceback.print_exc(ErrorTB)

    def linkClick(self, name):
        """ Clicks a link.
            parameters:
                name   - The id or innerText of the link
            returns:
                True on success, else False
        """
        if isinstance(name, basestring) or isinstance(name, int):
            myLink = self.linkGet(name)
        else:
            myLink = name
        return self.elementClick(myLink)

    def linkExists(self, name):
        """ Checks to see if a link exists
            parameters:
                name   - The id or innerText of the link.
            returns:
                True if the link is found, else False
        """
        myElement = self.linkGet (name)
        if myElement:
            return True
        else:
            return False

    def linkGet(self, name):
        """ Gets a link
            parameters:
                name  - The id, innerText or index of the link
            returns:
                an image
        """
        if isinstance(name, int):
            foundElement = self.elementFindByIndex ("a", name)
        else:
            foundElement = self.elementFind ("a", "id;innerText", name)
        
        if foundElement == None:
            if self.showDebugging: print "** linkGet() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement

    def linkGetValue(self, name, attribute):
        """ Gets the value of an attribute on a link
            parameters:
                name        - The id, innerText or index of the link, or a link element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, basestring) or isinstance(name, int):
            foundElement = self.linkGet(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print "** linkGetValue() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.elementGetValue (foundElement, attribute)

    def linksGet(self, filter=None):
        """ Gets a list of links
            parameters:
                [filter]    - Get only links specified by the filter
            returns:
                A list of links
        """
        return self.elementsGetList ("a", filter)
    
    def linksGetValue(self, attribute, filter=None):
        """ Gets a list of the specified value for the links
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only links specified by the filter
            returns:
                A list of link values.
        """
        myValues=[]
        myLinks = self.linksGet(filter)
        for link in myLinks[:]:
            myValues.append (link.getAttribute(attribute))
        return myValues

    def listBoxGet(self, name):
        """ Gets a list box.
            parameters:
                name    - The name or index of the listbox
            returns:
                A list box
        """
        if isinstance(name, int):
            foundElement = self.elementFindByIndex ("select", name)
        else:
            foundElement = self.elementFind ("select", "name;id", name)

        if foundElement == None:
            if self.showDebugging: print "** listBoxGet() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement
        
    def listBoxGetValue(self, name, attribute):
        """ Gets the value of an attribute on a listbox
            parameters:
                name        - The id, innerText or index of the listbox, or a listbox element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, basestring) or isinstance(name, int):
            foundElement = self.listBoxGet(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print "** listBoxGetValue() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.elementGetValue (foundElement, attribute)
        
    def listBoxGetOptions(self, name):
        """ Gets the list of options associated with a listbox.
            parameters:
                The name or id of the list box
            returns:
                A list of options
        """
        foundElement = self.elementFind ("select", "name;id", name)
        if foundElement == None:
            if self.showDebugging: print "** listBoxGetOptions() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            myValues = []
            count = 0
            myElements = foundElement.options
            while count < myElements.length:
                myValues.append (myElements[count].innerText)
                count += 1
            return myValues
        
    def listBoxGetSelected(self, name):
        """ Gets the list of selected options associated with a listbox.
            parameters:
                The name or id of the list box
            returns:
                The selected text
        """
        foundElement = self.elementFind ("select", "name;id", name)
        if foundElement == None:
            if self.showDebugging: print "** listBoxGetSelected() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            myValues = []
            count = 0
            myElements = foundElement.options
            while count < myElements.length:
                if myElements[count].selected:
                    #myValues.append (myElements[count].innerText)
                    return myElements[count].innerText
                count += 1
            #return myValues
            return None

    def listBoxSelect(self, name, value):
        """ Selects an item in a list box.
            parameters:
                name    - The name or id of the listbox
                value   - The value of the item to select in the list
            returns:
                True on success, else False
        """
        foundElement = self.elementFind ("select", "name;id", name)
        if foundElement == None:
            if self.showDebugging: print "** listBoxSelect() did not find " + name + "-" + str(value)
            return False
        else:
            for el in foundElement:
                if el.text == value:
                    if self.colorHighlight: el.style.backgroundColor=self.colorHighlight
                    el.selected = True
                    foundElement.FireEvent("onChange")
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
            print sys.exc_info()
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
            print sys.exc_info()
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
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return False
        else:   return True
        
    def radioButtonGet(self, name):
        """ Gets a radio button by the name.  If there are multiple radio buttons
            with the same name, the first one found is returned.
            parameters:
                name - radio button group name or index
            returns:
                a list values for the group
        """
        myElements = self.elementsGetList ("input", "type=radio")
        if isinstance(name, int):
            foundElement = self.elementFindByIndex ("input", name, None, myElements)
        else:
            foundElement = self.elementFind ("input", "name", name, myElements)

        if foundElement == None:
            if self.showDebugging: print "** radioButtonGet() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement
  
    def radioButtonGetSelected(self, name):
        """ Gets a list of selected radio button values for a Radio Button group
            parameters:
                name - radio button group name
            returns:
                a list of selected buttons from the group
        """
        myValues = []
        myElements = self.elementsGetList ("input", "type=radio;checked=True;name=" + name)
        for el in myElements[:]:
            myValues.append(el.value)
        return myValues
    
    def radioButtonSet(self, name, value, checked=True):
        """ Sets a Radio Button value
            parameters:
                name        - radio button group name
                value       - Which item to pick by name
                [checked]   - Check the button, True or False
            returns:
                True on success, else False
        """
        #TODO: Find way to get innerText
        myElements = self.elementsGetList ("input", "type=radio;name=" + name)
        for el in myElements[:]:
            if el.value == value:
                if self.colorHighlight: el.style.backgroundColor=self.colorHighlight
                el.checked = checked
                el.FireEvent("onClick")
                return True

        if self.showDebugging: print "** radioButtonSet() did not find " + name
        return False
        
    def radioButtonsGet(self, filter=None):
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
        return self.elementsGetList ("input", filter)

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
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return False
        else:   return True
        
    def scriptGet(self):
        """ Writes out a script based on the form that you input
            this writes the get methods of each control
            parameters:
                None
            returns:
                Nothing
        """
        
        self._wait()
        items = ["input", "select"]
        for i in items:
                        
            doc = self._ie.Document.getElementsByTagName(i)
            
            for i in range(doc.length):
                x = doc[i] 
                etype = getattr(x,"type")
                name = getattr(x,"name")
                
                    
                # Write out script line for each type
                if etype == 'text':
                    a =  """ie.GetTextBox("""
                    
                    c = "'%s'" % (name)
                    d = ","
                    if self.formName == 0:
                        e = "%s" % (self.formName)
                    else: 
                        e = "'%s'" % (self.formName)
                    f = ")" 
                    output = a+c+d+e+f
                    print output
                           
    
                elif etype == 'checkbox':
                    a = """ie.GetCheckBox("""
                    b = "'%s'," % (name)
                    if self.formName == 0:
                        c = "%s" % (self.formName)
                    else: 
                        c = "'%s'" % (self.formName)
                    d = ",1)"
                    output = a+b+c+d
                    print output
    
                elif etype == 'radio':
                    a = """ie.GetRadioButton("""
                   
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+c+d+e
                    print output
    
               
                elif etype == 'textarea':
                    a = """ie.GetTextBox("""
                    
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+c+d+e
                    print output
                    
                elif etype == 'select-one':
                    a =  """ie.GetListBox("""
                    
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+c+d+e
                    print output          

    def scriptWriteClass(self):
        """ Writes out a script for a Pyunit testcase based on the form that you input
            first attempt to automate the script writing process
            parameters:
                None
            returns:
                Nothing
        """
        
        self._wait()
        items = ["input", "select"]
        for i in items:
                        
            doc = self._ie.Document.getElementsByTagName(i)
                
            for i in range(doc.length):
                x = doc[i] 
                etype = getattr(x,"type")
                name = getattr(x,"name")
                    
                                # Write out script line for each type
                if etype == 'text':
                    a =  """self._ie.SetTextBox("""
                    b =  """'param',"""
                    c = "'%s'" % (name)
                    d = ","
                    if self.formName == 0:
                        e = "%s" % (self.formName)
                    else: 
                        e = "'%s'" % (self.formName)
                    f = ")" 
                    output = a+b+c+d+e+f
                    print output
                           
                elif etype == 'image':       
                    a = """self._ie.ClickImage("""
                    b = "'%s,'" %(name)

                    if self.formName == 0:
                        c = "%s" % (self.formName)
                    else: 
                        c = "'%s'" % (self.formName)
                    d = ")" 
                    output = a+b+c+d
                    print output
    
                elif etype == 'checkbox':
                    a = """self._ie.SetCheckBox("""
                    b = "'%s'," % (name)
                    if self.formName == 0:
                        c = "%s" % (self.formName)
                    else: 
                        c = "'%s'" % (self.formName)
                    d = ",1)"
                    output = a+b+c+d
                    print output
    
    
                elif etype == 'radio':
                    a = """self._ie.SetRadioButton("""
                    b = """'BLANK',""" 
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
    
                elif etype == 'button':
                    a = """self._ie.ClickButton("""
                    b = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
    
                elif etype == 'submit':
                    a = """self._ie.ClickSubmitButton("""
                    b = "'%s'," % (name)
                    if self.formName == 0:
                        c = "%s" % (self.formName)
                    else: 
                        c = "'%s'" % (self.formName)
                    d = ")"
                    output = a+b+c+d
                    print output
                    
                elif etype == 'textarea':
                    a = """self._ie.SetTextBox("""
                    b = """'param',"""
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
                    
                elif etype == 'select-one':
                    a =  """self._ie.SetListBox("""
                    b = """'param',"""
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
    
          
    
    def scriptWrite(self):
        """ Writes out a script based on the form that you input
            first attempt to automate the script writing process
            parameters:
                None
            returns:
                Nothing
        """
        
        self._wait()
        items = ["input", "select"]
        for i in items:
                        
            doc = self._ie.Document.getElementsByTagName(i)
    
            
            for i in range(doc.length):
                x = doc[i] 
                etype = getattr(x,"type")
                name = getattr(x,"name")
                nameProp = getattr(x,"nameProp")
                    
                # Write out script line for each type
                if etype == 'text':
                    a =  """ie.SetTextBox("""
                    b =  """'param',"""
                    c = "'%s'" % (name)
                    d = ","
                    if self.formName == 0:
                        e = "%s" % (self.formName)
                    else: 
                        e = "'%s'" % (self.formName)
                    f = ")" 
                    output = a+b+c+d+e+f
                    print output
                           
                elif etype == 'image':       
                    a = """ie.ClickImage("""
                    b = "'%s,'" %(nameProp)

                    if self.formName == 0:
                        c = "%s" % (self.formName)
                    else: 
                        c = "'%s'" % (self.formName)
                    d = ")" 
                    output = a+b+c+d
                    print output
    
                elif etype == 'checkbox':
                    a = """ie.SetCheckBox("""
                    b = "'%s'," % (name)
                    if self.formName == 0:
                        c = "%s" % (self.formName)
                    else: 
                        c = "'%s'" % (self.formName)
                    d = ",1)"
                    output = a+b+c+d
                    print output
    
                elif etype == 'radio':
                    a = """ie.SetRadioButton("""
                    b = """'BLANK',""" 
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
    
                elif etype == 'button':
                    a = """ie.ClickButton("""
                    b = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
    
                elif etype == 'submit':
                    a = """ie.ClickSubmitButton("""
                    b = "'%s'," % (name)
                    if self.formName == 0:
                        c = "%s" % (self.formName)
                    else: 
                        c = "'%s'" % (self.formName)
                    d = ")"
                    output = a+b+c+d
                    print output
                    
                elif etype == 'textarea':
                    a = """ie.SetTextBox("""
                    b = """'param',"""
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
                    
                elif etype == 'select-one':
                    a =  """ie.SetListBox("""
                    b = """'param',"""
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
    
    def scriptWriteFrames(self):
        """ Writes out a Frames script based on the form that you input
            first attempt to automate the script writing process
            parameters:
                None
            returns:
                Nothing
        """
        
        self._wait()
        if self.frameName:
            self._frameWait()
            
        items = ["input", "select"]
        for i in items:
           
            doc = self._ie.Document.frames[self.frameName].document.getElementsByTagName(i)    
            
            for i in range(doc.length):
                x = doc[i] 
                type = getattr(x,"type")
                name = getattr(x,"name")
                    
                 # Write out script line for each type
                if etype == 'text':
                    a =  """ie.SetTextBox("""
                    b =  """'param',"""
                    c = "'%s'" % (name)
                    d = ","
                    if self.formName == 0:
                        e = "%s" % (self.formName)
                    else: 
                        e = "'%s'" % (self.formName)
                    f = ")" 
                    output = a+b+c+d+e+f
                    print output
                           
                elif etype == 'image':       
                    a = """ie.ClickImage("""
                    b = "'%s,'" %(name)

                    if self.formName == 0:
                        c = "%s" % (self.formName)
                    else: 
                        c = "'%s'" % (self.formName)
                    d = ")" 
                    output = a+b+c+d
                    print output
    
                elif etype == 'checkbox':
                    a = """ie.SetCheckBox("""
                    b = "'%s'," % (name)
                    if self.formName == 0:
                        c = "%s" % (self.formName)
                    else: 
                        c = "'%s'" % (self.formName)
                    d = ",1)"
                    output = a+b+c+d
                    print output
    
                elif etype == 'radio':
                    a = """ie.SetRadioButton("""
                    b = """'BLANK',""" 
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
    
                elif etype == 'button':
                    a = """ie.ClickButton("""
                    b = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
    
                elif etype == 'submit':
                    a = """ie.ClickSubmitButton("""
                    b = "'%s'," % (name)
                    if self.formName == 0:
                        c = "%s" % (self.formName)
                    else: 
                        c = "'%s'" % (self.formName)
                    d = ")"
                    output = a+b+c+d
                    print output
                    
                elif etype == 'textarea':
                    a = """ie.SetTextBox("""
                    b = """'param',"""
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
                    
                elif etype == 'select-one':
                    a =  """ie.SetListBox("""
                    b = """'param',"""
                    c = "'%s'," % (name)
                    if self.formName == 0:
                        d = "%s" % (self.formName)
                    else: 
                        d = "'%s'" % (self.formName)
                    e = ")"
                    output = a+b+c+d+e
                    print output
                    
    def startTimer(self):
        """
            Start time for this timer
        """
        self.timer = datetime.datetime.now()
    
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
    
    def stop(self):
        """
            Cancels any in process navigation 
        """
        self._wait()
        self._ie.Stop()
        
    def tableCellExists(self, tableName, cellText):
        """ Checks to see if a cell in a table exists
            parameters:
                tableName   - The id, name or index of the table, or a table element.
                cellText    - The cell text to search for
            returns:
                True if the table is found, else False
        """
        if isinstance(tableName, basestring) or isinstance(tableName, int):
            myTable = self.tableGet(tableName)
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
            print sys.exc_info()
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
        myElement = self.tableGet (name)
        if myElement:
            return True
        else:
            return False
        
    def tableGet(self, name):
        """ Gets a table
            parameters:
                name  - The id or name of the table
            returns:
                a table
        """
        if isinstance(name, int):
            foundElement = self.elementFindByIndex ("table", name, name)
        else:
            foundElement = self.elementFind ("table", "id;name", name)

        if foundElement == None:
            if self.showDebugging: print "** tableGet() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement
        
    def tableGetData(self, name):
        """ Gets the date from a table
            parameters:
                name  - The id, name or index of the table, or a table element.
            returns:
                a string containing all the table data
        """
        if isinstance(name, basestring) or isinstance(name, int):
            myTable = self.tableGet(name)
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
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return None
        else:   return None
    
    def tableRowExists(self, name, row):
        """ Checks to see if a row in a table exists
            parameters:
                Name        - The id, name or index of the table, or a table element.
                row[]       - The row to search for. Use * to ignore cell.
            returns:
                True if the table is found, else False
        """
        if self.tableRowGetIndex (name, row):
            return True
        else:
            return False
        
    def tableRowGetIndex(self, name, row):
        """ Gets the index of a row in a table.
            parameters:
                Name        - The id, name or index of the table
                row[]       - The row to search for. Use * to ignore cell.
            returns:
                index of the row if found
        """
        if isinstance(name, basestring) or isinstance(name, int):
            myTable = self.tableGet(name)
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
            print sys.exc_info()
            traceback.print_exc(ErrorTB)
            return None
        else:   return None

    def tablesGet(self, filter=None):
        """ Gets a list of tables
            parameters:
                [filter]    - Get only tables specified by the filter
            returns:
                A list of tables
        """
        return self.elementsGetList ("table", filter)
    
    def textAreaExists(self, name):
        """ Checks to see if a textarea exists
            parameters:
                name   - The name, id or index of the textarea
            returns:
                True if the textarea is found, else False
        """
        myElement = self.textAreaGet (name)
        if myElement:
            return True
        else:
            return False

    def textAreaGet(self, name):
        """ Gets a text area.
            parameters:
                name    - The name, id or index of the textarea
            returns:
                The text area if found.
        """
        if isinstance(name, int):
            foundElement = self.elementFindByIndex ("textarea", name)
        else:
            foundElement = self.elementFind ("textarea", "name;id", name)
      
        if foundElement == None:
            if self.showDebugging: print "** textAreaGet() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement

    def textAreaGetValue(self, name, attribute):
        """ Gets the value of an attribute on a textarea
            parameters:
                name        - The id, name or index of the textarea, or a textarea element.
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, basestring) or isinstance(name, int):
            foundElement = self.textAreaGet(name)
        else:
            foundElement = name
            
        if foundElement == None:
            if self.showDebugging: print "** textAreaGetValue() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.elementGetValue (foundElement, attribute)
        
    def textAreaSet(self, name, value):
        """ Sets the text in a textarea.
            parameters:
                name    - The id, name or index of the text area, or a textarea element.
                value   - The value to set the text area to.
            returns:
                True on succes, else False
        """
        if isinstance(name, basestring) or isinstance(name, int):
            foundElement = self.elementFind ("textarea", "name;id", name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print "** textAreaSet() did not find " + name + "-" + str(value)
            return False
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            foundElement.value = value
            return True

    def textAreasGet(self, filter=None):
        """ Gets a list of textareas
            parameters:
                [filter]    - Get only textareas specified by the filter
            returns:
                A list of textareas
        """
        return self.elementsGetList ("textarea")

    def textAreasGetValue(self, attribute, filter=None):
        """ Gets a list of the specified value for the textareas
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only textareas specified by the filter
            returns:
                A list of link values.
        """
        myValues=[]
        myAreas = self.textAreasGet(filter)
        for area in myAreas[:]:
            myValues.append (area.getAttribute(attribute))
        return myValues
    
    def textBoxExists(self, name):
        """ Checks to see if a textbox exists
            parameters:
                name   - The name or id of the textbox
            returns:
                True if the textbox is found, else False
        """
        myElement = self.textBoxGet (name)
        if myElement:
            return True
        else:
            return False

    def textBoxGet(self, name):
        """ Gets a text box.
            parameters:
                name    - The name, id or index of the textbox
            returns:
                The text area if found.
        """
        if isinstance(name, int):
            foundElement = self.elementFindByIndex ("input", name)
        else:
            foundElement = self.elementFind ("input", "id;name;value", name)
        
        if foundElement == None:
            if self.showDebugging: print "** textBoxGet() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return foundElement

    def textBoxGetValue(self, name, attribute):
        """ Gets the value of an attribute on a textbox
            parameters:
                name        - The id, name or index of the textbox, or a textbox element
                attribute   - The name of the attribute to get the value for
            returns:
                The value of the attribute
        """
        if isinstance(name, basestring) or isinstance(name, int):
            foundElement = self.textBoxGet(name)
        else:
            foundElement = name
            
        if foundElement == None:
            if self.showDebugging: print "** textBoxGetValue() did not find " + name
            return None
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            return self.elementGetValue (foundElement, attribute)

    def textBoxSet(self, name, value):
        """ Sets the text in a text box.
            parameters:
                name    - The id, name or index of a textbox, or a textbox element.
                value   - The value to set the textbox to.
            returns:
                True on succes, else False
        """
        if isinstance(name, basestring) or isinstance(name, int):
            foundElement = self.textBoxGet(name)
        else:
            foundElement = name

        if foundElement == None:
            if self.showDebugging: print "** textBoxSet() did not find " + name + "-" + str(value)
            return False
        else:
            if self.colorHighlight: foundElement.style.backgroundColor=self.colorHighlight
            foundElement.value = value
            return True

    def textBoxesGet(self, filter=None):
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
        return self.elementsGetList ("input", filter)

    def textBoxesGetValue(self, attribute, filter=None):
        """ Gets a list of values for the specified attribute
            parameters:
                attribute   - The name of the attribute to get the value for
                [filter]    - Get only textboxes specified by the filter
            returns:
                A list of the specified value of the attribute
        """
        myValues=[]
        myBoxes = self.textBoxesGet()
        for box in myBoxes[:]:
            myValues.append (box.getAttribute(attribute))
        return myValues
    
    def windowFind(self, title, indexNum=1):
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
            shellWnd = DispatchEx('Shell.Application')
            wins = shellWnd.Windows()
            winsCount = wins.Count
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

        if self.showDebugging: print "** windowFind() did not find the " + title + "-" + str(indexNum) + " window."
        return None
    