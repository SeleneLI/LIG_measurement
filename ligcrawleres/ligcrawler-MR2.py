from __future__ import unicode_literals
import sys
import time
import socket
import ipaddress
from threading import Thread
from lispy import display_information
from ipaddress import IPv4Address, IPv4Network
from lispy.utils import *
from lispy.lisp import MapRequestMessage, EncapsulatedControlMessage, MapReplyMessage
from lispy.ip import IPv4Packet, IPv6Packet, UDPMessage
from numpy import*


def scan( Name , Start , End , Timestamp ,port_source):


    map_resolver = str('198.6.255.40')

    # Display the starting Time
    print('Thread ' + Name + ' started ' + time.strftime(' %a , %l:%M%p %z on %b %d, %Y')) # ' 1:36PM EST on Oct 18, 2010'

    i=1
    # Getting random port number
    #port_source = random.choice(range(MIN_EPHEMERAL_PORT, 65535))
    while ipaddress.ip_address(Start) <= ipaddress.ip_address(End):

        try:
           open('controller.log', 'r+')
           #flag = controller .readlines()
           #if len(flag) != 0:
           #   if flag[2] == 'stop\n':
           #       sys.exit()
        except:
            print(map_resolver + 'have been stopped')
            sys.exit()
        # Resolve IP from name
        try:
            mr_addr = socket.getaddrinfo(map_resolver, LISP_CONTROL_PORT, 0, 0, socket.SOL_UDP)
            eid_addr = socket.getaddrinfo( Start, 0, 0, 0, socket.SOL_UDP)

        except:
             print('ERROR: invalid addresses')
             sys.exit()


        # Converting ip string TO IPV4/6Address object
        ip_map_resolve = ipaddress.ip_address(mr_addr[0][4][0])
        ip_eid = ipaddress.ip_address(eid_addr[0][4][0])

        # Get our IP Address, our address must be routable on the interne
        ip_my = ipaddress.ip_address(get_my_ipaddress())
        ip_my6 = ipaddress.ip_address(get_my_ipaddress6())

        # generate a nonce
        nonce = get_a_nonce()

        # Building the LISP Control Message (lcm)
        lcm = MapRequestMessage(eid_prefix=ip_eid, itr_rloc=ip_my, nonce=nonce)

        # Building UDP Header
        udp = UDPMessage(source_port=port_source, destination_port=LISP_CONTROL_PORT, payload=lcm)

        # Building Inner IP Header
        # Computing udp checksum, checksum is only mandatory in IPV6
        if isinstance(ip_eid, IPv4Address):
            ih = IPv4Packet(source=ip_my, destination=ip_eid, payload=udp, protocol=IPPROTO_UDP)
            udp.checksum = udp.calculate_checksum(source=ip_my, destination=ip_eid)

        else:
            ih = IPv6Packet(source=ip_my6, destination=ip_eid, payload=udp, next_header=IPPROTO_UDP)
            udp.checksum = udp.calculate_checksum(source=ip_my6, destination=ip_eid)

        # Building LISP Header
        lh= EncapsulatedControlMessage(payload=ih)

        #UDP AND the Outer IP Header (OH) are built by the kernel

        # Creating the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((str(ip_my),port_source))


        # set a 3 sec timeout
        sock.settimeout(3)
        try:
            # Send the request and wait for the reply
            before = time.time()
            sock.sendto(lh.to_bytes(), mr_addr[0][4])
            data, sender_addr = sock.recvfrom(512)
            after = time.time()
            rtt = (after - before)* 1000

        except socket.timeout:
            #display_information.display(None , 0, Start, map_resolver, ip_my , Timestamp=Timestamp , rtt= None , sender_addr= None , resolver_num=3 )
            #print('processing ' + map_resolver + '  ' + Name + '...' + Start)
            nextint = int(ipaddress.IPv4Address(Start)) + 1
            if nextint <= int(ipaddress.IPv4Address(End)):
                Start= str(ipaddress.IPv4Address(nextint))
                i = i + 1
            else:
                break
            continue

        # PRINT THE MAPPING ENTRY#
        map_reply = MapReplyMessage.from_bytes(data)

        # LISP Map Reply, there are records
        if len(map_reply.records[0].locator_records) != 0:
            display_information.display(map_reply , 1 , Start , map_resolver , ip_my , rtt , sender_addr , Timestamp , resolver_num=3 )
            #print('processing ' + map_resolver + '  ' + Name + '...' + Start)
        # negative Map Reply
        else:
            display_information.display(map_reply, -1, Start , map_resolver , ip_my , rtt , sender_addr , Timestamp , resolver_num=3)
            #print('processing ' + map_resolver + '  ' + Name + '...' + Start)
        #incrementation adresse IP
        network= ipaddress.ip_network(str(map_reply.records[0].eid_prefix))
        a = network.num_addresses
        nextint = int(ipaddress.IPv4Address(Start)) + a
        if nextint <= int(ipaddress.IPv4Address(End)):
           Start = str(ipaddress.IPv4Address(nextint))
           i = i+1
        else:
            break

    print(time.strftime(' %a , %l:%M%p %z on %b %d, %Y')) # ' 1:36PM EST on Oct 18, 2010'
    print ('scanning done  ' + map_resolver + '  '+ Name)

