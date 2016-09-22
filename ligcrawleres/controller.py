import time
import sys
import os


#Set the Timestamp
Timestamp = int(time.time())
file = open('controller.log' , 'w+')
file.write(str(Timestamp)+'\n')

#Set the Flag to 0
file.write('0\n')


sys.exit()
