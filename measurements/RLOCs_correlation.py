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

map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50'   , '149.20.48.61' , '149.20.48.77', '206.223.132.89', '202.214.86.252' , '202.51.247.10'] # 3*EURO

TSPs = []
mapping_list = []
table = open('Tables/' + map_resolvers[0] + '-LISP-#RLOCs.csv', 'r')
reader = csv.reader(table)
for row in reader:
    del row[0]
    for TSP in row:
        TSPs.append(datetime.datetime.fromtimestamp(int(TSP)))
    break
Num_MR = len(map_resolvers)
TSP_counter = 1


correlation_tables = []
# EIDs-list for each Map Resolver
while TSP_counter < len(TSPs):
    EIDs_MRs_list = []
    RLOCs_MRs_list = []
    MR_counter = 0
    while MR_counter < Num_MR:
        EIDs_MR = []
        RLOCs_MR = []
        file = open('Tables/' + map_resolvers[MR_counter] + '-LISP-#RLOCs.csv', 'r')
        reader = csv.reader(file)
        for row in reader:
            if row[0] == '':
                continue
            if row[TSP_counter] != '' :
                EIDs_MR.append(row[0])
                RLOCs_MR.append(int(row[TSP_counter]))

        MR_counter += 1

        EIDs_MRs_list.append(EIDs_MR)
        RLOCs_MRs_list.append(RLOCs_MR)



    # EIDs -list intersection
    intersect = set(EIDs_MRs_list[0]).intersection(EIDs_MRs_list[1])
    i = 2
    while i < len(EIDs_MRs_list) :
        intersect = set(intersect).intersection(EIDs_MRs_list[i])
        i += 1

    # RLOCs intersection
    RLOCs_MRs_list_intersect = []
    intersect = list(intersect)
    MR_counter = 0
    for MR in EIDs_MRs_list :
        RLOCs_MR_intersect = []
        for EID in intersect :
            index = MR.index(EID)
            RLOCs_MR_intersect.append(RLOCs_MRs_list[MR_counter][index])

        RLOCs_MRs_list_intersect.append(RLOCs_MR_intersect)
        MR_counter += 1

   # calculate the correlation for each TSP

    correlation_table = []
    for MR_1 in RLOCs_MRs_list_intersect :
        correlation_row = []
        for MR_2 in RLOCs_MRs_list_intersect :
            correlation_row.append(pearsonr(MR_1,MR_2)[0])

        correlation_table.append(correlation_row)

    print(TSP_counter, ' ', len(intersect))
    TSP_counter += 1
    correlation_tables.append(correlation_table)
# calculate the Average correlation
Avg_correlation_table = [[0]*Num_MR]*Num_MR

for table in correlation_tables:
    for MR in table :
        for correlation in MR :
              Avg_correlation_table[table.index(MR)][MR.index(correlation)] += correlation

for MR in Avg_correlation_table:
    for correlation in MR :
        Avg_correlation_table[Avg_correlation_table.index(MR)][MR.index(correlation)] =  Avg_correlation_table[Avg_correlation_table.index(MR)][MR.index(correlation)] / len(correlation_tables)