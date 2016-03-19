import socket
import fcntl
import struct
import threading
import os
import subprocess


class threadclient(threading.Thread):
	def __init__(self,connsocket,addr):
		threading.Thread.__init__(self)
		self.connsocket=connsocket
		self.addr=addr
		print "Client- "+self.addr[0]+" connected"
	def run(self):
		while True:
		     	recv=self.connsocket.recv(1024)
			print recv
			if not recv: break
			self.connsocket.send(recv)
			#print "Packet Sent"
		     
				
				
			
		self.connsocket.close()
		print "Client- "+str(self.addr[0])+"Closed"

def get_ip_address(ifname):
	 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   	 return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24])

#servername=get_ip_address('eth0')
servername=socket.gethostbyname(socket.gethostname())
port=7734

os.system('fuser -k 7734/tcp')


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',port)) #Listening on all available interface, to select interface comment out the above code
print "Server is listening on %s with port number %d" %(servername,port)
print "Now waiting for Incoming Connection "
s.listen(10)
while True:
	connsocket,addr=s.accept()
	initthread=threadclient(connsocket,addr)
	initthread.start()
		