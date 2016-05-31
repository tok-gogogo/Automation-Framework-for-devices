#-*- coding: gbk -*-  
#-----------------------------------------------------------------------------
# Name:        py_mysql.py
# Purpose:     
#
# Author:      gongke
#
# Created:     2014/02/27
# RCS-ID:      py_mysql use mysql
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------

import MySQLdb
from public import *
import types
from global_parame import *

KEY_ROW = 'rowx'
KEY_COL = 'coly'

KEY_STNAME_INDEX = 0
KEY_URL_INDEX = 1
KEY_HEADPART = 3
#---------------------------------------
#excel
KEY_HEAD = 'HEADER'
KEY_END = 'END'
KEY_A_COL = 0
KEY_B_COL = 1
KEY_C_COL = 2
KEY_D_COL = 3

KEY_ASSIST = 'ASSIST'
KEY_SQLCMD = 'SQLExecute'
KEY_SQLCHECK = 'CheckValue'
KEY_SQLRESERVE = 'Reserve'

KEY_CONTROLTYPE = 'ControlType'
KEY_CONTROLNAME = 'ControlName'
KEY_CONTROLVALUE = 'ControlValue'

KEY_URL_NONE = 'NONE'
KEY_URL_WAITEVENT_START = 'START'
KEY_URL_WAITEVENT_END = 'END'
KEY_GROUP = 'G'
KEY_COMMENT = 'C'
ENCODE_DECODE = 'gbk'


