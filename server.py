'''
    program Server
    Author : Noam Tal
    program is used as a server for a client by picking a free port on the computer and connecting the client to the ADDR.
    The client can use some cool commands: getting the weather in Rehovot, Openning a site and getting the time and picking a desert.In order to
    exit a password is needed
'''

from socket import *
import threading
import time
from random import choice
import os
import thread
import subprocess
import math
import select



#gets the ip adress of the computer
def getIp():
    
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    ip=s.getsockname()[0]
    s.close()
    return str(ip)
    

#finding a free port for the communication
def get_open_port():

        s = socket(AF_INET, SOCK_STREAM)
        s.bind(("",0))
        s.listen(1)
        port = s.getsockname()[1]
        print port
        s.close()
        return port

#saving the free port for the communication in a file
def save_free_port():

        #os.chdir('C:')
        f = open(r"getport.txt", "w")
        f.write(str(port))


class server:

    #details
    bufSize= 1024
    serversock = socket(AF_INET, SOCK_STREAM)
    quest_level = 0

    def __init__(self, ip, password, port):
       
        self.ip=ip
        self.port=port
        self.password=password
        self.addr= (ip,port)
        self.serversock.bind(self.addr)
        self.serversock.listen(3)

        self.level_ques_num=2
        self.cur_test=0
        self.can_next=False
        # dictionaries of the questions and their right answer (from the options)
        self.Right_answers= {':which year did WW2 start?' :'1939', ':which year did Israel declared?':'1948', ':Rome was founded in the year ___ ?':'753 BC', ':The Eiffel Tower is built in ________?':'1889'}
        self.Hints= {':which year did WW2 start?' :'the war occured 6 years', ':which year did Israel declared?':'Israel is 71 years old according to 2019, so count yourself :)',
                     ':Rome was founded in the year ___ ?':'guess:753 BC or 622 BC',':The Eiffel Tower is built in ________?':'This tower was build in honor of the Paris 100th World Exhibition of the French Revolution.'}
        # list that every objec of it concludes a list of questins and answers
        self.History_test_1=[ [':which year did WW2 start?','1935','1917','1939','1945'], [':which year did Israel declared?','1946','1948','1956','1962'], ['2'],
         [':Rome was founded in the year ___ ?','753 BC','622 BC','413','928 BC'], [':The Eiffel Tower is built in ________?','1798','1889','1818','1876'] ]


        self.run()

    def check_answer(self,clientsock, question, ans, ques_index):
        
        if ans not in self.History_test_1[ques_index]:
            print len(ans)
            print 'ans-problem', self.History_test_1[ques_index]
            msg= "you have to choose one of the shown answers... believe me one of them is right :)"
            self.can_next= False

        else:
            self.can_next= True
            right_answer= self.Right_answers[question[1:]]
            if right_answer == ans:
                msg='Right'
            else:
                msg='Wrong'

        clientsock.send(msg)

    def handler(self,clientsock,addr):
        while 1:

                    #Trying recieving data, if he cant (the client left) he waits for another connection
                    try:
                        rlist,_,_ = select.select( [clientsock], [], [] )

                    except :
                        print "Oh no! ended communication with ",addr
                        break
   
    
                    data=rlist[0].recv(self.bufSize)
                    data=data.strip()
                    print (data)
   
                    if "SubjHistory" == data:
                        
                        question_answers=self.History_test_1[0]
                        msg= 'History-Level1-1-'+"-".join(question_answers)
                        clientsock.send(msg)
                        
                        #msg= ''
                        #self.quest_level +=1
                        #clientsock.send(msg)
                        #data = clientsock.recv(self.bufSize)
                        #time_check(data)
                        

                    elif 'yes hint' in data:
                        
                        data=data.split("-")
                        question= data[2]
                        question= question[1:]
                        msg='givenhint-'+ self.Hints[question]
                        clientsock.send(msg)
                    
                    elif 'time-end-error' == data:
                        
                        msg='bye'
                        clientsock.send(msg)
                        print "I had to end communication with ",addr
                        break
                        
                    else:       
                       
                        level_len=len(self.History_test_1)
                        data=data.split("-")
                        subj= data[0]
                        level= data[1]
                        level_num= int(level[5:])
                        question= data[2]
                        ques_num= int(question[0])
                        ans= data[3]
                        # the next question index for the history test list
                        ques_index= ques_num+level_num-1

                        self.check_answer(clientsock, question ,ans,ques_index-1)
                        #sennd the next qusteion right next


                        if self.can_next:
                            question_answers=self.History_test_1[ques_index]
                            #checking if we need to pass to the new level
                            
                            if len (question_answers) == 1:
                                
                                level_num+=1
                                level= level[0:5]+str (level_num)
                                question_answers= self.History_test_1[ques_num+level_num-1]
  
                            msg=('{}-{}-{}-{}').format(subj,str(level),ques_num+1,"-".join(question_answers))
                            print msg
                            clientsock.send(msg)



                        
                        # if self.quest_level >0:
                        #     msg= 'History-Level2'
                        #     clientsock.send(msg)
                        #     self.quest_level =0
                            
                        #     msg= '1:which year did Israel declared?'
                        #     self.quest_level +=1
                        #     clientsock.send(msg)
                        #     data = clientsock.recv(self.bufSize)
                        #     self.check_answer(clientsock,'1948',data)

                    # elif 'math' in data:
                        
                    #     msg= 'Level 1 \n \n 1: \n 5*3 + 270/9?'
                    #     self.quest_level +=1
                    #     clientsock.send(msg)
                        
                    #     data = clientsock.recv(self.bufSize)
                    #     self.check_answer(clientsock,'45',data)

                    #     if self.quest_level>0:
                    #         msg= '\n Leve2 \n \n 1: \n (7*2)**2 '
                    #         self.quest_level =0
                    #         clientsock.send(msg)
                    #         self.quest_level +=1
                    #         data = clientsock.recv(self.bufSize)
                    #         self.check_answer(clientsock,'196',data)
                                
 
                    #if "Admin" in data:
                       # msg=''
                       # msg=msg[:-1]
                       # print 'nowwwwwww'
                       # print msg
                       # clientsock.send(msg)
                        
                    #else:

        clientsock.close()

    def run (self):
        while 1:
            print 'waiting for connection...'
            clientsock, self.addr = self.serversock.accept()
            print '...connected from:', self.addr
            thread.start_new_thread(self.handler, (clientsock, self.addr)) 


ip = getIp()
password='Bye'
port= get_open_port()
save_free_port()

ser= server(ip,password,port)
ser.run()



