from __future__ import unicode_literals
import sys
import time
import socket
import ipaddress
from threading import Thread
from lispy import display_information , display_information_B
from ipaddress import IPv4Address, IPv4Network
from lispy.utils import *
from lispy.lisp import MapRequestMessage, EncapsulatedControlMessage, MapReplyMessage
from lispy.ip import IPv4Packet, IPv6Packet, UDPMessage
from numpy import*


def scan( Name , Timestamp , dst_EIDs , map_resolver):



    # Display the starting Time
    print('Thread ' + Name + ' started ' + time.strftime(' %a , %l:%M%p %z on %b %d, %Y')) # ' 1:36PM EST on Oct 18, 2010'

    i=1
    # Getting random port number
    port_source = random.choice(range(MIN_EPHEMERAL_PORT, 65535))
    for dst_EID_Prefix in dst_EIDs:
      for dst_EID in list(ipaddress.ip_network(dst_EID_Prefix)):
        # Convert to string
        dst_EID = str(dst_EID)
        # Resolve IP from name
        try:
            mr_addr = socket.getaddrinfo(map_resolver, LISP_CONTROL_PORT, 0, 0, socket.SOL_UDP)
            eid_addr = socket.getaddrinfo( dst_EID, 0, 0, 0, socket.SOL_UDP)

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
            display_information_B.display(None , 0, dst_EID, map_resolver, ip_my , Timestamp=Timestamp , rtt= None , sender_addr= None  )
            print('processing ' + Name + '...')
            continue

        # PRINT THE MAPPING ENTRY#
        map_reply = MapReplyMessage.from_bytes(data)

        # LISP Map Reply, there are records
        if len(map_reply.records[0].locator_records) != 0:
            display_information_B.display(map_reply , 1 , dst_EID , map_resolver , ip_my , rtt , sender_addr , Timestamp )
            print('processing' + Name + '...')
            break
        # negative Map Reply
        else:
            display_information_B.display(map_reply, -1, dst_EID , map_resolver , ip_my , rtt , sender_addr , Timestamp)
            print('processing' + Name + '...')
            break


    print(time.strftime(' %a , %l:%M%p %z on %b %d, %Y')) # ' 1:36PM EST on Oct 18, 2010'
    print ('scanning done  ' + Name)

if __name__ == '__main__':
    try:
      i = 0
      Threads = []
      dst_EID = []

      #Get Timestamp
      Timestamp = int(time.time())

      # Getting the EID_Prefix list
      list_current = open('EID_list_current.log', 'r')
      data = list_current.read().split()
      while i < len(data) :
          dst_EID.append(data[i])
          i = i+3

      list_current.close()


      scan('Thread1', Timestamp , dst_EID , str('149.20.48.77'))



      print(time.strftime(' %a , %l:%M%p %z on %b %d, %Y'))  # ' 1:36PM EST on Oct 18, 2010'
      sys.exit()

    except Exception as e :
      print(e)
      sys.exit()








