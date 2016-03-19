import sys
import subprocess
import glob
import os
import re

"""input = sys.stdin.readline()
sys.stdout.write('Uppercase: %s'%input.upper())
sys.stdout.flush()"""

"""addr='192.168.0.100'
output = subprocess.Popen(["ping","-c3",addr.strip()],stdout = subprocess.PIPE,stderr = subprocess.PIPE).communicate()[0]
print output
if 'Unreachable' in output: print('hi')
else: print "Fuck"""

"""currentdir=os.getcwd()
t=glob.glob(currentdir+"/rfc*.txt")
rfclist=[]
for i in t:
	obj=re.search(r'rfc([0-9]*)',i)
	print obj.group(0)
	rfclist.append(obj.group(0))"""

pattern='0733'
temp_file=open('indexrfc.txt','r')
for line in temp_file:
			obj=re.match(pattern,line)
			if obj:
				print line
				break
			

