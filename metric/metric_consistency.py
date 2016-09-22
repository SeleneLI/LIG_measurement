import sys
import re
import csv
import glob


map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EUROP , 3*US , 2*ASIA


list_TSP = open('Timestamp_list.log' , 'r')
TSPs_list = list_TSP.readlines()
TSPs = []
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



for map_resolver in map_resolvers:

   counter_TSP = 1
   table_stability_headers = [ ['EID Prefix', 'Reply Type', 'Recieved From', 'RLOC Addresses', 'RLOC Priorities', 'RLOC Weights','RLOC States', 'New Deployed Count', 'Configuration Count ', 'Recieved From Count' , 'Receievd not From RLOCs ']]
   with open('Tables/' + str(map_resolver) + '-consistency.csv', 'w', newline='') as fp:
       a = csv.writer(fp, delimiter=',')
       a.writerows(table_stability_headers)

   EID_Prefixes =[]
   file_names = glob.glob('data/' + str(map_resolver) + '/*.log')
   for file_name in file_names:
       EID_Prefix = re.split(r"[-]" , file_name)[1]
       if ':' in EID_Prefix:
           if EID_Prefix not in EID_Prefixes :
               EID_Prefixes.append(EID_Prefix)

   for TSP in TSPs :

      counter_TSP += 1
      for EID_Prefix in EID_Prefixes:
         counter_MR = 1
         RLOC_adds = []
         RLOC_numbers = ''
         RLOC_priorities = []
         RLOC_weights = []
         RLOC_states = []
         received_from = ''
         new_deployed_count = 0
         config_count = 0
         received_from_count = 0
         received_from_out_count = 0
         for MR in map_resolvers :
             file_name = 'data/' + str(MR) + '/TPT-' + str(EID_Prefix) + '-' + str(MR) + '-' +str(TSP) + '.log'

             try :
                file = open(file_name, 'r')
             except:
                 continue
             data = file.readlines()
             if counter_MR == 1 :
                     RLOC_numbers = (re.split(r"[=]", data[8])[1]).strip('\n')
                     if RLOC_numbers == '0':
                         received_from=(re.split(r"[=]", data[6])[1]).strip('\n')
                         RLOC_adds.append('')
                         RLOC_states.append('')
                         RLOC_priorities.append('')
                         RLOC_weights.append('')
                     else :
                         counter = 0
                         position = 13
                         received_from =(re.split(r"[=]", data[6])[1]).strip('\n')
                         while counter < int(RLOC_numbers):
                             RLOC_adds.append((re.split(r"[=]", data[position])[1]).strip('\n'))
                             RLOC_states.append((re.split(r"[=]", data[position+1])[1]).strip('\n'))
                             RLOC_priorities.append((re.split(r"[=]", data[position+2])[1]).strip('\n'))
                             RLOC_weights.append((re.split(r"[=]", data[position+3])[1]).strip('\n'))
                             counter = counter + 1
                             position += 4
                     counter_MR = counter_MR + 1
                     continue

             else:
                     RLOC_numbers_new = (re.split(r"[=]", data[8])[1]).strip('\n')
                     received_from_new = (re.split(r"[=]", data[6])[1]).strip('\n')
                     counter_MR = counter_MR + 1
                     if RLOC_numbers != RLOC_numbers_new and RLOC_numbers == '0' :
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

                     elif RLOC_numbers != RLOC_numbers_new  and RLOC_numbers_new == '0':

                         new_deployed_count += 1
                         RLOC_numbers = RLOC_numbers_new

                         RLOC_adds = []
                         RLOC_states = []
                         RLOC_priorities  = []
                         RLOC_weights = []


                     elif RLOC_numbers != RLOC_numbers_new and RLOC_numbers != '0' and RLOC_numbers_new != '0' :
                         config_count += 1

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


                     elif RLOC_numbers == RLOC_numbers_new and RLOC_numbers != '0' :
                         counter = 0
                         position = 13
                         while counter < int(RLOC_numbers):
                               if RLOC_adds[counter] !=  (re.split(r"[=]", data[position])[1]).strip('\n')  or RLOC_states[counter] !=  (re.split(r"[=]", data[position+1])[1]).strip('\n') or RLOC_priorities[counter] !=  (re.split(r"[=]", data[position+2])[1]).strip('\n') or RLOC_weights[counter] !=  (re.split(r"[=]", data[position+3])[1]).strip('\n'):
                                   config_count += 1
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

                     elif RLOC_numbers == RLOC_numbers_new and RLOC_numbers == '0' :
                         pass

                     if RLOC_numbers != '0' and received_from != received_from_new :
                         received_from = received_from_new
                         received_from_count += 1
                     if RLOC_numbers != '0' :
                        if received_from not in RLOC_adds and received_from != MR:
                             received_from_out_count +=1

         if RLOC_numbers == '0':

              table_stability = [[EID_Prefix] + ['Negative Reply'] + [received_from] + [RLOC_adds] + [RLOC_priorities] + [RLOC_weights] + [RLOC_states] + [str(new_deployed_count)] + [str(config_count)] + [str(received_from_count)]  + [str(received_from_out_count)] ]
              with open('Tables/' + str(map_resolver) + '-consistency.csv', 'a', newline='') as fp:
                  a = csv.writer(fp, delimiter=',')
                  a.writerows(table_stability)
         elif RLOC_numbers != '':

              table_stability = [[EID_Prefix] + ['LISP Reply'] + [received_from] + [RLOC_adds] + [RLOC_priorities] + [RLOC_weights] + [RLOC_states] + [str(new_deployed_count)] + [str(config_count)] + [str(received_from_count)]+ [str(received_from_out_count)]]
              with open('Tables/' + str(map_resolver) + '-consistency.csv', 'a', newline='') as fp:
                  a = csv.writer(fp, delimiter=',')
                  a.writerows(table_stability)





sys.exit()



