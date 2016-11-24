import sys
import time
import re
import os
import math
import csv
import glob
import numpy as np
import statistics
import  ipaddress
import datetime
from scipy.stats.stats import pearsonr



# List of the Map Resolver which will be measured
map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO

# Get the Timesstamp from Tables directory
TSPs = []
mapping_list = []
table = open('Tables/' + map_resolvers[0] + '-LISP.csv', 'r')
reader = csv.reader(table)
for row in reader:
    del row[0]
    for TSP in row:
        TSPs.append(datetime.datetime.fromtimestamp(int(TSP)))
    break

Num_MR = len(map_resolvers)
MR_counter = 0
correlation_Tables = []
Max_len = 0
EIDs_MRs_list = []
correlation_Table = []
while MR_counter < Num_MR:
    EIDs_count_MR = []
    TSP_counter = 1
    while TSP_counter < len(TSPs):
        EIDs_MR = []
        file = open('Tables/' + map_resolvers[MR_counter] + '-LISP.csv', 'r') #'-Negative-LISP.csv'
        reader = csv.reader(file)
        for row in reader:
            if row[0] == '':
                continue
            if row[TSP_counter] != '' :
                EIDs_MR.append(int(ipaddress.IPv4Address(row[0].split('/')[0])))

        EIDs_count_MR.append(len(EIDs_MR))
        TSP_counter += 1
    EIDs_MRs_list.append(EIDs_count_MR)
    MR_counter += 1


# filter the Tables
MR_counter_0 = 0
while MR_counter_0 < Num_MR:
      indexes = np.where(np.array(EIDs_MRs_list[MR_counter_0]) == 0)
      MR_counter_1 = 0
      while MR_counter_1 < Num_MR :
         i = 0
         for index in indexes[0]:
             del EIDs_MRs_list[MR_counter_1][index - i]
             i += 1
         MR_counter_1 += 1
      MR_counter_0 += 1

# calculate the correlation
MR_counter_0 = 0
while MR_counter_0 < Num_MR:
    correlation_row = []
    MR_counter_1 = 0
    while MR_counter_1 < Num_MR :
        correlation_row.append(math.ceil(pearsonr(EIDs_MRs_list[MR_counter_0], EIDs_MRs_list[MR_counter_1])[0]*1000)/1000) # np.corrcoef(EIDs_MRs_list[MR_counter_0], EIDs_MRs_list[MR_counter_1])[0, 1]
        MR_counter_1 += 1
    correlation_Table.append(correlation_row)
    MR_counter_0 += 1
# print
i = 0
for x in correlation_Table :
    MR =  'MR' + str(i)+ ':'
    print(MR , x)
    i +=1

sys.exit()