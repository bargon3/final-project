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
import base64


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
    bufSize= 8000
    serversock = socket(AF_INET, SOCK_STREAM)
    quest_level = 0
    user_id=0
    users_socket= {}
    users_hints= {}
    users_Time_till_hint= {}
    secret_code = "8642"

    def __init__(self, ip, port):
        
        #user_id+=1
        self.auto_shut= True
        self.ip=ip 
        self.port=port
        self.addr= ( ('',port) )
        self.serversock.bind(self.addr)
        self.serversock.listen(3)

        self.level_ques_num=2
        self.cur_test=0
        self.can_next=False
        self.Time_to_hint= "20"
        self.yes_hint= "True"
        self.admin_sock= None
        self.share_screen_sock= None
        self.end= False
        
        # dictionaries of the questions and their right answer (from the options)
        self.History_right_answers= {':which year did WW2 start?' :'1939', ':which year did Israel declared?':'1948', ':Rome was founded in the year ___ ?':'753 BC', ':The Eiffel Tower is built in ________?':'1889',
        ':The first newspaper in the world was started by?' :'China', ':Who is known as Man of Blood and Iron?' :'Bismarck', ':Which is considered as oldest civilization of the world?' :'Mesopotamian Civilization',
        ':Who is considered as the master of Greek comedy?' :'Aristophanes', ':Young Italy movement by led by two revolutionaries, One was "Mazzini" and Other was?' :'Garibaldi'    }
        
        #dictionarie of hints to every quesrion
        self.History_Hints= {':which year did WW2 start?' :'the war occured during 6 years', ':which year did Israel declared?':'Israel is 71 years old according to 2019, so count yourself :)',
                     ':Rome was founded in the year ___ ?':'guess:753 BC or 622 BC',':The Eiffel Tower is built in ________?':'This tower was build in honor of the Paris 100th World Exhibition of the French Revolution.'}
        
        # list that every object of it concludes a list of questins and answers
        self.History_test_1=[ [':which year did WW2 start?','1935','1917','1939','1945'], [':which year did Israel declared?','1946','1948','1956','1962'],
         [':Rome was founded in the year ___ ?','753 BC','622 BC','413','928 BC'], ['2'], 

         [':The Eiffel Tower is built in ________?','1798','1889','1818','1876'], [':The first newspaper in the world was started by?','Japan','China','USA','India'],
         [':Who is known as Man of Blood and Iron?','Napoleon','Sophocles','Aristophanes','Philip'], ['3'],

         [':Who is considered as the master of Greek comedy?','Aeschylus','Bismarck','Ho_Chi_Minh','Sir_Walter_Scott'],
         [':Young Italy movement by led by two revolutionaries, One was "Mazzini" and Other was?','Garibaldi','Victor','Emmanuel','Louis'] ,
         [':Which is considered as oldest civilization of the world?','Mesopotamian_Civilization','Harappan_Civilization','Chinese_Civilization','Egyptain_Civilization'], ['4']    ] 
         
         
         # list that every object of it concludes a list of questins and answers
        self.English_test= [ [':Yesterday, ......?','she have lunch with my mother','she eat lunch with my mother','she had lunch with my mother','she does lunch with my mother'],
         [':Your sister ......?','is older as you','is older like you','is older than you','is old than you'],
         [':They usually go to work ......?','under train','in train','by train','on train'], ['2'], 

         [':That is ......?','Better restaurant in town','A better restaurant in town','A best restaurant in town','the best restaurant in town'], 
         [':...... is it from Paris to London?','How far','How long','How much distance'], 
         [':...... is your father?','How big','How high','How tall'], ['3'],

         [':...... a cup of tea?','Do you like','How do you like','Would you like'],
         [':Which one is different?','cousin','aunt','dog'] ,
         [':The sofa is ...... the fireplace?','in front of','front'], ['4']    ] 

        # dictionaries of the questions and their right answer (from the options)        
        self.English_right_answers= {':Yesterday, ......?' :'she had lunch with my mother', ':Your sister ......?':'is older than you', ':They usually go to work ......?':'by train', 
        ':That is ......?':'the best restaurant in town', ':...... is it from Paris to London?':'How far', ':...... is your father?' :'How tall', ':...... a cup of tea?' :'Would you like',
         '::Which one is different?' :'dog', ':The sofa is ...... the fireplace?' :'in front of'   }
        

        self.run()

    def check_answer(self,clientsock, question, ans, ques_index, subj):
        
        #checking answewr in history test
        if 'History' in subj:

            if ans not in self.History_test_1[ques_index]:
                print len(ans)
                print 'ans-problem', self.History_test_1[ques_index]
                msg= "you have to choose one of the shown answers... believe me one of them is right :)"
                self.can_next= False
            
            else:
                self.can_next= True
                right_answer= self.History_right_answers[question[1:]]
                if right_answer == ans:
                    msg='Right'
                else:
                    msg='Wrong'

        #checking answewr in english test
        elif 'English' in subj:

            if ans not in self.English_test[ques_index]:
                print len(ans)
                print 'ans-problem', self.English_test[ques_index]
                msg= "you have to choose one of the shown answers... believe me one of them is right :)"
                self.can_next= False
            
            else:
                self.can_next= True
                right_answer= self.English_right_answers[question[1:]]
                if right_answer == ans:
                    msg='Right'
                else:
                    msg='Wrong'

        
        clientsock.send(msg)
        return msg


    def check_exit (self,clientsock,addr,cursor):

        t1= time.ctime()    #  'Tue May 05 22:05:44 2020' 
        t1= t1.split(" ")
        day= t1[0]
        HMS=t1[3]     
        last_entry= day+ ":" + HMS


       

        for key, value in self.users_socket.items():
                if value == clientsock:
                    del self.users_socket[key]
                    cursor.execute('''UPDATE users SET Last_entry = ? WHERE name = ? ''',
                    (last_entry , key))
                    conn.commit()
                    break
        
        if self.share_screen_sock != None:
            if clientsock == self.share_screen_sock:

                self.share_screen_sock= None
                
                if self.admin_sock is not None:

                    self.admin_sock.send("Share_screen_user_gone")                           
                    print ("sent to admin share screen alert")
        
        else:
                if self.admin_sock == clientsock:
                    self.admin_sock= None
                    print ("Admin is out!!!!!")

                    

    def  Admin_handle(self,clientsock,addr,data):

        # getting the requst that comes after the 'Admin_' word, for example: "Admin_update" will give- "update"
        request= data[6:]
        print ('The admin request--->'+ request)
        

        if 'update' in request:
            cursor.execute("SELECT * FROM users") # Fetching data
            table= ''
            for row in cursor:
                msg= " id-{}- name-{}- subject-{}- study_units-{}- current_level-{}- current_question-{}- L_grade-{}- T_grade-{}- history-{}- Last_entry-{} ".format( row[0] ,
                row[1],row[2],row[3],row[4],row[5], row[6], row[7], row[8] , row[10])
                
                table+= str(msg)+'/'

            #cursor.close()
            clientsock.send(table) 
        
        elif "End_test" in request:
            
            print (self.users_socket)
            for key, value in self.users_socket.items():
                self.users_socket[key].send("bye")
            
            self.end= True


        # Time hint change request, example: 'all_Time_till_hint:5'
        elif 'all_Time_till_hint:' in request:
            
            time= data.split(':')[1]
            self.Time_to_hint= time

            for value in self.users_Time_till_hint:
                    self.users_Time_till_hint[value]= time

            #clientsock.send("new_time_hint-" + str( self.Time_to_hint ))
            print ("new_time_hint-" + self.Time_to_hint )
        
        #example: 'private_Time_till_hint-25-Noam'
        elif 'private_Time_till_hint' in request:
            
            request = request.split('-')
            value = request[1]
            name= request[2]
            self.users_Time_till_hint[name] = value

        #example: 'all_Hints:False'
        elif 'all_Hints:' in request:

            need= data.split(':')[1]

            if need is "False" or "True" :
                self.yes_hint = need
                for value in self.users_hints:
                    self.users_hints[value]= need
                    
            else:
                print ('bad input- ' + need )
                msg= 'bad input'
                clientsock.send(msg)
        
        #example: 'private_Hints-False-Noam'
        elif 'private_Hints' in request:
            
            request = request.split('-')
            value = request[1]
            name= request[2]
            self.users_hints[name] = value
            print (self.users_Time_till_hint)
            
        
        elif "Shutdown" in request:
            
            Name= request.split('-')[1]

            try:
                
                wanted_clientsock= self.users_socket[Name]
                msg= "Shutdown , "+ Name
                wanted_clientsock.send(msg)
                print ("Shut down to "+ Name)

            except expression as identifier:
                print (identifier)
                print ("cant shutdown->" + Name)


        elif "auto_shut" in request:

            print ("in????????????????")
            if  "allow" in request:
                print ("allowing auto shut")
                self.auto_shut= True
                
            if  "stop"  in request:
                print ("Stoping auto shut")
                self.auto_shut= False
        
        

        #example: "Share_screen-Noam-63000
        elif "Share_screen" in request:

            Name= request.split('-')[1]
            p = request.split('-')[2]
            try:
                wanted_clientsock= self.users_socket[Name]
                self.share_screen_sock= wanted_clientsock
                msg= "activate_share_screen-"+ p 
                wanted_clientsock.send(msg)
            except:
                print ("He cant share screen")

            print ("Share screen command sent to "+ Name + " ,  port number" + p )
        
        #example: 'private_chat-Noam-Is everything ok?'
        elif "private_chat" in request:

            Name= request.split('-')[1]
            msg= request.split('-')[2]
            wanted_clientsock = self.users_socket[Name]
            #print type(self.users_socket[Name])

            if wanted_clientsock:
                wanted_clientsock.send("Admin_msg-"+msg)
                print ("chat msg send to"+ Name)
            else:
                print "problem"
        
        elif "to_all_Broadcast" in request:

            msg= request.split('-')[1]
            for key, value in self.users_socket.items():
                if value != "":

                    try:
                        self.users_socket[key].send("Admin_msg-" + msg)
                    except Exception as e:
                        print(e)

        elif "Good " in request:

            print (self.admin_sock)
            self.admin_sock.__send("man")
        
                


    def handler(self,clientsock,addr):
        
        while 1:

                    #Trying recieving data, if he cant (the client left) he waits for another connection
                    try:
                        rlist,_,_ = select.select( [clientsock], [], [] )
                        data=rlist[0].recv(self.bufSize)
                        data=data.strip()
                        print ('recieved-'+data)

                        if data == '' :
                             print "He is gone, ended communication with ",addr
                             break
                        
                        elif self.end == True:
                            clientsock.send("The test is over you cant connect")

                    except :
                        
                        print "Oh no! ended communication with ",addr
                        self.check_exit(clientsock,addr, cursor)
                        break
   
                    
                                 
                    if 'user' in data:

                        print ('registering')
                        user= data.split('-')
                        user_name= user[1] 
                        user_password= user[2] 
                        encrypted = base64.b64encode(user_password)

                        cursor.execute('''SELECT password FROM users WHERE name=?''', (user_name,))                      
                        check_profile = cursor.fetchone()
                        #cursor.close()
                        print (check_profile)

                        if len( user_name ) <2:
                            msg= "Name must be at least 2 characters"
                        
                        elif len( user_password ) <2:
                            msg= "password must be at least 2 characters"

                        # if the acount already created, he can continue, but if it it new acount with username that is taken he needs to pick new one
                        elif  check_profile:
                            if  user_password == base64.b64decode ( str(check_profile[0]) ) :                             
                                msg='already_created'
                                #self.users_hints[user_name] = self.yes_hint  
                                #self.users_Time_till_hint [user_name ]= self.Time_to_hint

                            else:
                                msg= 'If you are a new user: Name already taken, please pick a new one. \n if not, wrong password'                      

                        else:
                            cursor.execute('''INSERT INTO users(name,password, Last_entry)
                            VALUES(?,?,?)''', (user_name,encrypted,"Now"))
                            conn.commit()
                            #cursor.close()
                            msg= 'Great'
                            self.users_hints[user_name] = self.yes_hint   
                            self.users_Time_till_hint [user_name ]= self.Time_to_hint 
                        
                        
                        clientsock.send(msg)
                        'sent msg'
                             

                    elif 'Ready' in data:    

                        user= data.split('-')                        
                        user_name= user[0]
                        print ('His profile-' + user_name+ user_password )

                        self.users_socket[user_name]= clientsock

                        cursor.execute('''SELECT subject, current_level, current_question FROM users WHERE name=?''', 
                        (user_name ,))  

                        info= cursor.fetchone()
                       # cursor.close()
                        print (info)

                        if info != None:

                            subj= str(info[0])
                            level_num= int(info[1][1])
                            level= 'Level'+ str(level_num)
                            curr_ques= str(info[2])

                            ques_index= int(curr_ques) +level_num-2
                            if 'H' in subj:
                                subj='History'
                                question_answers=self.History_test_1[ques_index]

                            if 'E' in subj:
                                    subj='English'
                                    question_answers=self.English_test[ques_index]
                                
                            msg=('{}-{}-{}-{}-{}').format(subj,level ,curr_ques,"-".join(question_answers), self.users_Time_till_hint[user_name] )
                            
                            cursor.execute('''UPDATE users SET Last_entry = ? WHERE name = ? ''',
                            ("Now" , user_name))
                            
                        else:

                            msg= "not_registered"
                            print ("old acount no register")
              
                        clientsock.send(msg)

                    
                    # data= register-Noam-History-5
                    elif 'register' in data:

                        original_msg= data
                        #defult msg
                        msg= 'problem'
                        data=data.split("-")
                        name= data[1]
                        subj= data[2]
                        study_units= int (data[3] )                     
                        level_grade= T_grade= 0 
                        curr_question= 1
                        curr_level= '?'                     

                        self.users_socket[name]= clientsock
                                                                       
                        if 'History' in original_msg: 
                            # 3 or 4 points- level 1
                            if study_units==3 or study_units==4:

                                 curr_level= subj[0].upper()+ '1'
                                 question_answers=self.History_test_1[0]
                                 msg= 'History-Level1-1-'+"-".join(question_answers)+ '-' + str( self.Time_to_hint )

                            # 5 points- level 2
                            elif study_units==5:
                                
                                 question_level=3
                                 curr_level= subj[0].upper()+ '2'
                                 question_answers=self.History_test_1[0+question_level+1] # [4]- test number 2
                                 msg= 'History-Level2-4-'+"-".join(question_answers)+ '-' + str( self.Time_to_hint )
                            
                        
                        elif 'English' in original_msg: 
                            
                            # 3 or 4 points- level 1
                            if study_units==3 or study_units==4:

                                 curr_level= subj[0].upper()+ '1'
                                 question_answers=self.English_test[0]
                                 msg= 'English-Level1-1-'+"-".join(question_answers)+ '-' + str( self.Time_to_hint )

                            # 5 points- level 2
                            elif study_units==5:
                                
                                 question_level=3
                                 curr_level= subj[0].upper()+ '2'
                                 question_answers=self.English_test[0+question_level+1] # [4]- test number 2
                                 msg= 'English-Level2-4-'+"-".join(question_answers)+ '-' + str( self.Time_to_hint )

                        cursor.execute('''UPDATE users SET subject = ?, study_units = ?, current_level=?, current_question = ?, L_grade = ?, T_grade = ?, history = ?  WHERE name = ? ''',
                        (subj[0],study_units, curr_level , curr_question, level_grade ,T_grade  ,'', name)  )
                        conn.commit()
                        #cursor.close()
                        print (msg)
                        clientsock.send(msg)

                   
                    elif ('I am Admin'+self.secret_code) in data:
                        print ('Admin connected')
                        self.admin_sock= clientsock
                    
                    # if admin going to the admin handle function    
                    elif 'Admin_' in data:
                        print ('admin sent msg')
                        self.Admin_handle(clientsock,addr,data)
                            
                            
                    elif 'yes hint' in data:

                        print (self.users_hints)
                        print (data)
                        data=data.split("-")
                        user_name = data[0]
                        
                        #Noam- Level3- when is the...- yes hint
                        if self.users_hints[user_name] == "True":
                            
                            try:
                                question= data[3]
                                question= question[1:]
                                msg='givenhint-'+ self.History_Hints[question]
                                clientsock.send(msg)

                            except:
                                 print ("hint problem")
                            
                        else :
                            msg='No hints given'
                            print (msg)
                            clientsock.send(msg)
                    
                    elif 'time-end-error' == data:
                        
                        if self.auto_shut == True:
                            msg='bye'
                            clientsock.send(msg)
                            self.check_exit(clientsock,addr,cursor)
                            print "He passed the time ",addr
                            break

                        else:
                            print ("cant shut down")
                    
                    #example: "User_chat_all-Noam-I am ok" /   #example: "User_chat-Noam-I am ok"
                    elif 'User_chat' in data :
                        
                        if self.admin_sock is not None:
                            self.admin_sock.send( data )

                        #sending all users
                        if "_all" in data:

                            Name= data.split('-')[1]
                            msg= data.split('-')[2]
                            for key, value in self.users_socket.items():

                                if value != "" and key != Name:
                                    try:
                                        self.users_socket[key].send( data )
                                    except Exception as e:
                                        print(e)

                        
                        
                    else:       
                        
                        level_len=len(self.History_test_1)
                        data = data.split("-")
                        print (data)
                        subj= data[0]
                        level= data[1]
                        level_num= int(level[5:])
                        question= data[2]
                        ques_num= int(question[0])
                        ans= data[3]
                        name=data[4]
                        # the next question index for the history test list
                        ques_index= ques_num+level_num-1

                        feedback= self.check_answer(clientsock, question ,ans,ques_index-1, subj)
                        cursor.execute('''SELECT L_grade,T_grade FROM users WHERE name=?''', (name,))
                        old_grades = cursor.fetchone() # retrieves the next row
                        #cursor.close()
                        level_grade= int(old_grades[0])
                        total_grade= int(old_grades[1])

                        #if feedback is 'Right', adding 2 points and sending the next qusteion right next
                        if feedback== 'Right':
                            
                            level_grade= level_grade + 2
                            total_grade= total_grade + 2
                            print "Grades L,T--->  {} , {}".format( level_grade, total_grade)
                            cursor.execute('''UPDATE users SET L_grade = ?, T_grade = ?  WHERE name = ? ''',
                            (level_grade,total_grade, name))
                            #cursor.close()

                        if self.can_next:   

                            if 'History' in subj:
                                question_answers=self.History_test_1[ques_index]
                            if 'English' in subj:
                                 question_answers=self.English_test[ques_index]
                                 
                            
                            #checking if we need to pass to the new level
                            
                            if len (question_answers) == 1:
                                
                                # adding to the history (sql)
                                cursor.execute('''SELECT history FROM users WHERE name=?''', (name,))
                                old_history = cursor.fetchone() # retrieves the next row
                                # adding history, example: 'H1, H2'
                                new_history= old_history[0] + ', ' + subj[0] + str(level_num)
                                cursor.execute('''UPDATE users SET history = ?  WHERE name = ? ''',
                                (new_history, name))
                                #cursor.close()
                                
                                #changing to the next level
                                level_num+=1
                                level= level[0:5]+str (level_num)
                                # if the user did all the questions of a certain level right( 6 points), he will get to the next next level
                                ques_per_level= 3

                                if 'History' in subj:
                                    if level_grade== 6:
                                        ques_num= ques_num + ques_per_level
                                        question_answers= self.History_test_1[ques_num + level_num]
                                        level_num+=1
                                        level= level[0:5]+str (level_num)
                                    else:
                                        question_answers= self.History_test_1[ques_num+level_num - 1]
                                
                                elif 'English' in subj:
                                    if level_grade== 6:
                                        ques_num= ques_num + ques_per_level
                                        question_answers= self.English_test[ques_num + level_num]
                                        level_num+=1
                                        level= level[0:5]+str (level_num)
                                    else:
                                        question_answers= self.English_test[ques_num+level_num - 1]

                                #updating the current level, current question and nullify(0) the level grade of the user (sql)
                                cur_level= subj[0] + str(level_num)
                                cur_ques= ques_num+1
                                cursor.execute('''UPDATE users SET current_level = ? , L_grade=?  WHERE name = ? ''',
                                (cur_level ,0, name))
                                
                                conn.commit()
                                #conn.close()
                                #cursor.close()

  
                           
                            cur_ques= ques_num+1
                            cursor.execute('''UPDATE users SET current_question =?  WHERE name = ? ''',
                            (cur_ques , name))

                            # cursor.execute("SELECT * FROM users") # Fetching data
                            # for row in cursor:
                                
                            #     msg= " id-> {}, name-> {}, subject-> {}, study_units-> {},current_level-> {}, current_question-> {}, L_grade-> {}, T_grade-> {}, history-> {} ".format( row[0] ,
                            #     row[1],row[2],row[3],row[4],row[5], row[6], row[7], row[8] )

                            #     print msg
                                
                            print '-------------------------------------------------------------------'
                            msg=('{}-{}-{}-{}-{}').format(subj,str(level),ques_num+1,"-".join(question_answers), str(self.users_Time_till_hint[name]) )
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
port= get_open_port()
save_free_port()


conn = None
file_name='final_test2.db'

conn = lite.connect(file_name)
conn = lite.connect(file_name, check_same_thread=False)

cursor = conn.cursor()
#cursor.execute('''DROP TABLE users''')

try:
    cursor.execute(''' CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, subject Text,
    study_units Text, current_level TEXT, current_question Text, L_grade INTEGER, T_grade INTEGER, history TEXT, password Text, Last_entry Text ) ''')
    print ('new table')
    
except:
    print ('table already created')
    
conn.commit()
#conn.close()

ser= server(ip,port)
ser.run()



