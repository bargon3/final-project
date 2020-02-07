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
import sqlite3 as lite
import sys

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


#------------------------------------------------------------------
# class User:

#     #creats user with his name and the level
#     def __init__(self, name, cur_level):
#         self.name= name
#         self.cur_level= cur_level
#         self.history=''

#     def change_cur_level(self,cur_level):
#         self.cur_level=cur_level
        
#     # adding a passed level to the user history
#     # done level example: -history:2
#     def add_history(self, done_level):
#         self.history += done_level


# ------------------------------------------------------------------


class server:
   
    #details
    bufSize= 1024
    serversock = socket(AF_INET, SOCK_STREAM)
    quest_level = 0
    user_id=0

    def __init__(self, ip, password, port):
        
        #user_id+=1

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
        self.Right_answers= {':which year did WW2 start?' :'1939', ':which year did Israel declared?':'1948', ':Rome was founded in the year ___ ?':'753 BC', ':The Eiffel Tower is built in ________?':'1889',
        ':The first newspaper in the world was started by?' :'China', ':Who is known as Man of Blood and Iron?' :'Bismarck', ':Which is considered as oldest civilization of the world?' :'Mesopotamian Civilization',
        ':Who is considered as the master of Greek comedy?' :'Aristophanes', ':Young Italy movement by led by two revolutionaries, One was "Mazzini" and Other was?' :'Garibaldi'    }
        
        #dictionarie of hints to every quesrion
        self.Hints= {':which year did WW2 start?' :'the war occured during 6 years', ':which year did Israel declared?':'Israel is 71 years old according to 2019, so count yourself :)',
                     ':Rome was founded in the year ___ ?':'guess:753 BC or 622 BC',':The Eiffel Tower is built in ________?':'This tower was build in honor of the Paris 100th World Exhibition of the French Revolution.'}
        
        # list that every objec of it concludes a list of questins and answers
        self.History_test_1=[ [':which year did WW2 start?','1935','1917','1939','1945'], [':which year did Israel declared?','1946','1948','1956','1962'],
         [':Rome was founded in the year ___ ?','753 BC','622 BC','413','928 BC'], ['2'], 

         [':The Eiffel Tower is built in ________?','1798','1889','1818','1876'], [':The first newspaper in the world was started by?','Japan','China','USA','India'],
         [':Who is known as Man of Blood and Iron?','Napoleon','Sophocles','Aristophanes','Philip'], ['3'],

         [':Who is considered as the master of Greek comedy?','Aeschylus','Bismarck','Ho Chi Minh','Sir Walter Scott'],
         [':Young Italy movement by led by two revolutionaries, One was "Mazzini" and Other was?','Garibaldi','Victor','Emmanuel','Louis'] ,
         [':Which is considered as oldest civilization of the world?','Mesopotamian Civilization','Harappan Civilization','Chinese Civilization','Egyptain Civilization'], ['4']    ] 
                


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
        return msg

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
                    
                    # data= 'register-Leo-history:1'
                    if 'register' in data:

                        original_msg= data

                        data=data.split("-")
                        name= data[1]
                        curr_level= data[2]
                        cursor.execute('''INSERT INTO users(name, subject, grade, current_level, history)
                        VALUES(?,?,?,?,?)''', (name,'history', 0, curr_level,''))
                        conn.commit()

                        # with lite.connect("test.db") as con:
                        #     cur = con.cursor()
                        #     data=data.split("-")
                        #     name= data[1]
                        #     curr_level= data[2]
                        #     cursor.execute('''INSERT INTO users(name, current_level)
                        #     VALUES(?,?)''', (name,curr_level))
                        #     con.commit()
                        
                        print 'his name is--->'+data[1]
                        
                        
                            
                        if 'History' in original_msg: 
                            
                            question_answers=self.History_test_1[0]
                            msg= 'History-Level1-1-'+"-".join(question_answers)
                            clientsock.send(msg)
                            
                            #msg= ''
                            #self.quest_level +=1
                            #clientsock.send(msg)
                            #data = clientsock.recv(self.bufSize)
                            #time_check(data)
                        

                    elif 'Admin' in data:
                            Admin_handle(self,clientsock,addr,data)
                            
                            
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
                        name=data[4]
                        # the next question index for the history test list
                        ques_index= ques_num+level_num-1

                        feedback= self.check_answer(clientsock, question ,ans,ques_index-1)
                        #sennd the next qusteion right next
                        if feedback== 'Right':
                            cursor.execute('''SELECT grade FROM users WHERE name=?''', (name,))
                            old_grade = cursor.fetchone() # retrieves the next row
                            cursor.execute('''UPDATE users SET grade = ?  WHERE name = ? ''',
                            (int (old_grade[0]) +2, name))

                        if self.can_next:   
                            question_answers=self.History_test_1[ques_index]
                            #checking if we need to pass to the new level
                            
                            if len (question_answers) == 1:
                                
                                # adding to the history (sql)
                                cursor.execute('''SELECT history FROM users WHERE name=?''', (name,))
                                old_history = cursor.fetchone() # retrieves the next row
                                print old_history
                                print type(old_history)
                                new_history= old_history[0]+', succsses at '+ subj+ ':' + str(level_num)
                                cursor.execute('''UPDATE users SET history = ?  WHERE name = ? ''',
                                (new_history, name))
                                
                                #changing to the next level
                                level_num+=1
                                level= level[0:5]+str (level_num)
                                question_answers= self.History_test_1[ques_num+level_num-1]

                                #updating the current level of the user (sql)
                                cur_level= subj+ ':' + str(level_num)
                                cursor.execute('''UPDATE users SET current_level = ?  WHERE name = ? ''',
                                (cur_level, name))
                                
                                conn.commit()

  
                            cursor.execute("SELECT * FROM users") # Fetching data
                            data= ''
                            for row in cursor:
                                msg= "id-> ",row[0]," name-> ",row[1]," subject->",row[2], " grade->", row[3]," current_level->",row[4], " history->", row[5]
                                print msg
                                data+=msg+'//'
                                
                            print data    
                            clientsock.send(msg)    
                                
                            print '-------------------------------------------------------------------'
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
        
    def  Admin_handle(self,clientsock,addr,data):
        
        data= data[5:]
        print ('without' +data)
        
        
        
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


conn = None
file_name='E:\\YB project\\test.db'

conn = lite.connect(file_name)
conn = lite.connect('test.db', check_same_thread=False)

cursor = conn.cursor()
#cursor.execute('''DROP TABLE users''')

#cursor.execute(''' CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, subject Text,
#grade INTEGER, current_level TEXT, history TEXT ) ''')
conn.commit()

ser= server(ip,password,port)
ser.run()



