import sys
import re
import csv
import glob
import ipaddress
from ipaddress import IPv4Address, IPv4Network

# List of the Map Resolver which will be measured
map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EUROP , 3*US , 2*ASIA

table_Negative = []
table_LISP = []

# Getting the Timestamp
list_TSP = open('Timestamp_list.log' , 'r')
TSPs_list = list_TSP.readlines()
TSPs = []

# the Start and End Timestamp which you want to set the interval
TSP_Start = '1471168801'
TSP_END = '1471255201'
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

TSPs_table = [[''] + TSPs]
print(len(TSPs))

# collecting the data for each Map Resolver
for map_resolver in map_resolvers:
   table_Negative = []
   table_LISP = []
   counter_TSP = 1
   for TSP in TSPs :
      print(counter_TSP)
      PATH =  'data/'+ str(map_resolver) + '/*'+str(map_resolver)+'-'+str(TSP)+'.log'
      file_names = glob.glob(PATH)

      for file_name in file_names :
          row = [''] * (len(TSPs)+1)
          EID_Prefix = re.split(r"[-]" , file_name)[1]
          EID_Prefix = EID_Prefix.replace(':' , '/')
          file = open(file_name , 'r')
          data = file.readlines()
          if 'LOCATOR_COUNT' not in data[8] :
              continue
          loc_count = data[8]
          loc_count = re.split(r"[=]", loc_count)[1]
          if loc_count == '0\n':
             RTT = data[7]
             RTT = re.split(r"[=]", RTT)[1]
             RTT = RTT.replace('ms\n', '')
             Found = False
             if table_Negative != [] :
               for search_row in table_Negative :
                   index = table_Negative.index(search_row)
                   if  re.split( r"[/]" , EID_Prefix)[0] == re.split( r"[/]" , search_row[0])[0]  :
                        search_row[counter_TSP] = RTT
                        search_row[0] = EID_Prefix
                        table_Negative[index]=search_row
                        Found = True
                        break
               if Found == False:

                   row[0] = str(EID_Prefix)
                   row[counter_TSP] = RTT
                   table_Negative.append(row)
             else:
                 row[0]=str(EID_Prefix)
                 row[counter_TSP] = RTT
                 table_Negative.append(row)
          else:
              RTT = data[7]
              RTT = re.split(r"[=]", RTT)[1]
              RTT = RTT.replace('ms\n', '')
              Found = False
              if table_LISP != []:
                  for search_row in table_LISP:
                      index = table_LISP.index(search_row)
                      if re.split( r"[/]" , EID_Prefix)[0] == re.split( r"[/]" , search_row[0])[0]:
                          search_row[counter_TSP] = RTT
                          search_row[0] = str(EID_Prefix)
                          table_LISP[index] = search_row
                          Found = True
                          break
                  if Found == False:
                      row[0] = str(EID_Prefix)
                      row[counter_TSP] = RTT
                      table_LISP.append(row)
              else:
                  row[0] = str(EID_Prefix)
                  row[counter_TSP] = RTT
                  table_LISP.append(row)

      counter_TSP = counter_TSP+1



   for row in table_Negative :
       index = table_Negative.index(row)
       row[0] = IPv4Network(row[0])
       table_Negative[index] = row

   for row in table_LISP :
       index = table_LISP.index(row)
       row[0] = IPv4Network(row[0])
       table_LISP[index] = row

   table_Negative = TSPs_table + sorted(table_Negative)
   table_LISP = TSPs_table + sorted(table_LISP)

   for row in table_Negative :
       index = table_Negative.index(row)
       row[0] = str(row[0])
       table_Negative[index] = row

   for row in table_LISP :
       index = table_LISP.index(row)
       row[0] = str(row[0])
       table_LISP[index] = row


   # Write the collected data for the Negative Map-Reply in '-Negative.csv'
   with open('Tables/'+str(map_resolver)+'-Negative.csv', 'w', newline='') as fp:
       a = csv.writer(fp, delimiter=',')
       a.writerows(table_Negative)
   # Write the collected data for the LISP Map-Reply in '-LISP.csv'
   with open('Tables/'+str(map_resolver)+'-LISP.csv', 'w', newline='') as fp:
       a = csv.writer(fp, delimiter=',')
       a.writerows(table_LISP)


sys.exit()



