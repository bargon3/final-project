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

        os.chdir('C:')
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
        self.quest_level = 0
        self.run()

    def check_answer(self,clientsock,right_answer,data):

        if right_answer in data:
            msg='Right'
        else:
            msg='Wrong'

        clientsock.send(msg)


    def time_check(self,data):
        if 'error' in data:
            if '10' in data:
                msg= 'what do you say about moving to the next question?'
                clientsock.send(msg)
                data = clientsock.recv(self.bufSize)
        else:
            return False

    def handler(self,clientsock,addr):
        while 1:

                    #Trying recieving data, if he cant (the client left) he waits for another connection
                    try:
                        rlist,_,_ = select.select( [clientsock], [], [] )

                    except :
                        print "Oh no! ended communication with ",addr
                        break
   

                    data=rlist[0].recv(self.bufSize)
                    print (data)
                    if 'history' in data:

                        msg= 'History-Level1'
                        clientsock.send(msg)
                        
                        msg= '1:which year did WW2 start?'
                        self.quest_level +=1
                        clientsock.send(msg)
                        
                        data = clientsock.recv(self.bufSize)
                        #time_check(data)
                            
                        self.check_answer(clientsock,'1939',data)

                        if self.quest_level >0:
                            msg= 'History-Level2'
                            clientsock.send(msg)
                            self.quest_level =0
                            
                            msg= '1:which year did Israel declared?'
                            self.quest_level +=1
                            clientsock.send(msg)
                            data = clientsock.recv(self.bufSize)
                            self.check_answer(clientsock,'1948',data)

                    elif 'math' in data:
                        
                        msg= 'Level 1 \n \n 1: \n 5*3 + 270/9?'
                        self.quest_level +=1
                        clientsock.send(msg)
                        
                        data = clientsock.recv(self.bufSize)
                        self.check_answer(clientsock,'45',data)

                        if self.quest_level>0:
                            msg= '\n Leve2 \n \n 1: \n (7*2)**2 '
                            self.quest_level =0
                            clientsock.send(msg)
                            self.quest_level +=1
                            data = clientsock.recv(self.bufSize)
                            self.check_answer(clientsock,'196',data)
                                
 
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


