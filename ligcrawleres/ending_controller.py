import time
import sys
import os


Time = (5*60*60)+(58*60)
time.sleep(Time)

# Get Timestamp
controller = open('controller.log', 'r')
Timestamp = controller.readline().strip('\n')
controller.close()

os.remove('controller.log')

Time =  1*60
time.sleep(Time)

# Copy the EIDs_Prefix list
list = open('summary/EID_list_' + str(Timestamp) + '.log', 'r+')
data = list.readlines()
list.close()

# create the current EID_Prefix
list_current = open('summary/EID_list_' + 'current' + '.log', 'w+')
list_current.writelines(data)
list_current.close()

os.remove('controller.log')

sys.exit()