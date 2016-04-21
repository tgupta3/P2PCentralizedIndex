import socket
import random
import sys
import os
import glob
import threading
import datetime
from clientdef import *
import fcntl


class clientuploadmulti(threading.Thread):

	stopcheck=True

	def __init__(self,conn,clienthost,clientport):
		threading.Thread.__init__(self)
		self.conn=conn
		self.clienthost=clienthost
		self.clientport=clientport
		self.conn.settimeout(2)

	def run(self):
			while (clientuploadmulti.stopcheck):
				try:
					#print "Client thread spawned"	
					recv=self.conn.recv(1024)
					if not recv: break

					print recv
					recv=recv.splitlines()
					if(recv[0].split()[0]=='GET' and recv[0].split()[3]=="P2P-CI/1.0"):

					  rfcnorequired=recv[0].split()[2]
					  t = datetime.datetime.now()
					  filename="rfc"+rfcnorequired+".txt"
					  try:
						f=open(filename,'rb')
						statbuf = os.stat(filename)
						msg2send="P2P-CI/1.0 200 OK\nDate: %s, %s %s %s %s\nOS: %s\nLast-Modified: %s\nContent-length: %s\nContent-Type: text/text\n" %(t.strftime("%a"),t.strftime("%d"),t.strftime("%b"),t.strftime("%Y"),t.strftime("%H:%M:%S"),platform.platform(),statbuf.st_mtime,statbuf.st_size)

						self.conn.send(msg2send)
						bufferread=f.read(1024)
						while(bufferread):
								self.conn.send(bufferread)
								bufferread=f.read(1024)
						self.conn.shutdown(socket.SHUT_WR)
					  except IOError:
						t = datetime.datetime.now()
					   	msg2send1 = "P2P-CI/1.0 400 Bad Request\nDate: %s, %s %s %s %s\nOS: %s" % (t.strftime("%a"),t.strftime("%d"),t.strftime("%b"),t.strftime("%Y"),t.strftime("%H:%M:%S"),platform.platform())
					   	print "File not found"
						self.conn.send(msg2send1)
						self.conn.shutdown(socket.SHUT_WR)
					elif(recv[0].split()[0]=='GET'):
						t = datetime.datetime.now()
						msg2send1 = "P2P-CI/1.0 400 Bad Request\nDate: %s, %s %s %s %s\nOS: %s" % (t.strftime("%a"),t.strftime("%d"),t.strftime("%b"),t.strftime("%Y"),t.strftime("%H:%M:%S"),platform.platform())
						self.conn.send(msg2send1)
						self.conn.shutdown(socket.SHUT_WR)
					else:
						t = datetime.datetime.now()
						msg2send1 = "P2P-CI/1.0 505 Bad Request\nDate: %s, %s %s %s %s\nOS: %s" % (t.strftime("%a"),t.strftime("%d"),t.strftime("%b"),t.strftime("%Y"),t.strftime("%H:%M:%S"),platform.platform())
						self.conn.send(msg2send1)
						self.conn.shutdown(socket.SHUT_WR)
							
				except socket.timeout:
					continue

			self.conn.close()
			print "Connection closed thread"

	def stop(self):
			clientuploadmulti.stopcheck=False


class clientuploadthread(threading.Thread):
	
	stopcheck=True
	connestablish=False
	threadlist=[]

	def __init__(self,s,clienthost,clientport):
		threading.Thread.__init__(self)
		self.s=s
		self.clienthost=clienthost
		self.clientport=clientport
		self.conn=None

		
	def run(self):
		while (clientuploadthread.stopcheck):
				try:	
					#print "Waiting to accept connection"
					self.conn,self.addr=self.s.accept()
					clientuploadthread.connestablish=True
					clientuploadthread.threadlist.append(self.conn)
					print "Client Connected"
					substhread=clientuploadmulti(self.conn,self.clienthost,self.clientport)
					substhread.start()
				except socket.timeout:
					continue
	 	if(clientuploadthread.connestablish):
	 			substhread.stop()
	 			print "Connection Closed"			
				
		
	def stop(self):
			clientuploadthread.stopcheck=False

		



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
			presentrfc.append("RFC"+rfcno)

		if(choice=='2'):
			rfc=raw_input("Enter RFC to lookup in form RFCnumber")
			rfcno=rfc[3:]
			msg2send="LOOKUP RFC %s P2P-CI/1.0\nHost: %s\nPort: %s" %(rfcno,clientname,clientport)
			print msg2send
			self.s.send(msg2send)
			msgrecv=self.s.recv(1024)
			print msgrecv
			msgrecv=msgrecv.splitlines()
			if(msgrecv[0].split()[1]=="200"):
				print "RFC available hurray"
				hostrfcavail=msgrecv[1].split()[-2]   #To Add- Check for condition when rfc is available at multiple peers
				portrfcavail=msgrecv[1].split()[-1]
				for item in presentrfc:
						if item==("RFC"+rfcno):
							print "RFC is already available at the host"
							return
				downstatus=downloadrfc(msgrecv[1].split()[1],hostrfcavail,portrfcavail) 
				if downstatus:
						title=lookuptitle(msgrecv[1].split()[1])
						msg2send="ADD RFC %s P2P-CI/1.0\nHost: %s\nPort: %s\nTitle: %s" %(rfcno,clientname,clientport,title)
						print msg2send
						self.s.send(msg2send)
						print self.s.recv(1024)
			else:
				print"RFC not available at any of the peers"


		if(choice=='3'):
			msg2send="LIST ALL P2P-CI/1.0\nHost: %s\nPort: %s" %(clientname,clientport)
			print msg2send
			self.s.send(msg2send)
			print self.s.recv(1024)
			


		if(choice=='4'):
			self.s.close()






os.system('fuser -k 59994/tcp')
clientname=socket.gethostname()
clientport=random.randint(49152,65535)
#clientport=59994
clientupload=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientupload.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientupload.bind(('',clientport))
clientupload.listen(10)
clientupload.settimeout(5)
clientthread=clientuploadthread(clientupload,clientname,clientport)
clientthread.start()

c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


serverip=raw_input("Enter IP: ")
serverport=7734
c.connect((serverip,serverport))
msg2send="Host: %s\nPort: %s" %(clientname,clientport)
c.send(msg2send)
print msg2send
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

	if(choice=='4'): 
			clientthread.stop()
			sys.exit()

	