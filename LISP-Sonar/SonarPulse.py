
#Library import
import sys
import time
import ipaddress
import subprocess
import re

FILEXT = '.log'

# Function performing the actualy measurment
# Input:
#       EID  - EID prefix to check
#       MR   - The resolver to use
#       ID   - Unique ID (actually the Unix Time)
# Output:
#       Output will be written in the file EID.log
#       in the directory year/month/day/, where 
#       the year/month/day is obbtained from the ID 
#       

def BasicPulse(HOST, ID, EID, MR, LOGDIR):
    
    #print HOST + ' (' + str(ID) + '): ' + EID + ' => ' + MR
    
    DATE = time.gmtime(ID)
    # Re-create log file name 
    FILEDIR = LOGDIR +  str(DATE.tm_year) + '/' + str(DATE.tm_mon)  + '/' + str(DATE.tm_mday) + '/' 
    
    try:
        IP = ipaddress.ip_address(EID)
    except ValueError:
        print 'Error!!!!!!!! XXXXX'
    
    FILENAME = 'EIDv' + str(IP.version) + '-' + str(IP).replace('.','_').replace(':','_') + FILEXT
    
    FILE = FILEDIR + FILENAME
  
    try:
        F = open( FILE, "a" )
    except IOError:
        print 'Critical Error:' + FILE + ' !!!'
        sys.exit(1)
    
    F.write('\n---RoundID-<' + str(ID) + '>---HOST-<' + HOST + '>---EID-<' + str(EID) + '>---MR-<' + str(MR) + '>--->\n')
    F.write('Host =\t' + HOST + '\n') 
    F.write('Date =\t'+ str(DATE.tm_mday) + '.' + str(DATE.tm_mon) + '.' + str(DATE.tm_year) + '\n') 
    F.write('Time =\t'+ str(DATE.tm_hour) + ':' + str(DATE.tm_min) + ':' + str(DATE.tm_sec) + '\n') 
    F.write('EID =\t' + str(EID) + '\n')
    F.write('MR =\t'+ str(MR) + '\n')
    
    # The different parameters should be configurable!
    F.write('LIG = lig -b -d -t 3 -c 3 -m ' + str(MR) + '   ' + str(EID) + '\n')
 
    try:
        # Here put real LIG Call
        LIGP = subprocess.Popen(['echo', 'HELLO!'], stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print 'Critical Error: while calling LIG function !!!'
        sys.exit(1)
        
    LIGOUTPUT = LIGP.communicate()[0]
    F.write(LIGOUTPUT)
    
    F.write('\n--------------------------------------------------------------->\n')
    F.close()
    
    
def RLOCPulse(HOST, ID, EID, MR, LOGDIR):
    
    #print HOST + ' (' + str(ID) + '): ' + EID + ' => ' + MR
    
    DATE = time.gmtime(ID)
    # Re-create log file name 
    FILEDIR = LOGDIR +  str(DATE.tm_year) + '/' + str(DATE.tm_mon)  + '/' + str(DATE.tm_mday) + '/' 
    
    try:
        IP = ipaddress.ip_address(EID)
    except ValueError:
        print 'Error!!!!!!!! XXXXX'
    
    FILENAME = 'EIDv' + str(IP.version) + '-' + str(IP).replace('.','_').replace(':','_') + FILEXT
    
    FILE = FILEDIR + FILENAME
  
    try:
        F = open( FILE, "a" )
    except IOError:
        print 'Critical Error:' + FILE + ' !!!'
        sys.exit(1)
    
    F.write('\n---RoundID-<' + str(ID) + '>---HOST-<' + HOST + '>---EID-<' + str(EID) + '>---MR-<' + str(MR) + '>--->\n')
    F.write('Host =\t' + HOST + '\n') 
    F.write('Date =\t'+ str(DATE.tm_mday) + '.' + str(DATE.tm_mon) + '.' + str(DATE.tm_year) + '\n') 
    F.write('Time =\t'+ str(DATE.tm_hour) + ':' + str(DATE.tm_min) + ':' + str(DATE.tm_sec) + '\n') 
    F.write('EID =\t' + str(EID) + '\n')
    F.write('MR =\t'+ str(MR) + '\n')
    
    # The different parameters should be configurable!
    F.write('LIG = lig -b -d -t 3 -c 3 -m ' + str(MR) + '   ' + str(EID) + '\n')
 
    try:
        # Here put real LIG Call
        LIGP = subprocess.Popen(['./lig', '-b', '-d', '-t 5', '-c 3', '-m', str(MR), str(EID)],stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print 'Critical Error: while calling LIG function !!!'
        sys.exit(1)
        
    LIGOUTPUT = LIGP.communicate()[0]
    LIGOUTPUTLines = LIGOUTPUT.split('\n')
    RLOC = None
    for LIGLine in LIGOUTPUTLines:
        if re.match(r"LOCATOR_\d+=", LIGLine):
            if RLOC != None:
                F.write('||LIG = lig -b -d -t 3 -c 3 -m ' + str(RLOC) + '  ' + str(EID) + '\n')
                try:
                    # Here put real LIG Call
                    LIGRLOCP = subprocess.Popen(['./lig', '-b', '-d', '-t 5', '-c 3', '-m', str(MR), str(EID)], stdout=subprocess.PIPE)
                                                 #'-b -d -t 3 -c 3 -m '+str(MR)+' '+str(EID)], stdout=subprocess.PIPE)
                except subprocess.CalledProcessError:
                    print 'Critical Error: while calling LIG function !!!'
                    sys.exit(1)
        
                LIGRLOCOUTPUT = LIGRLOCP.communicate()[0]
                LIGRLOCOUTPUTLines = LIGRLOCOUTPUT.split('\n')
                for LIGRLOCLine in LIGRLOCOUTPUTLines:
                    F.write('||' + LIGRLOCLine + '\n')
            RLOC = LIGLine.split('=')[1]
        F.write('|' + LIGLine + '\n')
    if RLOC != None:
        F.write('||LIG = lig -b -d -t 3 -c 3  -m ' + str(RLOC) + '  ' + str(EID) + '\n')
        try:
            # Here put real LIG Call
            LIGRLOCP = subprocess.Popen(['./lig', '-b', '-d', '-t 5', '-c 3', '-m', str(MR), str(EID)], stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print 'Critical Error: while calling LIG function !!!'
            sys.exit(1)
        
        LIGRLOCOUTPUT = LIGRLOCP.communicate()[0]
        LIGRLOCOUTPUTLines = LIGRLOCOUTPUT.split('\n')
        for LIGRLOCLine in LIGRLOCOUTPUTLines:
            F.write('||' + LIGRLOCLine + '\n')

    F.write('\n--------------------------------------------------------------->\n')
    F.close()
    
    
    
    