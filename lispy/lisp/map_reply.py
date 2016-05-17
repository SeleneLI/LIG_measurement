from bitstring import ConstBitStream, BitArray, Bits
from lispy.utils import *
from lispy.lisp import MapReplyRecord

class MapReplyMessage:

    message_type = LISP_MAP_REPLY

    def __init__(self, probe=False, enlra_enabled=False, security=False, nonce='\x00\x00\x00\x00\x00\x00\x00\x00', records=None):

        # Set defaults
        self.probe = probe
        self.enlra_enabled = enlra_enabled
        self.security = security
        self.nonce = nonce
        self.records = records or []

        # Store space for reserved bits
        self._reserved1 = BitArray(17)

    @classmethod
    def from_bytes(cls, bitstream):
		
        '''	
				0                   1                   2                   3
				0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
			   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
			   |Type=2 |P|E|S|          Reserved               | Record Count  |
			   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
			   |                         Nonce . . .                           |
			   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
			   |                         . . . Nonce                           |
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
		
        packet = cls()

        # Convert to ConstBitStream (if not already provided)
        if not isinstance(bitstream, ConstBitStream):
            if isinstance(bitstream, Bits):
                bitstream = ConstBitStream(auto=bitstream)
            else:
                bitstream = ConstBitStream(bytes=bitstream)

        # Read the type
        type_nr = bitstream.read('uint:4')
        if type_nr != packet.message_type:
            msg = 'Invalid bitstream for a {0} packet'
            class_name = packet.__class__.__name__
            raise ValueError(msg.format(class_name))

        # Read the flags
        (packet.probe,
         packet.enlra_enabled,
         packet.security) = bitstream.readlist('3*bool')

        # Skip reserved bits
        packet._reserved1 = bitstream.read(17)

        # Store the record count until we need it
        record_count = bitstream.read('uint:8')

        # Read the nonce
        packet.nonce = bitstream.read('bytes:8')

        # Read the records
        for dummy in range(record_count):
            record = MapReplyRecord.from_bytes(bitstream)
            packet.records.append(record)

        return packet
