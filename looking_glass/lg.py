#! /usr/bin/python3.4
import sys
import time
import socket
from lispy.utils import *
from lispy.lisp import MapRequestMessage, EncapsulatedControlMessage, MapReplyMessage
from lispy.ip import IPv4Packet, IPv6Packet, UDPMessage
from ipaddress import IPv4Address
from flask import *

app = Flask(__name__)

def do_map_request(map_resolver, dst_eid):
    port_source = random.choice(range(MIN_EPHEMERAL_PORT, 65535))
    
    # Resolve IP from name
    mr_addr = socket.getaddrinfo(map_resolver, LISP_CONTROL_PORT, 0, 0, socket.SOL_UDP)
    eid_addr = socket.getaddrinfo(dst_eid, 0, 0, 0, socket.SOL_UDP)
    
    # TO IPV4/6Address object
    
    ip_map_resolve = ipaddress.ip_address(mr_addr[0][4][0]);
    ip_eid = ipaddress.ip_address(eid_addr[0][4][0]);
    ip_my = ipaddress.ip_address(get_my_ipaddress());
    ip_my6 = ipaddress.ip_address(get_my_ipaddress6());
    
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
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    sock.bind((str(ip_my),port_source))
    output = "Sending Map-Request to " + map_resolver + " for " + str(ip_eid) + "...\n"
    before = time.time();
    sock.sendto(lh.to_bytes(), mr_addr[0][4])
    data, addr = sock.recvfrom(512)
    after = time.time();
    
    map_reply = MapReplyMessage.from_bytes(data)

    ##########################
    #  BUILD OUTPUT STRING   #
    ##########################
    if nonce != map_reply.nonce:
        output +="Warning: Bad nonce, reply may be spoofed\n"
    output += "Received map-reply from " + addr[0] + " with rtt " + "{0:.5f}".format(after-before) + " secs\n";
    output +="Mapping entry for EID '" + str(ip_eid) + "':\n"

    output += str(map_reply.records[0].eid_prefix)
    output +=" via map-reply, record ttl: "
    output += str(map_reply.records[0].ttl) + ", "
    output +=  "auth, " if map_reply.records[0].authoritative else "not auth "
    output += "mobile\n" if map_reply.records[0].mobility else "not mobile\n"
    
    # Not a negative Map Reply
    if len(map_reply.records[0].locator_records) != 0:
        output += " " + "Locator".ljust(40) + "State".ljust(10) + "Priority/Weight".ljust(10) + "\n";
        for record in map_reply.records:
            for locator in record.locator_records:
                output += " " + str(locator.address).ljust(40)
                if locator.reachable:
                    output += "up".ljust(10)
                else:
                    output += "down".ljust(10)
                output += (str(locator.m_priority) + "/" +  str(locator.m_weight) + "\n")
                
    # Negative map reply
    else:
        output += " Negative cache entry, action: "
        if map_reply.records[0].action == LISP_ACTION_NO_ACTION:
            output += "no-action\n"
        elif map_reply.records[0].action == LISP_ACTION_FORWARD:
            output += "forward-native\n"
        elif map_reply.records[0].action == LISP_ACTION_DROP:
            output += "drop\n"
        elif map_reply.records[0].action == LISP_ACTION_SEND_MAP_REQUEST:
            output += "send-map-request\n"
    return output;
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('lg.html', output="", eid="")
    else:
        map_resolver = request.form['ms']
        dst_eid = request.form['eid']
        if map_resolver == '':
            output = "ERROR: Please specify a Map-Resolver"
        elif dst_eid == '':
            output = "ERROR: Please specify EID."
        else:
            try:
                output = do_map_request(map_resolver, dst_eid);
            except Exception as e:
                output = "ERROR: " + str(e)
        rows = output.count('\n')
        return render_template('lg.html', output=output, eid=dst_eid, rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

    

