import sys
import re
import csv
import glob
import ipaddress
from ipaddress import IPv4Address, IPv4Network


# List of the Map Resolver which will be measured
map_resolvers  = ['137.194.18.132']

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

TSPs_table = [[''] + TSPs]
print(len(TSPs))
# collecting the data for each Map Resolver
for map_resolver in map_resolvers:
   table = []
   counter_TSP = 1
   for TSP in TSPs :
      PATH =  'data/'+ str(map_resolver) + '/*'+str(map_resolver)+'-'+str(TSP)+'.log'
      file_names = glob.glob(PATH)
      print(counter_TSP)
      for file_name in file_names :
          row = [''] * (len(TSPs)+1)
          EID_Prefix = re.split(r"[-]" , file_name)[1]
          EID_Prefix = EID_Prefix.replace(':', '/')
          file = open(file_name , 'r')
          data = file.readlines()
          if 'LOCATOR_COUNT' not in data[8] :
              continue
          loc_count = data[8]
          loc_count = re.split(r"[=]", loc_count)[1]
          RTT = data[7]
          RTT = re.split(r"[=]", RTT)[1]
          RTT = RTT.replace('ms\n', '')
          Found = False
          if table != [] :
               for search_row in table :
                   index = table.index(search_row)
                   if re.split( r"[/]" , EID_Prefix)[0] == re.split( r"[/]" , search_row[0])[0] :
                        search_row[counter_TSP] = RTT
                        search_row[0] = str(EID_Prefix)
                        table[index]=search_row
                        Found = True
                        break
               if Found == False:

                   row[0] = EID_Prefix
                   row[counter_TSP] = RTT
                   table.append(row)
          else:
                 row[0]=EID_Prefix
                 row[counter_TSP] = RTT
                 table.append(row)


      counter_TSP = counter_TSP+1

   for row in table :
       index = table.index(row)
       row[0] = IPv4Network(row[0])
       table[index] = row

   table = TSPs_table + sorted(table)
   for row in table :
       index = table.index(row)
       row[0] = str(row[0])
       table[index] = row

   # Write the collected data for the Negative and LISP Map-Reply in '-Negative-LISP.csv'
   with open('Tables/'+str(map_resolver)+'-Negative-LISP.csv', 'w', newline='') as fp:
       a = csv.writer(fp, delimiter=',')
       a.writerows(table)




sys.exit()



