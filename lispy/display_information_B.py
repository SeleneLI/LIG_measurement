from __future__ import unicode_literals
from lispy.lisp import  MapReplyMessage
from lispy import  Listing
import logging
import logging.handlers
import time



def display( reply , reply_type  , dst_EID , map_resolver , my_ip , rtt , sender_addr , Timestamp):



   file = logging.getLogger(dst_EID + '-' + map_resolver)
   formatter = logging.Formatter(' %(message)s')
   if reply_type == 0:
     fileHandler = logging.FileHandler('TPT-'+ dst_EID + '-' + map_resolver + '-' + str(Timestamp)+ '_t'+'.log' )
   else:
      EID_Prefix = str(reply.records[0].eid_prefix).replace('/' , ':')
      fileHandler = logging.FileHandler('TPT-'+ EID_Prefix +'-' + map_resolver +'-' +  str(Timestamp)+ '.log')
   fileHandler.setFormatter(formatter)
   streamHandler = logging.StreamHandler()
   streamHandler.setFormatter(formatter)
   file.setLevel(logging.INFO)
   file.addHandler(fileHandler)
   file.addHandler(streamHandler)


   if reply_type == 1 :

      #Listing.lister( dst_EID , str(reply.records[0].eid_prefix) , str(len(reply.records[0].locator_records)) , Timestamp , map_resolver)
      logging.info('------------------------------------------------------------------->')
      for num_records in range(len(reply.records)):

          file.info('Date:' + time.strftime(' %l:%M%p  on %b %d, %Y'))
          file.info('EID=' + dst_EID)
          file.info('Resolver=' + map_resolver + '\n')
          file.info('Using source address (ITR-RLOC)' + str(my_ip))
          file.info('Send map-request to ' + map_resolver + ' for ' + dst_EID)
          file.info('RECEIVED_FFROM=' + str(sender_addr[0]))
          file.info('RTT='+ str(rtt) + 'ms')
          file.info('LOCATOR_COUNT=' + str(len(reply.records[num_records].locator_records)))
          file.info('MAPPING_ENTRY=' + str(reply.records[num_records].eid_prefix))
          file.info('TTL=' + str(reply.records[num_records].ttl))
          file.info('AUTH=' + str(reply.records[num_records].authoritative))
          file.info('MOBILE=' + str(reply.records[num_records].mobility))

          for num_loc_records in range(len(reply.records[num_records].locator_records)):
              file.info('LOCATOR' + str(num_loc_records) + '=' + str(reply.records[num_records].locator_records[num_loc_records].address) )
              file.info( 'LOCATOR' + str(num_loc_records) + '_STATE=Up'  )
              file.info('LOCATOR' + str(num_loc_records) + '_PRIORITY=' + str(reply.records[num_records].locator_records[num_loc_records].priority))
              file.info('LOCATOR' + str(num_loc_records) + '_WEIGHT=' + str(reply.records[num_records].locator_records[num_loc_records].weight))


      file.info('\n')


   elif reply_type == -1 :

      #Listing.lister(dst_EID , str(reply.records[0].eid_prefix), '0', Timestamp , map_resolver)
      logging.info('------------------------------------------------------------------->')
      for num_loc_records in range(len(reply.records[0].locator_records)+1):

        file.info('Date:' + time.strftime('%l:%M%p  on %b %d, %Y'))
        file.info('EID=' + dst_EID)
        file.info('Resolver=' + map_resolver + '\n')
        file.info('Using source address (ITR-RLOC)' + str(my_ip))
        file.info('Send map-request to ' + map_resolver + ' for ' + dst_EID)
        file.info('RECEIVED_FFROM=' + str(sender_addr[0]))
        file.info('RTT=' + str(rtt))
        file.info('LOCATOR_COUNT=0')
        file.info('MAPPING_ENTRY=' + str(reply.records[0].eid_prefix))
        file.info('TTL=' + str(reply.records[0].ttl))
        file.info('AUTH=' + str(reply.records[0].authoritative))
        file.info('MOBILE=' + str(reply.records[0].mobility))
        file.info('RESULT= Negative cache entry')
        file.info('ACTION=' + str(reply.records[0].action) + '\n')



   elif reply_type == 0 :
       file.info('------------------------------------------------------------------->')
       file.info('Date:' + time.strftime(' %l:%M%p  on %b %d, %Y'))
       file.info('EID=' + dst_EID)
       file.info('Resolver=' + map_resolver + '\n')
       file.info('Using source address (ITR-RLOC)')
       file.info('Send map-request to ' + map_resolver + ' for ' + dst_EID + ',,,')
       file.info('Send map-request to ' + map_resolver + ' for ' + dst_EID + ',,,')
       file.info('Send map-request to ' + map_resolver + ' for ' + dst_EID + ',,,')
       file.info('*** No map-reply received ***' + '\n')

   logging.shutdown()
