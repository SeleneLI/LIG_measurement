from bitstring import BitStream, ConstBitStream, Bits
from lispy.utils import *
from ipaddress import *

class UDPMessage:
	
	header_type = IPPROTO_UDP
	
	def __init__(self, source_port=0, destination_port=0, payload=''):
		self.payload = payload
		self.source_port = source_port
		self.destination_port = destination_port
		self.checksum = 0

	def generate_pseudo_header(self, source, destination):
		# Calculate the length of the UDP layer
		udp_length = 8 + len(self.payload.to_bytes())

		if isinstance(source, IPv4Address) \
		and isinstance(destination, IPv4Address):
			# Generate an IPv4 pseudo-header
			header = BitStream('uint:32=%d, '
								'uint:32=%d, '
								'uint:16=17, '
								'uint:16=%d' % (int(source),
                                               int(destination),
                                               udp_length))

		elif isinstance(source, IPv6Address) \
		and isinstance(destination, IPv6Address):
			# Generate an IPv6 pseudo-header
			header = BitStream('uint:128=%d, '
								'uint:128=%d, '
								'uint:32=%d, '
								'uint:32=17' % (int(source),
												int(destination),
												udp_length))
		else:
			raise ValueError('Source and destination must belong to the same '
							 'IP version')

		# Return the header bytes
		return header.bytes
	
	#Calculate UDP checksum
	def ones_complement(self, message):
		message = bytes(message)

		# Add padding if the message has an odd number of bytes
		if len(message) % 2 == 1:
			message = message + '\x00'
		checksum = 0
		for i in range(0, len(message), 2):
			next_16_bits = (message[i] << 8) + message[i + 1]
			tmp = checksum + next_16_bits
			checksum = (tmp & 0xffff) + (tmp >> 16)
		checksum = ~checksum & 0xffff

		return checksum

	def calculate_checksum(self, source, destination):
		# Calculate the pseudo-header for the checksum calculation
		pseudo_header = self.generate_pseudo_header(source, destination)

		# Remember the current checksum, generate a message and restore the
		# original checksum
		old_checksum = self.checksum
		self.checksum = 0
		message = self.to_bytes()
		self.checksum = old_checksum

		# Calculate the checksum
		my_checksum = self.ones_complement(pseudo_header + message)

		if my_checksum == 0:
			my_checksum = 0xffff

		return my_checksum
		

	def to_bytes(self):
		'''
				  0      7 8     15 16    23 24    31  
                 +--------+--------+--------+--------+ 
                 |     Source      |   Destination   | 
                 |      Port       |      Port       | 
                 +--------+--------+--------+--------+ 
                 |                 |                 | 
                 |     Length      |    Checksum     | 
                 +--------+--------+--------+--------+ 
                 |                                     
                 |          data octets ...            
                 +---------------- ...                 
		'''
		# Write the source and destination ports
		bitstream = BitStream('uint:16=%d, ''uint:16=%d' % (self.source_port,self.destination_port))
		
        # Write the length
		payload_bytes = self.payload.to_bytes()
		length = len(payload_bytes) + 8
		
		bitstream += BitStream('uint:16=%d' % length)

		# Write the checksum
		bitstream += BitStream('uint:16=%d' % self.checksum)
        
		return bitstream.bytes + payload_bytes
