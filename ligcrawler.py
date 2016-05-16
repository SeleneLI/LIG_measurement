import sys
import time
import socket
import ipaddress
from ipaddress import IPv4Address, IPv4Network
from lispy.utils import *
from lispy.lisp import MapRequestMessage, EncapsulatedControlMessage, MapReplyMessage
from lispy.ip import IPv4Packet, IPv6Packet, UDPMessage
from numpy import*

try:
    map_resolver = str("137.194.18.132")
    dst_eid = str("0.0.0.0")
except:
    sys.exit()

tableau=[[0 for j in range(0,2)] for i in range(0,2^20)]
tableau[0][0]="EID"
tableau[0][1]="RLOC correspondant"
i=1

while ipaddress.ip_address(dst_eid)<= ipaddress.ip_address('255.255.255.255.255'):
    port_source = random.choice(range(MIN_EPHEMERAL_PORT, 65535))

    # Resolve IP from name
    try:
        mr_addr = socket.getaddrinfo(map_resolver, LISP_CONTROL_PORT, 0, 0, socket.SOL_UDP)
        eid_addr = socket.getaddrinfo(dst_eid, 0, 0, 0, socket.SOL_UDP)

    except:
         print('ERROR: invalid addresses')
         sys.exit()


    # Converting ip string TO IPV4/6Address object
    ip_map_resolve = ipaddress.ip_address(mr_addr[0][4][0]);
    ip_eid = ipaddress.ip_address(eid_addr[0][4][0]);

    # Get our IP Address, our address must be routable on the interne
    ip_my = ipaddress.ip_address(get_my_ipaddress());
    ip_my6 = ipaddress.ip_address(get_my_ipaddress6());

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

    # set a 5 sec timeout
    sock.settimeout(5)

    try:
        # Send the request and wait for the reply
        before = time.time();
        sock.sendto(lh.to_bytes(), mr_addr[0][4])
        data, addr = sock.recvfrom(512)
        after = time.time();

    except socket.timeout:
        print('Error: request timed out after 5s')
        sys.exit()

    # PRINT THE MAPPING ENTRY#
    map_reply = MapReplyMessage.from_bytes(data)

    reponse = map_reply.records[0].eid_prefix
    reponsetab = str(reponse)

    # Not a negative Map Reply, there are records
    if len(map_reply.records[0].locator_records) != 0:
        tableau[i][1]=reponsetab
        tableau[i][0]=dst_eid
        
    #incrementation adresse IP
    network= ipaddress.ip_network(reponsetab)
    a = network.num_addresses
    nextint = int(ipaddress.IPv4Address(dest_eid)) + a
    dest_eid = str(ipaddress.IPv4Address(nextint))
    i = i+1
    



tableau