if __name__ == '__main__':
    try:
      time.sleep(30)
      Threads = []
      port_source = 32968#35268
      #Get Timestamp
      controller = open('controller.log' , 'r')
      Timestamp = controller.readline().strip('\n')

      #create the EID_Prefix list
      #list = open('EID_list_' + str(Timestamp) + '.log', 'w+')



      # Scanning the IPs from 0.0.0.0 to 255.255.255.255
      t1 = Thread(target=scan ,args=('Thread1','0.0.0.0'     , '153.16.6.255' , Timestamp ,port_source ))
      t2 = Thread(target=scan, args=('Thread2','153.16.7.0'   , '153.16.27.255' , Timestamp ,port_source+1))
      t3 = Thread(target=scan, args=('Thread3', '153.16.28.0', '153.16.48.255' , Timestamp ,port_source+2))
      t4 = Thread(target=scan, args=('Thread4','153.16.49.0' , '153.16.69.255' , Timestamp ,port_source+3 ))
      t5 = Thread(target=scan, args=('Thread5','153.16.70.0', '153.16.90.255' , Timestamp  ,port_source+4))
      t6 = Thread(target=scan, args=('Thread6','153.16.91.0', '153.16.111.255' , Timestamp  ,port_source+5))
      t7 = Thread(target=scan, args=('Thread7', '153.16.112.0', '153.16.132.255', Timestamp ,port_source+6))
      t8 = Thread(target=scan, args=('Thread8','153.16.133.0', '153.16.153.255' , Timestamp ,port_source+7 ))
      t9 = Thread(target=scan, args=('Thread9','153.16.154.0', '153.16.174.255' , Timestamp ,port_source+8))
      t10 = Thread(target=scan, args=('Thread10','153.16.175.0', '153.16.195.255' , Timestamp ,port_source+9))
      t11 = Thread(target=scan,args=('Thread11','153.16.196.0', '153.16.216.255' , Timestamp ,port_source+10))
      t12 = Thread(target=scan, args=('Thread12', '153.16.217.0', '153.16.237.255', Timestamp ,port_source+11))
      t13 = Thread(target=scan, args=('Thread13', '153.16.238.0', '153.16.250.255', Timestamp ,port_source+12))
      t14 = Thread(target=scan,args=('Thread14','153.16.251.0'  , '255.255.255.255' , Timestamp ,port_source+13))

      Threads.append(t1)
      Threads.append(t2)
      Threads.append(t3)
      Threads.append(t4)
      Threads.append(t5)
      Threads.append(t6)
      Threads.append(t7)
      Threads.append(t8)
      Threads.append(t9)
      Threads.append(t10)
      Threads.append(t11)
      Threads.append(t12)
      Threads.append(t13)
      Threads.append(t14)

      for x in Threads :
          x.start()
      for x in Threads :
          x.join()




      print(time.strftime(' %a , %l:%M%p %z on %b %d, %Y'))  # ' 1:36PM EST on Oct 18, 2010'

      sys.exit()

    except Exception as e :
      print(e)
      sys.exit()







