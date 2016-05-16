#!/usr/bin/python

#Library import
import subprocess
import socket
import os
import sys
import time
import random
import threading

#Custom import
from SonarPulse import BasicPulse, RLOCPulse


# Initial Defines
# These should be in a configuration file!!!!

LOGDIR = 'log/'
MAPDIR = 'mappings/'

EIDDIR = './'
EIDv4FILE = 'EIDv4-Current-List.txt'
EIDv6FILE = 'EIDv6-Current-List.txt'

MRDIR = './'
MRv4FILE = 'MRv4-Current-List.txt'
MRv6FILE = 'MRv6-Current-List.txt'

#Variables

MRv4LIST = None

#
# Local Subroutines

#---------------------------------------------------------------->
# Log Directories Bootstrap Check

def CheckDateSubDir(DIR,ID):
    
    #Get Date to check/create directory tree
    TIME = time.gmtime(ID)
    TODAYDIR = str(TIME.tm_year) + '/' + str(TIME.tm_mon) + '/' + str(TIME.tm_mday) +'/'

    #Check if the mappings sub-directory exists, if not create it.
    itexists = os.path.isdir(DIR + TODAYDIR)
    if itexists == False :
        try:
            os.makedirs(DIR + TODAYDIR)
        except os.error:
            print 'Critical Error: Creating ' + DIR + TODAYDIR
            sys.exit(1)



def BootstrapFilesCheck(ID):

    #Check if the log directory LOGDIR exists, if not create it.
    itexists = os.path.isdir(LOGDIR)
    if itexists == False :
        try:
            os.mkdir(LOGDIR)
        except os.error:
            print 'Critical Error: Creating ' + LOGDIR
            sys.exit(1)

    #Check if the mappings sub-directory exists, if not create it.
    itexists = os.path.isdir(LOGDIR + MAPDIR)
    if itexists == False :
        try:
            os.mkdir(LOGDIR + MAPDIR)
        except os.error:
            print 'Critical Error: Creating ' + LOGDIR + MAPDIR
            sys.exit(1)

    CheckDateSubDir(LOGDIR + MAPDIR,ID)

   
   
def LoadList(FILE):
    
    # Load a list of IP addresses and create a random list
    try:
        F = open( FILE, "r" )
    except IOError:
        print 'Critical Error:' + FILE + ' Not Found!!!'
        sys.exit(1)
        
    LLIST = F.read().split('\n')
    F.close()
    
    if LLIST.count('') > 0: 
        #If closing empty line exists remove it
        LLIST.remove('')
        
    # Randomize List so to not follow the same order at each experiment
    random.shuffle(LLIST)
    return LLIST
    

class SonarThread (threading.Thread):
    def __init__(self, threadID, tname, thost, tid, teid, tmrlist, tlogdir):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = tname
        self.host = thost
        self.timeid = tid
        self.eid = teid
        self.mrlist = tmrlist
        self.logdir = tlogdir
    def run(self):
        print 'Starting ' + self.name
#        print self.name + '\t' + self.host + '\t' + `self.timeid` + '\t' + self.eid + '\t' + `self.mrlist` + '\t' + self.logdir 
        for mr in self.mrlist:
#            BasicPulse(self.host, self.timeid , self.eid, mr, self.logdir)
            RLOCPulse(self.host, self.timeid , self.eid, mr, self.logdir)



# Main 
# Identify Machine to Mark Logs
HOST = socket.gethostname()
print 'Host Name => ' + HOST

# Call time 
ID = int(time.time())

BootstrapFilesCheck(ID)

#Load list of IPv4 Map-Resolvers
MRv4LIST = LoadList(MRDIR+MRv4FILE)
#Load list of IPv6 EIDs
MRv6LIST = LoadList(MRDIR+MRv6FILE)

MRLIST = MRv4LIST + MRv6LIST
random.shuffle(MRLIST)

#Load list of IPv4 Map-Resolvers
EIDv4LIST = LoadList(MRDIR+EIDv4FILE)
#Load list of IPv6 EIDs
EIDv6LIST = LoadList(MRDIR+EIDv6FILE)

EIDLIST = EIDv4LIST + EIDv6LIST
random.shuffle(EIDLIST)

threads = []
threadID = 1

for EID in EIDLIST:
    # Create new threads
    tName = 'Thread ' + `threadID`
    thread = SonarThread(threadID, tName, HOST, ID, EID, MRLIST, LOGDIR + MAPDIR)
    thread.start()
    threads.append(thread)
    threadID += 1
    if threading.activeCount() > 110:
        while threading.activeCount() > 100:
            time.sleep(1)
    time.sleep(0.25)


for t in threads:
    t.join()
    
print "Exiting Main Thread"

#    for MR in MRLIST:
#       BasicPulse(HOST, ID, EID, MR, LOGDIR + MAPDIR)


'''




#---------------------------------------------------------------->

#---------------------------------------------------------------->
#  Probe v4 Resolvers
Probe_Resolvers_v4()
{
# Ping and traceroute all v4 resolvers 
# Do not parallelize ping and traceroute otherwise files 
# could be messed up
cat ${RESOLVERFILEv4} | perl ${RANDFILE} | while read resolver
do
    OUTPUT="$LOGDIR$MRDIR$V4DIR/"${HOST}-${resolver}.log
    echo >> $OUTPUT
    echo "--- Round ID $ID ----------------------------------->" >> $OUTPUT
    echo "Date=$DATE" >> $OUTPUT
    echo >> $OUTPUT
    echo "=>Ping" >> $OUTPUT
    ping -n -c 3 $resolver >> $OUTPUT
    echo >> $OUTPUT
    echo "==>Traceroute" >> $OUTPUT
    traceroute -n $resolver 2>> $OUTPUT >> $OUTPUT &
done

} #Probe_Resolvers_v4


#---------------------------------------------------------------->
#  Probe v6 Resolvers
Probe_Resolvers_v6()
{
# Ping and traceroute all resolvers 
# Do not parallelize ping and traceroute otherwise files 
# could be messed up
cat ${RESOLVERFILEv6} | perl ${RANDFILE} | while read resolver
do
    OUTPUT="$LOGDIR$MRDIR$V6DIR/"${HOST}-${resolver}.log
    echo >> $OUTPUT
    echo "--- Round ID $ID ----------------------------------->" >> $OUTPUT
    echo "Date=$DATE" >> $OUTPUT
    echo >> $OUTPUT
    echo "=>Ping" >> $OUTPUT
    ping6 -n -c 3 $resolver >> $OUTPUT
    echo >> $OUTPUT
    echo "==>Traceroute" >> $OUTPUT
    traceroute6 -n $resolver 2>> $OUTPUT >> $OUTPUT &
done

} #Probe_Resolvers_v6



'''