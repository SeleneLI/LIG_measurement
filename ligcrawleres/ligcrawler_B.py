from __future__ import unicode_literals
import sys
import time
import re
import socket
import ipaddress
from threading import Thread
from lispy import display_information , display_information_B
from ipaddress import IPv4Address, IPv4Network
from lispy.utils import *
from lispy.lisp import MapRequestMessage, EncapsulatedControlMessage, MapReplyMessage
from lispy.ip import IPv4Packet, IPv6Packet, UDPMessage
from numpy import*


def scan( Name , Timestamp , list_EIDs_Prefix, map_resolver , replies , reply_position , port_source):

    # Display the starting Time
    print('Thread ' + Name + ' started ' + time.strftime(' %a , %l:%M%p %z on %b %d, %Y')) # ' 1:36PM EST on Oct 18, 2010'


    # Getting random port number
    #port_source = random.choice(range(MIN_EPHEMERAL_PORT, 65535))

    reply_counter = 0
    for dst_EID_Prefix in list_EIDs_Prefix:
      list_replies  = list(replies[reply_counter])
      if list_replies[reply_position] == 'n':
          reply_counter = reply_counter + 1
          continue
      counter = 1
      network = ipaddress.ip_network(str(dst_EID_Prefix ))
      addrs_num = network.num_addresses
      dst_EID = ''.join((re.split('/' , dst_EID_Prefix))[0])
      while counter <= addrs_num:
        # Convert to string
        dst_EID = str(dst_EID)
        # Resolve IP from name
        try:
            mr_addr = socket.getaddrinfo(map_resolver, LISP_CONTROL_PORT, 0, 0, socket.SOL_UDP)
            eid_addr = socket.getaddrinfo( dst_EID, 0, 0, 0, socket.SOL_UDP)

        except:
            # print('ERROR: invalid addresses')
             continue
             #sys.exit()


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


        #set  3 secs timeout
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
            print('processing ' + map_resolver + '  '+ Name + '...')
            print(dst_EID)
            dst_EID = int(ipaddress.IPv4Address(dst_EID)) + 1
            dst_EID = str(ipaddress.IPv4Address(dst_EID))
            counter = counter + 1
            if counter > addrs_num :
                reply_counter = reply_counter + 1
            continue

        # PRINT THE MAPPING ENTRY#
        map_reply = MapReplyMessage.from_bytes(data)

        # LISP Map Reply, there are records
        if len(map_reply.records[0].locator_records) != 0:
            display_information_B.display(map_reply , 1 , dst_EID , map_resolver , ip_my , rtt , sender_addr , Timestamp )
            print('processing ' + map_resolver + '  '+ Name + '...')
            reply_counter = reply_counter + 1
            break
        # negative Map Reply
        else:
            display_information_B.display(map_reply, -1, dst_EID , map_resolver , ip_my , rtt , sender_addr , Timestamp)
            print('processing ' + map_resolver + '  '+ Name + '...')
            reply_counter = reply_counter + 1
            break


    print(time.strftime(' %a , %l:%M%p %z on %b %d, %Y')) # ' 1:36PM EST on Oct 18, 2010'
    print ('scanning done  ' + Name)

if __name__ == '__main__':
    try:
      i = 0
      port_source = 34168
      Threads = []
      list_EIDs_Prefix = []
      replies = []

      #Get Timestamp
      Timestamp = int(time.time())

      try:
          TSP_list= open('Timestamp_list.log' , 'a')
      except:
          TSP_list= open('Timestamp_list.log', 'w+')

      TSP_list.write(str(Timestamp) +'\n')
      TSP_list.close()


      # Getting the EID_Prefix list
      list_current = open('summary/EID_list_current.log', 'r')
      data = list_current.read().split()
      while i < len(data) :
          if  '/' in data[i]:
            list_EIDs_Prefix.append(data[i])
            replies.append(data[i+1])
            i = i+3
          else:
              i = i+1

      list_current.close()




      t1 = Thread(target=scan, args=('Thread1', Timestamp , list_EIDs_Prefix , str('149.20.48.77') , replies , 1 , port_source))
      t2 = Thread(target=scan, args=('Thread2', Timestamp , list_EIDs_Prefix , str('149.20.48.61') , replies , 3 ,port_source +1))
      t3 = Thread(target=scan, args=('Thread3', Timestamp , list_EIDs_Prefix , str('198.6.255.40') , replies , 5 , port_source+2))
      t4 = Thread(target=scan, args=('Thread4', Timestamp , list_EIDs_Prefix , str('217.8.98.42') , replies  , 7 , port_source+3))
      t5 = Thread(target=scan, args=('Thread5', Timestamp , list_EIDs_Prefix , str('217.8.98.46') , replies  , 9 , port_source+4))
      t6 = Thread(target=scan, args=('Thread6', Timestamp , list_EIDs_Prefix , str('193.162.145.50') , replies , 11 , port_source+5))
      t7 = Thread(target=scan, args=('Thread7', Timestamp , list_EIDs_Prefix , str('217.8.97.6') , replies , 13 , port_source+6))
      t8 = Thread(target=scan, args=('Thread8', Timestamp , list_EIDs_Prefix , str('202.51.247.10') , replies , 15 , port_source+7))
      t9 = Thread(target=scan, args=('Thread9', Timestamp, list_EIDs_Prefix, str('173.36.254.164'), replies, 17 , port_source+8))
      t10 = Thread(target=scan, args=('Thread10', Timestamp, list_EIDs_Prefix, str('198.6.255.37'), replies, 19 , port_source+9))
      t11 = Thread(target=scan, args=('Thread11', Timestamp, list_EIDs_Prefix, str('206.223.132.89'), replies, 21 , port_source+10))
      t12 = Thread(target=scan, args=('Thread12', Timestamp, list_EIDs_Prefix, str('202.214.86.252'), replies, 23 , port_source+11))
      t13 = Thread(target=scan, args=('Thread13', Timestamp, list_EIDs_Prefix, str('137.194.18.132'), replies, 25 , port_source+12))
      t14 = Thread(target=scan, args=('Thread14', Timestamp, list_EIDs_Prefix, str('132.227.62.246'), replies, 27, port_source + 13))


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

      for x in Threads:
          x.start()
      for x in Threads:
          x.join()



      print(time.strftime(' %a , %l:%M%p %z on %b %d, %Y'))  # ' 1:36PM EST on Oct 18, 2010'
      sys.exit()

    except Exception as e :
      print(e)
      sys.exit()








