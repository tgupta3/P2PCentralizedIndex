import os
import subprocess
import time

temp_file= open('words.txt','r')
process = subprocess.Popen(['python', 'clientp2p.py'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

for line in temp_file:
	
	print line
	process.stdin.write(line)
	output = process.stdout.readline()
	print output
	
	
