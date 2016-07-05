import time
import sys


#Set the Timestamp
Timestamp = int(time.time())
file = open('controller.log' , 'w+')
file.write(str(Timestamp)+'\n')

#Set the Flag to 0
file.write('0\n')
file.close()


sys.exit()
