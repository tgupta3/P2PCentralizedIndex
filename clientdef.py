import socket
import random
import sys
import os
import glob
import re
import platform
import fcntl
import struct

def getrfc():
	currentdir=os.getcwd()
	rfclist=glob.glob(currentdir+"/rfc*.txt")
	rfcpre=[]
	for i in rfclist:
		
		obj=re.search(r'rfc([0-9]*)',i)

		if (not obj): 
			print "No RFC present"
			break
		else : 
			rfcpre.append((obj.group(0)).upper())
	return rfcpre


def addtoserver(c,presentrfc,clientname,clientport):
	print "Adding to server"
	for i in presentrfc:
		rfcno=i[3:]
		title=lookuptitle(rfcno)
		msg2send="ADD RFC %s P2P-CI/1.0\nHost: %s\nPort: %s\nTitle: %s" %(rfcno,clientname,clientport,title)
		print msg2send
		c.send(msg2send)
		print c.recv(1024)
		

def lookuptitle(rfcno):
	rfcno=rfcno.zfill(4)

	temp_file=open('indexrfc.txt','r')
	for line in temp_file:
			obj=re.match(rfcno,line)
			if obj:
				index2=line.find('.')
				index1=line.find(" ")
				return line[index1+1:index2]

def downloadrfc(rfcdown,cienthost,clientport):
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	clientip=cienthost
	clport=int(clientport)
	s.connect((clientip,clport))
	msg2send="GET RFC %s P2P-CI/1.0\nHost: %s\nOS: %s" %(rfcdown,socket.gethostname(),platform.platform())
	newrfcrecv="rfc"+rfcdown+".txt"
	filesave=open(newrfcrecv,'wb')
	s.send(msg2send)
	filerecv=s.recv(1024)
	print filerecv
	while(filerecv):
			filesave.write(filerecv)
			filerecv=s.recv(1024)
			print filerecv
	filesave.close()
	print "File recieve completed"
	s.close()
	return True

def get_ip_address(ifname):
	 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	 return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24])