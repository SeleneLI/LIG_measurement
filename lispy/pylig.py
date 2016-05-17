#!/usr/bin/python3.4
import sys
import time
import socket
from ipaddress import IPv4Address
from lispy.utils import *
from lispy.lisp import MapRequestMessage, EncapsulatedControlMessage, MapReplyMessage
from lispy.ip import IPv4Packet, IPv6Packet, UDPMessage


debug = False;

# TODO: change this to somthing like: pylig [-m <Map-Resolver>] <destination-EID> and check if they are corrects.
try:
    map_resolver = str(sys.argv[1])
    dst_eid = str(sys.argv[2])
except:
    print('usage: pylig <map-resolver> <destination-eid>')
    sys.exit()

port_source = random.choice(range(MIN_EPHEMERAL_PORT, 65535))

# Resolve IP from name
try:
    mr_addr = socket.getaddrinfo(map_resolver, LISP_CONTROL_PORT, 0, 0, socket.SOL_UDP)
    eid_addr = socket.getaddrinfo(dst_eid, 0, 0, 0, socket.SOL_UDP)
except:
    print('ERROR: invalid addresses')
    print('usage: pylig <map-resolver> <destination-eid>')
    sys.exit()

# TO IPV4/6Address object
ip_map_resolve = ipaddress.ip_address(mr_addr[0][4][0]);
ip_eid = ipaddress.ip_address(eid_addr[0][4][0]);
ip_my = ipaddress.ip_address(get_my_ipaddress());
ip_my6 = ipaddress.ip_address(get_my_ipaddress6());

if debug:
	print("Map-Resolver:", ip_map_resolve)
	print("Destination EID:", ip_eid)
	print("My IP:", ip_my)
	print("My IP6:", ip_my6)
	
	
	
	
'''
We build this:

        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |                       IPv4 or IPv6 Header                     |
   OH  |                      (uses RLOC addresses)                    |
     \ |                                                               |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |       Source Port = xxxx      |       Dest Port = 4342        |
   UDP +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |           UDP Length          |        UDP Checksum           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   LH  |Type=8 |S|                  Reserved                           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |                       IPv4 or IPv6 Header                     |
   IH  |                  (uses RLOC or EID addresses)                 |
     \ |                                                               |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |       Source Port = xxxx      |       Dest Port = yyyy        |
   UDP +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |           UDP Length          |        UDP Checksum           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   lcm |                      LISP Control Message                     |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       
'''

# generate a nonce
nonce = get_a_nonce()
# lcm
lcm = MapRequestMessage(eid_prefix=ip_eid, itr_rloc=ip_my, nonce=nonce)
# UDP
udp = UDPMessage(source_port=port_source, destination_port=LISP_CONTROL_PORT, payload=lcm)
# IH
if isinstance(ip_eid, IPv4Address):
	ih = IPv4Packet(source=ip_my, destination=ip_eid, payload=udp, protocol=IPPROTO_UDP)
	udp.checksum = udp.calculate_checksum(source=ip_my, destination=ip_eid)
else:
	ih = IPv6Packet(source=ip_my6, destination=ip_eid, payload=udp, next_header=IPPROTO_UDP)
	udp.checksum = udp.calculate_checksum(source=ip_my6, destination=ip_eid)
# LH
lh= EncapsulatedControlMessage(payload=ih)

#UDP AND OH are built by the kernel

if debug:
	print("LCM:", lcm.to_bytes())
	print("UDP:", udp.to_bytes())
	print("IH:", ih.to_bytes())
	print("LH:", lh.to_bytes())


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((str(ip_my),port_source))
print("Sending Map-Request to", map_resolver, "for", str(ip_eid), "...");
before = time.time();
sock.sendto(lh.to_bytes(), mr_addr[0][4])
data, addr = sock.recvfrom(512)
after = time.time();

##########################
# PRINT THE MAPPING ENTRY#
##########################
print("Received map-reply from", addr[0], "with rtt %.5f secs\n" %  (after-before));
map_reply = MapReplyMessage.from_bytes(data)
if debug:
	print("received message:", data)
	
if debug:
	print("nonce0:", bytes(nonce))
	print("nonce:", map_reply.nonce)

if nonce != map_reply.nonce:
	print("Bad nonce, reply may be spoofed")

print("Mapping entry for EID '" + str(ip_eid) + "':")

print(map_reply.records[0].eid_prefix,
	"via map-reply, record ttl:",
	str(map_reply.records[0].ttl) + ",",
	"auth," if map_reply.records[0].authoritative else "not auth",
	"mobile," if map_reply.records[0].mobility else "not mobile")
# Not a negative Map Reply

if len(map_reply.records[0].locator_records) != 0:
	print(" " + "Locator".ljust(40) + "State".ljust(10) + "Priority/Weight".ljust(10));
	for record in map_reply.records:
		for locator in record.locator_records:
			print(" " + str(locator.address).ljust(40) , end=""),
			if locator.reachable:
				print("up".ljust(10), end=""),
			else:
				print("down".ljust(10), end=""),
			print(str(locator.m_priority) + "/" +  str(locator.m_weight))
			
# Negative map reply
else:
	print(" Negative cache entry, action: ", end="");
	if map_reply.records[0].action == LISP_ACTION_NO_ACTION:
		print("no-action")
	elif map_reply.records[0].action == LISP_ACTION_FORWARD:
		print("forward-native")
	elif map_reply.records[0].action == LISP_ACTION_DROP:
		print("drop")
	elif map_reply.records[0].action == LISP_ACTION_SEND_MAP_REQUEST:
		print("send-map-request")
	

