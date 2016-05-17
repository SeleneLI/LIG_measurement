from lispy.utils import *
from lispy.ip.afi import *
from bitstring import ConstBitStream, BitArray, Bits

class MapRequestMessage:
	message_type = LISP_MAP_REQUEST;
	
	#Constructeur
	def __init__(self, authoritative=False, probe=False, smr=False, pitr=False,
                 smr_invoked=False, nonce='\x00\x00\x00\x00\x00\x00\x00\x00',
                 source_eid=None, itr_rloc=None, eid_prefix=None,
                 map_reply=None):
		
		self.authoritative = authoritative
		self.probe = probe
		self.smr = smr
		self.pitr = pitr
		self.smr_invoked = smr_invoked
		self.nonce = nonce
		self.source_eid = source_eid
		self.itr_rloc = itr_rloc
		self.eid_prefix = eid_prefix
		self.map_reply = map_reply
		
	
	def to_bytes(self):
		'''
        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |Type=1 |A|M|P|S|p|s|    Reserved     |   IRC   | Record Count  |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                         Nonce . . .                           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                         . . . Nonce                           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |         Source-EID-AFI        |   Source EID Address  ...     |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |         ITR-RLOC-AFI 1        |    ITR-RLOC Address 1  ...    |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                              ...                              |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |         ITR-RLOC-AFI n        |    ITR-RLOC Address n  ...    |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |   Reserved    | EID mask-len  |        EID-Prefix-AFI         |
   Rec +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |                       EID-Prefix  ...                         |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                   Map-Reply Record  ...                       |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	'''
		# Message type
		bitstream = BitArray('uint:4=%d' % self.message_type)
		# Add the flags
		bitstream += BitArray('bool=%d, bool=%d, bool=%d, bool=%d, ''bool=%d, bool=%d' % (self.authoritative,
                                                    self.map_reply is not None,
                                                    self.probe,
                                                    self.smr,
                                                    self.pitr,
                                                    self.smr_invoked))
		# Reserved
		bitstream +=BitArray(9)
		# Add IRC (0)
		bitstream += BitArray('uint:5=%d' % 0)
        # Add record count (1)
		bitstream += BitArray('uint:8=%d' % 1)
        # Add nonce
		bitstream += BitArray(bytes=self.nonce)
        # Add the source EID AFI (0)
		bitstream += BitArray('uint:16=%d' % 0)
		# We skip Source EID Address

		# ITR-RLOC-AFI and ITR-RLOC-Address
		bitstream += get_bitstream_for_afi_address(self.itr_rloc)
		# Reserved #2
		bitstream +=BitArray(8)
		
		eid_prefix = ip_network(self.eid_prefix)
		
		# Destination EID Mask len, AFI, and Address
		bitstream += BitArray('uint:8=%d' % eid_prefix.prefixlen)

        # Add the AFI && address 
		bitstream += get_bitstream_for_afi_address(eid_prefix)
		return bitstream.bytes
