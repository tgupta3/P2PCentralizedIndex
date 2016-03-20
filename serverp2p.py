import socket
import fcntl
import struct
import threading
import os
import subprocess


class peerlist():
	
	def __init__(self,host,port):
		self.host=host
		self.port=port
	
	@staticmethod
	def addpeer(host,port):
		
		print "Adding Peer"
		for i in activepeers:
				if(i.host==host and i.port==port):
					print "Peer Already Exist"
					return
				
		print "Peer Added"					
		activepeers.append(peerlist(host,port))

	@staticmethod
	def removepeer(host,port):
		
		for i in activepeers:
			if(i.host==host and i.port==port):
					print "Removing peer"
					activepeers.remove(i)


	@staticmethod
	def displaypeer():
		for i in activepeers:
			print "Host= %s with Port= %s"%(i.host,i.port)

class rfclist():
	def __init__(self,rfcno,title,host,port):
		self.rfcno=rfcno
		self.title=title
		self.host=host
		self.port=port

	@staticmethod
	def addrfc(rfcno,title,host,port):
		for r in rfcavail:
			if r.rfcno==rfcno:
				if r.host==host and r.port==port :
					return

		rfcavail.append(rfclist(rfcno,title,host,port))
		print "RFC added"

	@staticmethod
	def displayrfc():
		for r in rfcavail:
			print "RFC No=%s with Title=%s is available at host=%s with port %s"%(r.rfcno,r.title,r.host,r.port)

	@staticmethod
	def removerfc(host,port):
		print "Removing RFC"
		delindex=[]
		for i,r in enumerate(rfcavail):
			if (r.host==host and r.port==port):
				delindex.append(i)
		
		if not delindex:
			print "No rfc to be removed"
			return
		
		for i in reversed(delindex):
				del rfcavail[i]
					
		

class threadclient(threading.Thread):
	def __init__(self,connsocket,addr):
		threading.Thread.__init__(self)
		self.connsocket=connsocket
		self.addr=addr
		recv=self.connsocket.recv(1024)
		linelist=recv.splitlines()
		self.peerhost=(linelist[0])[6:]
		self.peerport=(linelist[1])[6:]
		peerlist.addpeer(self.peerhost,self.peerport)
		print "Client- "+self.addr[0]+" connected"
		
		
	def run(self):
		while True:
				recv=self.connsocket.recv(1024)
				if not recv: break
				#print recv
				lines=recv.splitlines()
				
				if(lines[0].split()[0]=="ADD"):
					rfcnorecv=lines[0].split()[2]
					titlerecv=' '.join(lines[3].split()[1:])
					peerlist.addpeer(self.peerhost,self.peerport)
					rfclist.addrfc(rfcnorecv,titlerecv,self.peerhost,self.peerport)
					msg2send="P2P-CI/1.0 200 OK\nRFC %s %s %s %s"%(rfcnorecv,titlerecv,self.peerhost,self.peerport)
					self.connsocket.send(msg2send)		
								

				elif (lines[0].split()[0]=='LIST'):
					self.connsocket.send(listmsg())
	
				
				elif (lines[0].split()[0]=='LOOKUP'):
					rfcnotolookup=lines[0].split()[2]
					indexrfc=[]
					for i,r in enumerate(rfcavail):
						if(r.rfcno==rfcnotolookup):
							indexrfc.append(i)
					if not indexrfc:
						self.connsocket.send("Not found")
					else:
						self.connsocket.send(lookupmsg(indexrfc))				
				
				else:
					self.connsocket.send("error")
				
			 
		self.connsocket.close()
		print "Client- "+str(self.addr[0])+" Closed"
		peerlist.removepeer(self.peerhost,self.peerport)
		rfclist.removerfc(self.peerhost,self.peerport)
		peerlist.displaypeer()
		rfclist.displayrfc()


def listmsg():
	global rfcavail
	basemsg="P2P-CI/1.0 200 OK"
	msg2send=basemsg
	for r in rfcavail:
		msg2send+='\n'
		msgnxtline="RFC %s %s %s %s"%(r.rfcno,r.title,r.host,r.port)
		msg2send+=msgnxtline
	#print len(msg2send.splitlines())
	return msg2send	

def lookupmsg(indexrfc):
	global rfcavail
	msg2send="P2P-CI/1.0 200 OK"
	for r in indexrfc:
		msg2send+='\n'
		msgnxtline="RFC %s %s %s %s"%(rfcavail[r].rfcno,rfcavail[r].title,rfcavail[r].host,rfcavail[r].port)
		msg2send+=msgnxtline
	return msg2send

def get_ip_address(ifname):
	 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	 return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24])

#servername=get_ip_address('eth0')

servername=socket.gethostbyname(socket.gethostname())
port=7734

os.system('fuser -k 7734/tcp')
activepeers=[]
rfcavail=[]

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
