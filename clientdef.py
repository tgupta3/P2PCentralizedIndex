import socket
import random
import sys
import os
import glob
import re


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