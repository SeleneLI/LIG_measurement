from bitstring import ConstBitStream, BitStream, Bits
from ipaddress import IPv6Address
import numbers
from lispy.utils import *


class IPv6Packet:
    header_type = IPPROTO_IPV6
    version = 6

    def __init__(self, traffic_class=0, flow_label=0, next_header=0,
                 hop_limit=0, source=None, destination=None, payload=''):

        self.payload = payload
        self.next_header = next_header
        self.traffic_class = traffic_class
        self.flow_label = flow_label
        self.hop_limit = hop_limit
        self.source = source
        self.destination = destination

    def to_bytes(self):
        '''
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   |Version| Traffic Class |           Flow Label                  |
		   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   |         Payload Length        |  Next Header  |   Hop Limit   |
		   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   |                                                               |
		   +                                                               +
		   |                                                               |
		   +                         Source Address                        +
		   |                                                               |
		   +                                                               +
		   |                                                               |
		   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   |                                                               |
		   +                                                               +
		   |                                                               |
		   +                      Destination Address                      +
		   |                                                               |
		   +                                                               +
		   |                                                               |
		   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        '''

        # Write the version
        bitstream = BitStream('uint:4=%d' % self.version)

        # Write the traffic class
        bitstream += BitStream('uint:8=%d' % self.traffic_class)

        # Write the flow label
        bitstream += BitStream('uint:20=%d' % self.flow_label)

        # Write the payload length
        payload_bytes = self.payload.to_bytes()
        payload_length = len(payload_bytes)
        bitstream += BitStream('uint:16=%d' % payload_length)

        # Write the next header type
        bitstream += BitStream('uint:8=%d' % self.next_header)

        # Write the hop limit
        bitstream += BitStream('uint:8=%d' % self.hop_limit)

        # Write the source and destination addresses
        bitstream += BitStream('uint:128=%d, ''uint:128=%d' % (int(self.source),int(self.destination)))

        return bitstream.bytes + payload_bytes
