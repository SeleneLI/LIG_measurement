import sys
import re
import csv
import glob
import ipaddress
from ipaddress import IPv4Address, IPv4Network

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

TSPs_table = [[''] + TSPs]
print(len(TSPs))
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
          if loc_count != '0\n' :
              Found = False
              if table != [] :
                   for search_row in table :
                       index = table.index(search_row)
                       if re.split( r"[/]" , EID_Prefix)[0] == re.split( r"[/]" , search_row[0])[0] :
                            search_row[counter_TSP] = loc_count
                            search_row[0] = str(EID_Prefix)
                            table[index]=search_row
                            Found = True
                            break
                   if Found == False:

                       row[0] = EID_Prefix
                       row[counter_TSP] = loc_count
                       table.append(row)
              else:
                     row[0]=EID_Prefix
                     row[counter_TSP] = loc_count
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

   with open('Tables/'+str(map_resolver)+'-LISP-#RLOCs.csv', 'w', newline='') as fp:
       a = csv.writer(fp, delimiter=',')
       a.writerows(table)




sys.exit()



