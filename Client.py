'''
    program Client
    Author : Noam Tal
    program is used as a client for a client by getting a free port that the server chose and having a communication with the server.
    The client can use some cool commands: getting the weather in Rehovot, Openning a site and getting the time and picking a desert.In order to
    exit a password is needed
'''

from Tkinter import *
from socket import *
import os
import select
import math
import time
import thread
import time
#from Admin import start

#connecting window 
# def connecting(event):
#     password=entry1.get()

#     if password =='Legend':
#         root2.destroy()
#         start()
#         quit()
#     else:
#         wrong= Label(root2, text=" Wrong password, try again or login as regular acount", fg='red')
#         wrong.grid(row=2,columnspan=5)

#     return password


#getting the free port             
def read_free_port():
   os.chdir('C:')
   f = open("getport.txt", "r")
   return int(f.read())

def getIp():
    
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    ip=s.getsockname()[0]
    s.close()
    return str(ip)

class client:

   tcpCliSock = socket(AF_INET, SOCK_STREAM)
   #details
   bufSize= 1024
   end_msg = "I dont belive you *******"
   cli_num=0

   def __init__(self,ip,port):
      self.ip=ip
      self.port=port
      self.addr= (ip,port)
      self.tcpCliSock.connect(self.addr)
      client.cli_num+=1
      self.time_handle=False
      self.communication()

   # def sendMsg (self,data): 
   #  if not data:tcpCliSock.close()
   #  self.tcpCliSock.send(data)

   def communication(self):

      print ('write the subject you want to be tested on? History/ math')
      data= raw_input('> ')   
      check= False

      while check== False:
         
         if 'history' in data or 'math' in data :
            self.tcpCliSock.send(data)
            check=True
            
         else:
            print ('There is no such option')
            data= raw_input('> ')
              
      print ('ok, we can start')
      
      while 1:

         try:
            #rlist,_,_ = select.select( [self.tcpCliSock], [], [], 20 )
            data= self.tcpCliSock.recv(self.bufSize)

         except:
             print ("ammm, communication problem....")
             break


         #If there is no data the server is gone...
         
         print ('.......')
         #data=rlist[0].recv(self.bufSize)
         print (data)
         thread.start_new(self.get_input, ())
         


         """
         # start = time.time()
         # end = time.time()
         # t= end - start
               
               #while not self.time_handle:
                  #end = time.time()
                  #t= end - start
                  #if t==10:
                  #   print '10 sec'
                      #msg="error: 10 seconds passed..."
                      #self.tcpCliSock.send(msg)
                      #data = self.tcpCliSock.recv(self.bufSize)
                      #print (data)

               #print "kein"
         """
                     
                  
         # else:
         #    print ("There was a problem")
         #    break

   def get_input(self):

      data = raw_input('> ')
      #self.time_handle=True
      try:
         self.tcpCliSock.send(data)
         data= self.tcpCliSock.recv(self.bufSize)
         print (data)
      except error:
         print ("The server decided you do not worth it")



   
      


ip = getIp()
MyCly= client( ip,read_free_port() )




