from bitstring import ConstBitStream, BitArray, Bits
from ipaddress import IPv4Network, IPv6Network
import numbers
from lispy.ip.afi import *
from lispy.lisp import LocatorRecord


class MapReplyRecord:
    ACT_NO_ACTION = 0
    ACT_NATIVELY_FORWARD = 1
    ACT_SEND_MAP_REQUEST = 2
    ACT_DROP = 3

    def __init__(self, ttl=0, action=ACT_NO_ACTION, authoritative=False, mobility=False, map_version=0, eid_prefix=None, locator_records=None):
        # Set defaults
        self.ttl = ttl
        self.action = action
        self.authoritative = authoritative
        self.mobility = mobility
        self.map_version = map_version
        self.eid_prefix = eid_prefix
        self.locator_records = list(locator_records or [])

    @classmethod
    def from_bytes(cls, bitstream):
		
        '''
		+-> +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   |   |                          Record TTL                           |
		   |   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   R   | Locator Count | EID mask-len  | ACT |A|      Reserved         |
		   e   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   c   | Rsvd  |  Map-Version Number   |       EID-Prefix-AFI          |
		   o   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		   r   |                          EID-Prefix                           |
		   d   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
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

        # Read the record TTL
        record.ttl = bitstream.read('uint:32')

        # Store the locator record count until we need it
        locator_record_count = bitstream.read('uint:8')

        # Store the EID prefix mask length until we need it
        eid_prefix_len = bitstream.read('uint:8')

        # Read the Negative Map_Reply action
        record.action = bitstream.read('uint:3')

        # Read the flag
        record.authoritative = bitstream.read('bool')
        
        # Read mobility bits(first bit in reserved space)
        record.mobility = bitstream.read('bool')

        # Read reserved bits
        record._reserved1 = bitstream.read(11 + 4)

        # Read the map version
        record.map_version = bitstream.read('uint:12')

        # Read the EID prefix
        record.eid_prefix = read_afi_address_from_bitstream(bitstream,
                                                            eid_prefix_len)


        # Read the locator records
        for dummy in range(locator_record_count):
            locator_record = LocatorRecord.from_bytes(bitstream)
            record.locator_records.append(locator_record)


        return record
