from bitstring import ConstBitStream, BitArray, Bits
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network
import logging
import numbers
from lispy.ip.afi import *

class LocatorRecord:
    def __init__(self, priority=255, weight=0, m_priority=255, m_weight=0,
                 local=False, probed_locator=False, reachable=False,
                 address=None):
        
        # Set defaults
        self.priority = priority
        self.weight = weight
        self.m_priority = m_priority
        self.m_weight = m_weight
        self.local = local
        self.probed_locator = probed_locator
        self.reachable = reachable
        self.address = address

    @classmethod
    def from_bytes(cls, bitstream):
        '''
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |  /|    Priority   |    Weight     |  M Priority   |   M Weight    |
           | L +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           | o |        Unused Flags     |L|p|R|           Loc-AFI             |
           | c +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |  \|                             Locator                           |
		   +-> +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        '''
        record = cls()

        # Convert to ConstBitStream (if not already provided)
        if not isinstance(bitstream, ConstBitStream):
            if isinstance(bitstream, Bits):
                bitstream = ConstBitStream(auto=bitstream)
            else:
                bitstream = ConstBitStream(bytes=bitstream)

        # Read the priorities and weights
        (record.priority, record.weight, record.m_priority,
         record.m_weight) = bitstream.readlist('4*uint:8')

        # Read over unused flags
        record.reserved = bitstream.read(13)

        # Read the flags
        (record.local,
         record.probed_locator,
         record.reachable) = bitstream.readlist('3*bool')

        # Read the locator
        record.address = read_afi_address_from_bitstream(bitstream)

        return record
