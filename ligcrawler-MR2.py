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


def scan( Name , Start , End , Timestamp):


    map_resolver = str('198.6.255.40')

    # Display the starting Time
    print('Thread ' + Name + ' started ' + time.strftime(' %a , %l:%M%p %z on %b %d, %Y')) # ' 1:36PM EST on Oct 18, 2010'

    i=1
    # Getting random port number
    port_source = random.choice(range(MIN_EPHEMERAL_PORT, 65535))
    while ipaddress.ip_address(Start) <= ipaddress.ip_address(End):

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
            display_information.display(None , 0, Start, map_resolver, ip_my , Timestamp=Timestamp , rtt= None , sender_addr= None  )
            print('processing ' + Name + '...')
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
            display_information.display(map_reply , 1 , Start , map_resolver , ip_my , rtt , sender_addr , Timestamp )
            print('processing' + Name + '...')
        # negative Map Reply
        else:
            display_information.display(map_reply, -1, Start , map_resolver , ip_my , rtt , sender_addr , Timestamp)
            print('processing' + Name + '...')
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
    print ('scanning done  ' + Name)

if __name__ == '__main__':
    try:

      Threads = []
      #Get Timestamp
      controller = open('controller.log' , 'r')
      Timestamp = controller.readline().strip('\n')

      #create the EID_Prefix list
      #list = open('EID_list_' + str(Timestamp) + '.log', 'w+')



      t1 = Thread(target=scan ,args=('Thread1','0.0.0.0'     , '153.16.6.255' , Timestamp))
      t2 = Thread(target=scan, args=('Thread2','153.16.7.0'   , '153.16.17.255' , Timestamp))
      t3 = Thread(target=scan, args=('Thread3', '153.16.18.0', '153.16.25.255' , Timestamp))
      t4 = Thread(target=scan, args=('Thread4','153.16.26.0' , '153.16.39.255' , Timestamp ))
      t5 = Thread(target=scan, args=('Thread5','153.16.40.0', '153.16.54.255' , Timestamp ))
      t6 = Thread(target=scan, args=('Thread6','153.16.55.0', '153.16.120.255' , Timestamp ))
      t7 = Thread(target=scan, args=('Thread7','153.16.121.0', '153.16.144.255' , Timestamp ))
      t8 = Thread(target=scan, args=('Thread8','153.16.145.0', '153.16.150.255' , Timestamp))
      t9 = Thread(target=scan, args=('Thread9','153.16.151.0', '153.16.155.255' , Timestamp))
      t10 = Thread(target=scan, args=('Thread10', '153.16.156.0', '255.255.255.255', Timestamp))
      # t11 = Thread(target=scan,args=('Thread11','153.16.203.0'  , '255.255.255.255' , Timestamp))


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
      #Threads.append(t11)

      for x in Threads :
          x.start()
      for x in Threads :
          x.join()




      print(time.strftime(' %a , %l:%M%p %z on %b %d, %Y'))  # ' 1:36PM EST on Oct 18, 2010'
      # Copy the EIDs_Prefix list
      list = open('EID_list_' + str(Timestamp) + '.log', 'r+')
      data = list.readlines()
      list.close()

      # create the current EID_Prefix
      list_current = open('EID_list_' + 'current' + '.log', 'w+')
      list_current.writelines(data)
      list_current.close()
      sys.exit()

    except Exception as e :
      print(e)
      sys.exit()