class opSQL():
    def __init__(self):
        self.m_bSTOP = False
        
    def init_sql(self,*args):
        #*args : user=root , host='localhost',passwd='',dbname =''
        dick = {0:'host',1:'user',2:'passwd',3:'dbname',4:'port'}
        dic_init ={'user':'root','passwd':'admin','host':'localhost','dbname':'mydata','port':3306}
        num = 0
        dick_keys = dick.keys()
        dick_values =dick.values()
        self.error_list = []
        self.error_total = 0
        for  arg in args:
            if len(arg.split('='))==1:
                dic_init[dick[num]] 
            else:
                num = dick_values.index(arg.split('=')[0].strip())
                dic_init[dick[dick_keys[num]]]  = arg.split('=')[1].strip()
            num = num + 1 
        
        tmp_param =[]
        tmp_param.append(dic_init['host'])
        tmp_param.append(dic_init['user'])
        tmp_param.append(dic_init['passwd'])
        tmp_param.append(dic_init['dbname'])
        tmp_param.append(dic_init['port'])
        
        print 'init param:',tmp_param
        arg_tuple = tuple(tmp_param)
        #cmd = 'MySQLdb.connect'
        try:
            self.conn = apply(MySQLdb.connect,arg_tuple)
            self.conn.set_character_set(ENCODE_DECODE)
            self.cursor  = self.conn.cursor()
        except Exception,e:
            log_print(e)
            log_print('connect mysql fail')
            return False
        return True
            
    #def is_chinese(self,uchar):
    
    def ModifyTable(self,msg):
        for x in msg:
            mac_addr = x[0]
            mac_step="000000000001"
            mac_addr = mac_increase_param_13(mac_addr,mac_step,500)
            total = 0
            sqlcmd  = "insert into allmactable values('"
            for z in x:
                if total==0:
                    sqlcmd = sqlcmd  + mac_addr + "'"
                elif total==1:
                    sqlcmd = sqlcmd  + ",'unuse'"
                elif total==3:
                    sqlcmd = sqlcmd  + ",'"+ x[3].strftime("%Y%m%d%H%M%S")+"'"
                else:
                    if z==None:
                        z=''
                    sqlcmd = sqlcmd +",'"+ z +"'"
                total+=1
            sqlcmd = sqlcmd + ")"
            print "sqlcmd:",sqlcmd
            self.update(sqlcmd)
            sqlcmd = "delete from allmactable where Status='used'"
            self.update(sqlcmd)

    def close_mysql(self):
        self.cursor.close()
        self.conn.close()
        
    def update(self,sqlcmd):
        msg = None
        try:
            self.cursor.execute(sqlcmd)
            msg = self.cursor.fetchall()
        except Exception,e:
            log_print(e)
            log_print('SQL execute error!!!!')
        log_print('********* sql result *********')   
        log_print(msg)
            #sqlcmd = "update allmactable set Mac='unuse' where Status='used'"
            
            
        log_print('********* result end   *********')
        #self.cursor.close()
        self.conn.commit()
        #self.conn.close()
        return msg
        
    def execute_new(self,cmd,checkvalue):
        try:
            self.cursor.execute(cmd)
            msg = self.cursor.fetchall()
            log_print('********* sql result *********')
            #print msg
            
            log_print(msg)
            log_print('********* result end   *********')
            Find_str_flag = False
            #print 'cmd:',cmd
            #print 'checkvalue:',checkvalue
            if checkvalue!='':
                for x in msg:
                    for y in x:
                        if y== checkvalue:
                            Find_str_flag = True
                            break
            else:
                Find_str_flag = True
                
            if Find_str_flag ==True:
                info = 'execute cmd:' + cmd  + ' and find the keyword:' + checkvalue
                log_print(info)
            else:
                
                info = 'execute cmd:' + cmd  + ' and not find the keyword:' + checkvalue
                self.error_total +=1
                self.error_list.append({self.error_total:{'sql':cmd,'checkvalue':checkvalue.decode(ENCODE_DECODE)}}) 
                log_print(info)
                return False
        except Exception,e:
            log_print(e)
            info = cmd  + 'execute fail!!!'
            self.error_total +=1
            self.error_list.append({self.error_total:{'sql':cmd,'checkvalue':checkvalue.decode(ENCODE_DECODE)}}) 
            log_print(info)
            return False 
        return True  
                
    def execute(self,*args):
        find_str = ''
        cmd = ''
        num = 0
        #self.cursor.execute('select * from user')
        #rs = self.cursor.fetchall()
        for arg in args:
            if num ==0:
                find_str  = arg
            elif num ==1:
                cmd = arg
            else:
                cmd = cmd + ',' + arg
            num = num +1
        try:
            self.cursor.execute(cmd)
            msg = self.cursor.fetchall()
            log_print('********* sql execute result *********')
            log_print(msg)
            if find_str!=None:
                find_flag = False
                for x in msg:
                    if find_str == x[1]:
                        print 'find the keyword:%s in : %s %s %s %s '%(find_str,x[0],x[1],x[2].encode(ENCODE_DECODE),x[3]) 
                        find_flag =True
                        break
                if find_flag == False:
                    print 'not find the keyword:',find_str
                    return False
                    
        except Exception,e:
            log_print(e)
            log_print('mysql command execute fail')
            return False 
        return True  
    
    def is_chinese(self,uchar):
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False
    def close(self):
        self.conn.close()
    
   
       
    def readglobal(self):
        p_path1 = os.path.abspath(sys.argv[0])
        tmp_global_file ='\\global\\global_param.xls'
        findstr = 'Simu'
        path_parent = Getfindpath(p_path1,findstr)
        global_file = path_parent + tmp_global_file
        self.read_global_param(global_file)
        
    def read_global_param(self,filename ='E:\\Simu_server\\global\\global_param.xls',sheetname='global'):
        testexcel = readexcel(filename,sheetname)
        self.global_p = testexcel.Excel_read()
        msg = self.global_p
        log_print(msg)
        
    def Replace_global_multi_list(self,list=[]):
        tmp_list =[]
        tmp_l=[]
        for x in list:
            tmp_l = self.Replace_global_param_dic(x)
            tmp_list.append(tmp_l)
        return tmp_list
            
    def Replace_global_param_dic(self,list=[]):
        #print '********** Replace_global_param_dic before**********:'
        #log_print(list)
        tmp_list_op = []
        for dic_t in list:
            #print dic_t
            dic_list_keys = dic_t.keys()
            dic_list_values=dic_t.values()
            tmp_list = self.Replace_global_param(dic_list_values)
            dic_tt = {}
            for i in range(len(dic_list_keys)):
                print dic_list_keys[i],tmp_list[i]
                dic_tt[dic_list_keys[i]] = tmp_list[i]
            tmp_list_op.append(dic_tt)
        #print '********** Replace_global_param_dic ___after  **********:'
        #log_print(tmp_list_op)
        return tmp_list_op
 
    def Replace_global_param(self,list=[]):
        print '********** Replace_global_param **********'
        tmp_list_op = []
        for x in list:
            if x.find('%%')>-1:
                list_global = x.split('%%')
                tmp_t = 0
                tmp_str =''
                #print list_global
                for tmp_str_p in list_global:
                    if tmp_t % 2 == 0:
                        tmp_str= tmp_str + tmp_str_p
                    else:
                        #print '*******here********',tmp_str_p
                        if self.global_p.has_key(tmp_str_p)==True:
                            tmp_str = tmp_str + self.global_p[tmp_str_p]
                        else:
                            msg = 'the global file excel not find the global_parma:'+tmp_str_p
                            self.test_NG_error = msg
                            log_print(msg)
                    tmp_t = tmp_t + 1
                #print tmp_str
                tmp_list_op.append(tmp_str)
            else:
                tmp_list_op.append(x)
        return tmp_list_op
    
    
    def OpenFile(self,filePath):
        log_print( 'OpenFile fuction')
        try:
            obj_book = xlrd.open_workbook(filePath)
            return obj_book
        except Exception ,e:
            log_print(e)
            
    def OpMySQL(self,FilePath,Sheet,FlowName):
        self.readglobal()
        myPath = FilePath  
        log_print(myPath)       
        lst = []
        obj_book = 0
        obj_table = 0
        
        LOOPMAX = 0
        shttName =''
        ret = 0 #return value form function
        
        obj_book =  self.OpenFile(myPath)
        for sheet_name in obj_book.sheet_names():
            if sheet_name == Sheet :
                obj_table = obj_book.sheet_by_name(sheet_name) 
                break
        if obj_table == 0 :
            log_print('error: Open excel file failed,Please check path of file is right or check sheetname') 
            return False
        
        bNeedReadHead = True
        NEXTNODE = True

        myDictNodeCur = {'rowx':'','coly':''}
        myDictNodeNext = {'rowx':'','coly':''}
        dct_Cell={} #dicitionary
        while NEXTNODE == True:
            if bNeedReadHead == True:
                if self.ReadFlowHeader(obj_table,FlowName,myDictNodeNext) == False:
                    return  False
                bNeedReadHead = False           
            
            if (myDictNodeNext[KEY_ROW] == -1) & ( myDictNodeNext[KEY_COL] == -1):
                NEXTNODE = False
                continue
            
            myDictNodeCur.update(myDictNodeNext)
            #read Page
            if self.ReadFlowPage(obj_table,myDictNodeCur,myDictNodeNext,lst) == False:
                return False
            
            if (myDictNodeNext[KEY_ROW] == -1) & (myDictNodeNext[KEY_COL] == -1):
                NEXTNODE = False
                continue 
        #print lst   #need dele    
        print '*************'
        log_print( lst)
        print '*************'
        if self.OperateSQL(FlowName,lst) == False:
            return False
        if len(self.error_list)>0:
            log_print('sql execute error:')
            p_str ='['
            p_num = 0 
            for x in self.error_list:
                #print 'x:',x
                p_num = p_num + 1
                p_str=p_str + '{'
                p_str = p_str + str(p_num)+':{\'sql\':'
                p_str = p_str + x[p_num]['sql']
                p_str = p_str + ','
                p_str = p_str + '\'checkvalue\':'
                p_str = p_str + x[p_num]['checkvalue']
                p_str = p_str +'}'
                if len(self.error_list) == p_num:
                    p_str=p_str + '}'
                else:
                    p_str=p_str + '},'
            p_str=p_str + ']'
            log_print(p_str)
        del lst    
        return True           
        
    def OperateSQL(self,FlowName,lst):
        self.test_NG_error = ''
        lst = self.Replace_global_multi_list(lst)
        log_print('********* Operate Replay_globa: ************\n')
        log_print(lst)
        if self.test_NG_error.find('the global file')>-1:
            return False
        dstURL={}
        lstLen = len(lst)
        i = 0
        while i < lstLen:
            lstSub=[]
            lstSub.extend(lst[i])
            if self.m_bSTOP == True:
                self.close()
            lstSubLen = len(lstSub)
            j = 0    
            while j < lstSubLen:
                if self.m_bSTOP == True:
                    self.close()
                if j == 0 :
                    dstURL={}
                    dstURL.update(lstSub[j])   
                    if self.init_sql(dstURL['Init'])==False:
                        return False
                else:
                    dstComb = {}
                    dstComb.update(lstSub[j])
                    if dstComb[KEY_ASSIST]== KEY_COMMENT:
                        j+=1                  
                        continue
                    try:
                        cmd = dstComb[KEY_CONTROLTYPE]
                        checkvalue =dstComb[KEY_CONTROLNAME]
                        #self.execute(checkvalue,cmd)
                        self.execute_new(cmd,checkvalue)
                        #if self.execute_new(cmd,checkvalue) ==False:
                            
                    except Exception,e:
                        log_print(e)
                        return False 
                j+=1
            i+=1         
        return True
        
    def ReadFlowPage(self,obj_table,dctCurNode,dctNextNode,lst):
        log_print( 'ReadFlowPage fuction')
        lstSub = []
        strNextNode = ''    
      
        ret = self.ReadWebPgURL(obj_table,dctCurNode,lstSub)
        if ret == False:
            return False
        else:
            strNextNode = ret
            

        ret = self.CheckWebPgControl(obj_table,dctCurNode)            
        if ret == False:
            return False
            
        ret = self.ReadWebPgControl(obj_table,dctCurNode,lstSub)
        if ret == False:
            return False    
            
        lst.append(lstSub)
            
        self.transform(strNextNode,dctNextNode)
        
        
    
    def ReadWebPgURL(self,obj_table,dctCurNode,lst):
        log_print( 'ReadPg fuction')
        strNextNode = ''
        myURL =''      
        row = dctCurNode[KEY_ROW]
        col = dctCurNode[KEY_COL]
        
        #Get Keyword URL 
        myURL = obj_table.cell(row+1,col).value
        myURL.strip()
        
        if cmp(myURL,'Init') == -1:
            log_print( 'error:not find KeyWord-Init,Please check format of file')
            return False
          
        #Get URL Value    
        myURLValue = obj_table.cell(row+1,col+1).value 
        myURLValue.strip()      
        #test value.can not be empty.
        if myURLValue =='':
            log_print('error: not find value of ')
            return False
            
        dct_URL = {'Init':myURLValue}
        lst.append(dct_URL)            
        #get NextNode
        strNextNode = obj_table.cell(row,col+3).value
        return strNextNode
    
    
    def CheckWebPgControl(self,obj_table,dctCurNode):
        log_print( 'CheckWebPgControl fuction')
        row = dctCurNode[KEY_ROW]+2
        col = dctCurNode[KEY_COL]        

        myASSIST = obj_table.cell(row,col).value
        myASSIST.strip()
        myControlType = obj_table.cell(row,col+1).value
        myControlType.strip()

        myControlName = obj_table.cell(row,col+2).value
        myControlName.strip()
        myControlValue = obj_table.cell(row,col+3).value
        myControlValue.strip()
        
        if cmp(myASSIST,KEY_ASSIST) == -1:
            log_print('Can not find sqlExecute')     
            return False
            
        if cmp(myControlType,KEY_SQLCMD) == -1:             
            log_print('not find SqlExecute')
            return False
        
        if cmp(myControlName,KEY_SQLCHECK) == -1:               
            log_print( 'not find CheckValue')
            return False
        
        if cmp(myControlValue,KEY_SQLRESERVE) == -1:
           log_print( 'not find Reserve')
           return False           
    
    def ReadWebPgControl(self,obj_table,dctCurNode,lst):
        log_print( 'ReadWebPgControl fuction')
        print 'ReadWebPgControl'
        row = dctCurNode[KEY_ROW]+3
        col = dctCurNode[KEY_COL]      
        
        nrows = obj_table.nrows  
        timesBlank = 0 
        for rows in range(row,nrows):
            dct_Combn={}
            mySubASSIST = str(obj_table.cell(rows,col).value)
            mySubASSIST.strip()
            if mySubASSIST == KEY_END:
                return True
            dct_ASSIST ={KEY_ASSIST:mySubASSIST}
            dct_Combn.update(dct_ASSIST)
            
            mySubControlType = str(obj_table.cell(rows,col+1).value)
            mySubControlType.strip()
            if mySubControlType =='':
                log_print('not find sql execute')
                return False
            dct_CONTROLTYPE= {KEY_CONTROLTYPE:mySubControlType}         
            dct_Combn.update(dct_CONTROLTYPE)
            
            mySubControlName = str(obj_table.cell(rows,col+2).value.encode(ENCODE_DECODE)) 
            mySubControlName.strip()
            if isinstance(mySubControlName,float) == False & isinstance(mySubControlName,int) == False:
                if self.isChinese(mySubControlName) == True:
                    mySubControlValue = obj_table.cell(rows,col+2).value
                else:
                    mySubControlValue = obj_table.cell(rows,col+2).value.encode(ENCODE_DECODE)
                
            else:
                mySubControlName = str(mySubControlName)
                mySubControlName = mySubControlName.encode(ENCODE_DECODE)
                mySubControlName = mySubControlName[0:mySubControlValue.find('.')]
            dct_CONTROLNAME = {KEY_CONTROLNAME:mySubControlName}
            dct_Combn.update(dct_CONTROLNAME)
            
            mySubControlValue = obj_table.cell(rows,col+3).value
            if isinstance(mySubControlValue,float) == False & isinstance(mySubControlValue,int) == False:
                if self.isChinese(mySubControlValue) == True:
                    mySubControlValue = obj_table.cell(rows,col+3).value
                else:
                    mySubControlValue = obj_table.cell(rows,col+3).value.encode(ENCODE_DECODE)
                
            else:
                mySubControlValue = str(mySubControlValue)
                mySubControlValue = mySubControlValue.encode(ENCODE_DECODE)
                mySubControlValue = mySubControlValue[0:mySubControlValue.find('.')]
            dct_CONTROLVALUE = {KEY_CONTROLVALUE:mySubControlValue}
            dct_Combn.update(dct_CONTROLVALUE) 
            lst.append(dct_Combn)
            
            print 'dct_Combn:',dct_Combn     
            del dct_Combn
            
        return True
    
    def isChinese(self,strCheck):   
        log_print( 'isChinese fuction')     
        hz_yes = False   
        for  ch  in  strCheck:
              
            if  isinstance(ch, unicode):
                  
                if ch >= u'\u4e00' and ch<=u'\u9fa5': #have chinese.
                      
                    hz_yes = True   
                    break   
            else :  
                continue
                        
        return hz_yes
    
    def ReadFlowHeader(self,obj_table,FlowName,dctNode):
        print 'ReadFlowHeader fuction :',FlowName
        myFlowName = ''
        myDict = {'rowx':'','coly':''}
        nrows = obj_table.nrows
        for rows in range(0,nrows):
            dct_Combn={}
            myHeader = obj_table.cell(rows,KEY_B_COL).value
            myHeader.strip()
            if myHeader != '':
                if myHeader == 'FLOWHEADER':
                    myFlowName = obj_table.cell(rows,KEY_C_COL).value
                    
                    if myFlowName == FlowName:
                        strOrg =  obj_table.cell(rows+1,KEY_C_COL).value
                        strOrg.strip()
                        self.transform(strOrg,dctNode)                         
                        return True  
        return False
    
    def transform(self,strOrg,dctRowCol):
        print 'transform:',strOrg
        myStrOrg = strOrg
        lstColch = []
        lstColn = []        
        lstRown = []
        if (strOrg == 'NULL')|(strOrg == ''):
           dctRowCol[KEY_ROW] = -1
           dctRowCol[KEY_COL] = -1
           return
        self.checkString(strOrg)
        #get Col
        for ch in myStrOrg:
           if ch.isalpha() == True:               
               lstColch.append(ch)
           else:
               break
        for ndex in range(len(lstColch)):     
            lstColn.append( self.strToNum(lstColch[ndex]))
            
       #get col
        dctRowCol[KEY_COL] = self.Cal26(lstColn)
        
                
       #get Row        
        for ch in myStrOrg:
           if ch.isalpha() == True:
               continue
           else:
               lstRown.append(int(ch))
        
       #get row
        dctRowCol[KEY_ROW] = self.Cal10(lstRown)  
        print ' *********** transform *********** '  
        print dctRowCol
        print ' *********** transform *********** '  
        
    #calculate 26    
    def Cal26(self,lst):
        sum = 0
        for x in range(len(lst)):
            sum  = sum  + lst.pop()*(26**x)
        
        sum = sum - 1
        return sum            
        
    #calculate 10   
    def Cal10(self,lst):
        sum = 0    
        for x in range(len(lst)):
            sum  = sum  + lst.pop()*(10**x)
        
        sum = sum - 1
        return sum
    
    def strToNum(self,ch):
        if (ch == 'A') | (ch == 'a'):return 1
        if (ch == 'B') | (ch == 'b'):return 2
        if (ch == 'C') | (ch == 'c'):return 3
        if (ch == 'D') | (ch == 'd'):return 4
        if (ch == 'E') | (ch == 'e'):return 5
        if (ch == 'F') | (ch == 'f'):return 6
        if (ch == 'G') | (ch == 'g'):return 7
        if (ch == 'H') | (ch == 'h'):return 8
        if (ch == 'I') | (ch == 'i'):return 9        
        if (ch == 'J') | (ch == 'j'):return 10
        if (ch == 'K') | (ch == 'k'):return 11
        if (ch == 'L') | (ch == 'l'):return 12
        if (ch == 'M') | (ch == 'm'):return 13
        if (ch == 'N') | (ch == 'n'):return 14
        if (ch == 'O') | (ch == 'o'):return 15
        if (ch == 'P') | (ch == 'p'):return 16
        if (ch == 'Q') | (ch == 'q'):return 17        
        if (ch == 'R') | (ch == 'r'):return 18    
        if (ch == 'S') | (ch == 's'):return 19           
        if (ch == 'T') | (ch == 't'):return 20  
        if (ch == 'U') | (ch == 'u'):return 21                
        if (ch == 'V') | (ch == 'v'):return 22   
        if (ch == 'W') | (ch == 'w'):return 23           
        if (ch == 'X') | (ch == 'x'):return 24           
        if (ch == 'Y') | (ch == 'y'):return 25           
        if (ch == 'Z') | (ch == 'z'):return 26           
        
        return -1
    
    def checkString(self,string):
        nSetpOld =0
        nSetpNew =0
        idx = 0
        if string.isalnum() == True:
            for ch in string:                
                if (ch.isalpha() == False)&(idx == 0):                    
                    return False                  
                idx = idx + 1
            return True
        else:
            return False
        
    
        
if __name__ == "__main__":
    test = opSQL()
    test.init_sql("host=192.168.22.18")
    #sqlcmd = "update allmactable set Status = 'unuse' where Status = 'used' "
    sqlcmd = "select * from allmactable  where Status='used'"
    #sqlcmd = "show tables"
    msg = test.update(sqlcmd)
    test.ModifyTable(msg)
    test.close_mysql()
    
    '''
    filepath ='E:\\Simu_server\\auto_conf\\sql_op.xls'
    Sheet= 'SQL_TEST'
    FlowName = 'QUERY_DEMIO'
    
    test.OpMySQL(filepath,Sheet,FlowName)
    '''
    '''
    arg_cmd = 'use CyEms'
    test.execute(None,arg_cmd)
    arg_cmd = 'show tables'
    test.execute(None,arg_cmd)
    arg_cmd = 'select * from topoelement'
    test.execute('中文测试',arg_cmd)
    '''
    #test.close()
    
        