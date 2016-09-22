from __future__ import unicode_literals
from lispy.lisp import  MapReplyMessage
from lispy import  Listing
import logging
import logging.handlers
import time
import os



def display( reply , reply_type  , dst_EID , map_resolver , my_ip , rtt , sender_addr , Timestamp , resolver_num):



   # LISP reply
   if reply_type == 1 :

      # Write the result in the EID list
      Listing.lister( dst_EID , str(reply.records[0].eid_prefix) , str(len(reply.records[0].locator_records)) , Timestamp ,  resolver_num)


   # Negative reply
   elif reply_type == -1 :

      # Write the result in the EID list
      Listing.lister(dst_EID , str(reply.records[0].eid_prefix), '0', Timestamp , resolver_num )


   # Timeout
   elif reply_type == 0 : pass



