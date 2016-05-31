#-*- coding: UTF-8 -*-  
import   poplib   
import   cStringIO   
import   email   
import   base64   

class popu3:
    def __init__(self,POP3SERVER='192.168.27.89',USERNAME='gongke',PASSWORD='gongke'):
        self.pop3server = POP3SERVER
        self.username = USERNAME
        self.password = PASSWORD
        self.mail_m = poplib.POP3(self.pop3server)
        self.mail_m.user(self.username)
        self.mail_m.pass_(PASSWORD)
    
    def mail_receive(self):
        numMessages=len(self.mail_m.list()[1])
        print   'num   of   messages',   numMessages
        return True

    def close(self):
        self.mail_m.quit()
        
if __name__=='__main__':
    test_mail = popu3()
    print "111111"