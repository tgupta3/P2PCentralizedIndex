import socket
import random
import sys
import os
import glob
from clientdef import *



class serverthread():

	def __init__(self,s):
		self.s=s

	def option(self,choice):
		global clientname
		global clientport
		if(choice=='1'):
			rfc=raw_input("Enter RFC in the form RFCtitle number")
			rfcno=rfc[3:]
			title=lookuptitle(rfcno)
			msg2send="ADD RFC %s P2P-CI/1.0\nHost: %s\nPort: %s\nTitle: %s" %(rfcno,clientname,clientport,title)
			print msg2send
			self.s.send(msg2send)
			print self.s.recv(1024)

		if(choice=='2'):
			rfc=raw_input("Enter RFC to lookup in form RFCnumber")
			rfcno=rfc[3:]
			msg2send="LOOKUP RFC %s P2P-CI/1.0\nHost: %s\nPort: %s" %(rfcno,clientname,clientport)
			print msg2send
			self.s.send(msg2send)
			print self.s.recv(1024)


		if(choice=='3'):
			msg2send="LIST ALL P2P-CI/1.0\nHost: %s\nPort: %s" %(clientname,clientport)
			print msg2send
			self.s.send(msg2send)
			print self.s.recv(1024)


		if(choice=='4'):
			self.s.close()



clientname=socket.gethostname()
clientport=random.randint(49152,65535)
c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#serverip=raw_input("Enter IP: ")
#serverip='3255-a.local'
serverip='3255-a.local'
serverport=7734

c.connect((serverip,serverport))
presentrfc=getrfc()

addtoserver(c,presentrfc,clientname,clientport)
print presentrfc
print "Client name %s with Port number as %s" %(clientname,clientport)
#print "Connected to IP %s" %(serverip)
serverclient=serverthread(c)
while True:
	"""input=sys.stdin.readline()
	c.send(input)
	sys.stdout.write(c.recv(1024))
	sys.stdout.flush()"""
	
	choice=raw_input("Enter choice \n 1:Add RFC \n 2:Lookup RFC \n 3:List RFC\n 4:Quit \n")
	serverclient.option(choice)
	if(choice=='4'): break

	