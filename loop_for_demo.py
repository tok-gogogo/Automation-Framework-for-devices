
import for_demo 
import os,shutil,sys
def loop_for(path='E://ippool.txt'):
    #-----------------------------------------------------------------------------
        # Name:        file_Refresh
        # param:       path:path of users config file 
        # explain:     redefined the loop of "for"
        # Author:      chenzheng
        # 
        # Created:     2013/03/20
        #-----------------------------------------------------------------------
    fileSource = open(path,'r+')
    lines = fileSource.readline()
    linenum = 0
    pathfilebak = path[0:-4]+'_bak'+path[len(path)-4:len(path)]
    tmpfile = open(pathfilebak,'w')
    while len(lines) != 0 :
        linenum +=1
        #print lines
        param_list = []
        filename = ''
        times = 0     
        if lines.find('#for')!=-1:
            while 1:
                lines = fileSource.readline()
                linenum +=1
                if lines.find('for_demo$')!=-1:
                    filename = (lines.split('for_demo$')[1]).split(',[')[0]
                    #print filename
                    times = (lines.split('for_demo$')[1]).split('],')[1]
                    times = int(times)
                    #print times
                    str = (lines.split('for_demo$')[1])[len(filename)+2:-4]
                    #print str
                    tmplist = str.split('  ')
                    #print tmplist
                    tuple1 = ()
                    
                    for str in tmplist :
                        list = str.split(',')
                        #print list
                        dstlist = []
                        dstlist.append(list[0][2:-1])
                        dstlist.append(list[1][1:-1])
                        
                        try:
                            list[2]=int(list[2])
                            list[3]=int(list[3])
                        except :
                            print "change to int fail,so it's string"
                            list[2]=list[2][1:-1]
                            list[3]=list[3][1:-1] 
                            
                        dstlist.append(list[2])
                        dstlist.append(list[3])
                        dstlist.append(int(list[4][0:-1]))
                        tuple1=tuple(dstlist)
                        param_list.append(tuple1)
                        #print dstlist
                        #print tuple1
                    
                    #print param_list
                    #print filename.split(' ')[-1]
                    for_demo.for_demo(filename.split(' ')[-1],"e:\\result_ippool.txt",param_list,times)

                    
                if lines.find('#endfor')!=-1:
                    #find the position and replace the 'for' loop   
                    lines = fileSource.readline()
                    linenum +=1                                     
                    fileRe = open("e:\\result_ippool.txt",'r')
                    str = fileRe.read()
                    fileRe.close()            
                    tmpfile.write(str)
                    break
        tmpfile.write(lines)   

        lines = fileSource.readline()
    #print linenum
    tmpfile.close()
    fileSource.close()
    shutil.copy(pathfilebak,path)
    os.remove(pathfilebak)
if __name__=='__main__':
    loop_for()
    