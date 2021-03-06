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


    map_resolver = str('137.194.18.132') # the Map Resolver which will be tested

    # Display the starting Time for the Thread
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

            print('processing ' + Name + '...')
            print('No')
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

            print('processing' + Name + '...')
            print('yes')
        # negative Map Reply
        else:

            print('processing' + Name + '...')
            print('yes')
        #incrementation adresse IP
        network= ipaddress.ip_network(str(map_reply.records[0].eid_prefix))
        a = network.num_addresses
        nextint = int(ipaddress.IPv4Address(Start)) + a
        if nextint <= int(ipaddress.IPv4Address(End)):
           Start = str(ipaddress.IPv4Address(nextint))
           i = i+1
        else:
            break
    # Display the ending  Time for the Thread
    print(time.strftime(' %a , %l:%M%p %z on %b %d, %Y')) # ' 1:36PM EST on Oct 18, 2010'
    print ('scanning done  ' + Name)

if __name__ == '__main__':
    try:

      Threads = []


      Timestamp = int(time.time())





      # Scanning the IP address space which will be tested
      t1 = Thread(target=scan ,args=('Thread1','0.0.0.0' , '153.16.6.255' , Timestamp))



      Threads.append(t1)



      for x in Threads :
          x.start()
      for x in Threads :
          x.join()



      # Display the ending  Time for the crawler
      print(time.strftime(' %a , %l:%M%p %z on %b %d, %Y'))  # ' 1:36PM EST on Oct 18, 2010'

      # Copy the EIDs_Prefix list
      list = open('summary/EID_list_' + str(Timestamp) + '.log', 'r+')
      data = list.readlines()
      list.close()

      # create the current EID_Prefix
      list_current = open('summary/EID_list_' + 'current' + '.log', 'w+')
      list_current.writelines(data)
      list_current.close()
      sys.exit()

    except Exception as e :
      print(e)
      sys.exit()







