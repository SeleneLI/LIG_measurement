from bitstring import ConstBitStream, BitStream, Bits
from ipaddress import IPv4Address
import math
import numbers
from lispy.utils import *


class IPv4Packet:

    header_type = IPPROTO_IPIP
    version = 4

    def __init__(self, tos=0, identification=54321, dont_fragment=False,
                 more_fragments=False, fragment_offset=0, ttl=64, protocol=0,
                 source=None, destination=None, options='', payload='',
                 next_header=IPPROTO_UDP):

        # Set defaults
        self.tos = tos
        self.identification = identification
        self.dont_fragment = dont_fragment
        self.more_fragments = more_fragments
        self.fragment_offset = fragment_offset
        self.ttl = ttl
        self.source = source
        self.destination = destination
        self.options = options
        self.payload = payload
        self.protocol = protocol
        self.next_header = next_header

    def to_bytes(self):
        '''
            0                   1                   2                   3   
			0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
		   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   |Version|  IHL  |Type of Service|          Total Length         |
		   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   |         Identification        |Flags|      Fragment Offset    |
		   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   |  Time to Live |    Protocol   |         Header Checksum       |
		   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   |                       Source Address                          |
		   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   |                    Destination Address                        |
		   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   |                    Options                    |    Padding    |
		   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        '''

        # Write the version
        bitstream = BitStream('uint:4=%d' % self.version)

        # Write the header length
        bitstream += BitStream('uint:4=%d' % 5)

        # Write the type of service
        bitstream += BitStream('uint:8=%d' % self.tos)

        # Write the total length
        payload_bytes = self.payload.to_bytes()
        total_length = 20 + len(payload_bytes)
        bitstream += BitStream('uint:16=%d' % total_length)

        # Write the identification
        bitstream += BitStream('uint:16=%d' % self.identification)

        # Write the flags
        bitstream += BitStream('bool=False, bool=%d, '
                               'bool=%d' % (self.dont_fragment,
                                            self.more_fragments))

        # Write the fragment offset
        bitstream += BitStream('uint:13=%d' % self.fragment_offset)

        # Write the TTL
        bitstream += BitStream('uint:8=%d' % self.ttl)

        # Write the protocol number
        bitstream += BitStream('uint:8=%d' % self.protocol)

        # Write the header checksum as 0 for now, we calculate it later
        bitstream += BitStream('uint:16=0')

        # Write the source and destination addresses
        bitstream += BitStream('uint:32=%d, ''uint:32=%d' % (int(self.source), int(self.destination)))

        return bitstream.bytes + payload_bytes
