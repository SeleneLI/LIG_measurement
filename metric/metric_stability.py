import sys
import re
import csv
import glob
from ipaddress import IPv4Address, IPv4Network


# List of the Map Resolver which will be measured
map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EUROP , 3*US , 2*ASIA

# Getting the Timestamp
list_TSP = open('Timestamp_list.log' , 'r')
TSPs_list = list_TSP.readlines()
TSPs = []

# the Start and End Timestamp which you want to set the interval
TSP_Start = ''
TSP_END = ''
Interval = False
if Interval == True:
    for TSP in TSPs_list:
        TSP = TSP.strip('\n')
        if TSP_Start <=  TSP <= TSP_END :
            TSPs.append(TSP.strip('\n'))
        else:
            if TSP > TSP_END:
                break
            else:
                continue

else:
    for TSP in TSPs_list:
        TSPs.append(TSP.strip('\n'))


# collecting the data for each Map Resolver
for map_resolver in map_resolvers:
   print(map_resolver)
   # Set the headers of the file
   table_stability_headers = [ ['EID Prefix', 'Reply Type', 'Received From', 'RLOC Addresses', 'RLOC Priorities', 'RLOC Weights','RLOC States', 'New Deployed Changed', 'Configuration Changed ' , 'Statistical Changed', 'Recieved From Changed' , 'Received From not RLOCs '  , 'Received From RLOCs '  , 'Received From Map Resolver ' , 'Number of Timestamp' , 'Total Number of Timestamp']]
   with open('Tables/' + str(map_resolver) + '-stability.csv', 'w', newline='') as fp:
       a = csv.writer(fp, delimiter=',')
       a.writerows(table_stability_headers)

   EID_Prefixes =[]
   file_names = glob.glob('data/' + str(map_resolver) + '/*.log')
   for file_name in file_names:
       EID_Prefix = re.split(r"[-]" , file_name)[1]
       if ':' in EID_Prefix:
           if EID_Prefix not in EID_Prefixes :
               EID_Prefixes.append(EID_Prefix)
   print(map_resolver)

   EID_Prefixes = sorted(EID_Prefixes)
   counter_EID = 0
   for EID_Prefix in EID_Prefixes :
      EID_Prefix += 1
      counter_TSP = 0
      Map_Reply_Type = ''
      RLOC_adds = []
      RLOC_numbers = ''
      RLOC_priorities = []
      RLOC_weights = []
      RLOC_states = []
      received_from = ''
      new_deployed_count = 0
      config_count = 0
      Statistical_count = 0
      config_count_Temp = 0
      Statistical_count_Temp = 0
      Day_count = 0
      received_from_count = 0
      received_from_out_count = 0
      received_from_RLOCs = 0
      received_from_MR = 0
      for TSP in TSPs:
         print(counter_TSP)
         file_name = 'data/' + str(map_resolver) + '/TPT-' + str(EID_Prefix) + '-' + str(map_resolver) + '-' +str(TSP) + '.log'

         try :
            file = open(file_name, 'r')
         except:
             continue
         data = file.readlines()
         if counter_TSP == 0 :
                 RLOC_numbers = (re.split(r"[=]", data[8])[1]).strip('\n')
                 if RLOC_numbers == '0':
                     Map_Reply_Type = 'Negative Reply'
                     received_from , received_from_new =(re.split(r"[=]", data[6])[1]).strip('\n')
                     RLOC_adds.append('')
                     RLOC_states.append('')
                     RLOC_priorities.append('')
                     RLOC_weights.append('')
                 else :
                     Map_Reply_Type = 'LISP Reply'
                     counter = 0
                     position = 13
                     received_from , received_from_new =(re.split(r"[=]", data[6])[1]).strip('\n')
                     while counter < int(RLOC_numbers):
                         RLOC_adds.append((re.split(r"[=]", data[position])[1]).strip('\n'))
                         RLOC_states.append((re.split(r"[=]", data[position+1])[1]).strip('\n'))
                         RLOC_priorities.append((re.split(r"[=]", data[position+2])[1]).strip('\n'))
                         RLOC_weights.append((re.split(r"[=]", data[position+3])[1]).strip('\n'))
                         counter = counter + 1
                         position += 4
                 counter_TSP = counter_TSP + 1


         else:
                 RLOC_numbers_new = (re.split(r"[=]", data[8])[1]).strip('\n')
                 received_from_new = (re.split(r"[=]", data[6])[1]).strip('\n')
                 counter_TSP = counter_TSP + 1
                 Day_count +=1
                 if RLOC_numbers != RLOC_numbers_new and RLOC_numbers == '0' :  # Changed from Negative reply ---> LISP reply
                     Map_Reply_Type = 'LISP Reply'
                     new_deployed_count +=1
                     RLOC_numbers = RLOC_numbers_new

                     # store the new records
                     counter = 0
                     position = 13
                     while counter < int(RLOC_numbers):
                         RLOC_adds.append((re.split(r"[=]", data[position])[1]).strip('\n'))
                         RLOC_states.append((re.split(r"[=]", data[position + 1])[1]).strip('\n'))
                         RLOC_priorities.append((re.split(r"[=]", data[position + 2])[1]).strip('\n'))
                         RLOC_weights.append((re.split(r"[=]", data[position + 3])[1]).strip('\n'))
                         counter = counter + 1
                         position += 4

                 elif RLOC_numbers != RLOC_numbers_new  and RLOC_numbers_new == '0':   # Changed from LISP reply ---> Negative reply
                     Map_Reply_Type = 'Negative Reply'
                     new_deployed_count += 1
                     RLOC_numbers = RLOC_numbers_new

                     RLOC_adds = []
                     RLOC_states = []
                     RLOC_priorities  = []
                     RLOC_weights = []


                 elif RLOC_numbers != RLOC_numbers_new and RLOC_numbers != '0' and RLOC_numbers_new != '0' :  # the number of RLOCs changed
                     Map_Reply_Type = 'LISP Reply'
                     config_count_Temp += 1
                     RLOC_numbers = RLOC_numbers_new
                     RLOC_adds = []
                     RLOC_states = []
                     RLOC_priorities = []
                     RLOC_weights = []

                     # store the new records
                     counter = 0
                     position = 13
                     while counter < int(RLOC_numbers):
                         RLOC_adds.append((re.split(r"[=]", data[position])[1]).strip('\n'))
                         RLOC_states.append((re.split(r"[=]", data[position + 1])[1]).strip('\n'))
                         RLOC_priorities.append((re.split(r"[=]", data[position + 2])[1]).strip('\n'))
                         RLOC_weights.append((re.split(r"[=]", data[position + 3])[1]).strip('\n'))
                         counter = counter + 1
                         position += 4


                 elif RLOC_numbers == RLOC_numbers_new and RLOC_numbers != '0' : # No Changed in LISP reply RLOCs number , Checking the RLOCs set { address , State , Priority , Weight }
                     Map_Reply_Type = 'LISP Reply'
                     counter = 0
                     position = 13
                     while counter < int(RLOC_numbers):
                           if RLOC_adds[counter] !=  (re.split(r"[=]", data[position])[1]).strip('\n')  or RLOC_states[counter] !=  (re.split(r"[=]", data[position+1])[1]).strip('\n') or RLOC_priorities[counter] !=  (re.split(r"[=]", data[position+2])[1]).strip('\n') or RLOC_weights[counter] !=  (re.split(r"[=]", data[position+3])[1]).strip('\n'):
                               config_count_Temp += 1

                               RLOC_adds = []
                               RLOC_states = []
                               RLOC_priorities = []
                               RLOC_weights = []

                               # store the new records
                               counter = 0
                               position = 13
                               while counter < int(RLOC_numbers):
                                   RLOC_adds.append((re.split(r"[=]", data[position])[1]).strip('\n'))
                                   RLOC_states.append((re.split(r"[=]", data[position + 1])[1]).strip('\n'))
                                   RLOC_priorities.append((re.split(r"[=]", data[position + 2])[1]).strip('\n'))
                                   RLOC_weights.append((re.split(r"[=]", data[position + 3])[1]).strip('\n'))
                                   counter = counter + 1
                                   position += 4

                           position += 4
                           counter = counter + 1



                 elif RLOC_numbers == RLOC_numbers_new and RLOC_numbers == '0' : # No Changed in Negative Reply Do nothing
                     Map_Reply_Type = 'Negative Reply'

         if received_from != received_from_new :
                     received_from = received_from_new
                     received_from_count += 1

         if RLOC_numbers != '0' :
                    if received_from not in RLOC_adds and received_from != map_resolver :
                         received_from_out_count +=1
                    else:
                        if received_from in RLOC_adds :
                            received_from_RLOCs += 1
                        elif received_from == map_resolver:
                             received_from_MR += 1

         if RLOC_numbers == '0':
                     if received_from == map_resolver:
                         received_from_MR += 1

         if Day_count == 12 :
                     if config_count_Temp >= 3 :
                         Statistical_count += 1
                         config_count_Temp = 0
                     else:
                         config_count += config_count_Temp
                     Day_count = 0


      if RLOC_numbers == '0':
          # Write the collected data for the Negative Map-Reply in '-Negative.csv'
          table_stability = [[str(EID_Prefix)] + ['Negative Reply'] + [received_from] + [RLOC_adds] + [RLOC_priorities] + [RLOC_weights] + [RLOC_states] + [str(new_deployed_count)] + [str(config_count)] +  [str(Statistical_count)] + [str(received_from_count)] + [str(received_from_out_count)] + [str(received_from_RLOCs)] + [str(received_from_MR)] + [str(counter_TSP)] + [str(len(TSPs))]]
          with open('Tables/' + str(map_resolver) + '-stability.csv', 'a', newline='') as fp:
              a = csv.writer(fp, delimiter=',')
              a.writerows(table_stability)
      elif RLOC_numbers != '':
          # Write the collected data for the LISP Map-Reply in '-LISP.csv'
          table_stability = [[str(EID_Prefix)] + ['LISP Reply'] + [received_from] + [RLOC_adds] + [RLOC_priorities] + [RLOC_weights] + [RLOC_states] + [str(new_deployed_count)] + [str(config_count)] +  [str(Statistical_count)] + [str(received_from_count)]  + [str(received_from_out_count)] + [str(received_from_RLOCs)] + [str(received_from_MR)] +[str(counter_TSP)] + [str(len(TSPs))]]
          with open('Tables/' + str(map_resolver) + '-stability.csv', 'a', newline='') as fp:
              a = csv.writer(fp, delimiter=',')
              a.writerows(table_stability)





sys.exit()



