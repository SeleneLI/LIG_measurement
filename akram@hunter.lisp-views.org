import random
import os
import netifaces
import ipaddress
from ipaddress import IPv4Address

def get_my_ipaddress():
    for interface in netifaces.interfaces():
       if  netifaces.ifaddresses(interface) != {} and interface != 'fw0':
           for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
             try:
                ipt = ipaddress.ip_address(link['addr'])
                if not ipt.is_private and not ipt.is_loopback and not ipt.is_link_local:
                   return link['addr']
             except:
                pass
    return False
	
def get_my_ipaddress6():
    for interface in netifaces.interfaces():
        if netifaces.ifaddresses(interface) != {} and interface != 'fw0':
           for link in netifaces.ifaddresses(interface)[netifaces.AF_INET6]:
             try:
                ipt = ipaddress.ip_address(link['addr'])
                if not ipt.is_private and not ipt.is_loopback and not ipt.is_link_local:
                    return link['addr']
             except:
                pass
    return False
	

#GENERAL
LISP_CONTROL_PORT = 4342
IPPROTO_UDP = 17
IPPROTO_IPIP = 4
IPPROTO_IPV6 = 41

#LISP TYPES
LISP_MAP_REQUEST = 1
LISP_MAP_REPLY = 2
LISP_MAP_REGISTER = 3
LISP_ENCAP_CONTROL_TYPE = 8

#AFI AND MASK LEN
LISP_AFI_IP = 1
LISP_AFI_IPV6 = 2
LISP_IP_MASK_LEN = 32
LISP_IPV6_MASK_LEN = 128

# MAP REPLY ACTION CODE
LISP_ACTION_NO_ACTION = 0
LISP_ACTION_FORWARD = 1
LISP_ACTION_DROP = 2
LISP_ACTION_SEND_MAP_REQUEST = 3

#RANDOM PORTS
MIN_EPHEMERAL_PORT = 32768
MAX_EPHEMERAL_PORT = 65535


#Generate a 8 octets random value
def get_a_nonce():
	return bytearray(os.urandom(8))
	

