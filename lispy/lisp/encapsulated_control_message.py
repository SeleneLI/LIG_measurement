from bitstring import ConstBitStream, BitArray, Bits
from lispy.utils import *

class EncapsulatedControlMessage:

    message_type = LISP_ENCAP_CONTROL_TYPE

    def __init__(self, security=False, ddt_originated=False, for_rtr=False, relayed_by_rtr=False, payload=''):
        self.security = security
        self.ddt_originated = ddt_originated
        self.for_rtr = for_rtr
        self.relayed_by_rtr = relayed_by_rtr
        self.payload = payload

    def to_bytes(self):
        # Start with the type
        bitstream = BitArray('uint:4=%d' % self.message_type)

        # Add the flags
        bitstream += BitArray('bool=%d, bool=%d' % (self.security,self.ddt_originated))

        # Add padding
        bitstream += BitArray(26)

        return bitstream.bytes + self.payload.to_bytes()
