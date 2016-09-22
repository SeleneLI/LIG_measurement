import sys
import time
import re
import os
import csv
import glob
import numpy as np
import statistics
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from statsmodels.distributions.empirical_distribution import ECDF



map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO
Negative_From_MR_counter = 0
Negative_From_others_counter = 0
Negative_Total_TSPs = 0
LISP_From_MR_counter = 0
LISP_From_RLOCs_counter = 0
LISP_From_others_counter = 0
LISP_Total_TSPs = 0
for map_resolver in map_resolvers:
   table = open('../Tables/'+map_resolver+'-stability.csv', 'r')
   reader = csv.reader(table)
   for row in reader:
        if row[0] == 'EID Prefix' :
            continue
        if row[1] == 'LISP Reply':
            LISP_From_MR_counter += int(row[13])
            LISP_From_RLOCs_counter += int(row[12])
            LISP_From_others_counter += int(row[11])
            LISP_Total_TSPs += int(row[14])
        else:
            Negative_From_MR_counter += int(row[13])
            Negative_From_others_counter += (int(row[14]) - int(row[13]))
            Negative_Total_TSPs += int(row[14])


Negative_From_MR = round((Negative_From_MR_counter / Negative_Total_TSPs)*100 , 3)
Negative_From_others = round((Negative_From_others_counter / Negative_Total_TSPs)*100 , 3)

LISP_From_MR =round((LISP_From_MR_counter / LISP_Total_TSPs)*100 , 3)
LISP_From_RLOCs = round((LISP_From_RLOCs_counter / LISP_Total_TSPs)*100 ,3)
LISP_From_others= round((LISP_From_others_counter / LISP_Total_TSPs)*100 , 3 )


print('Negative Reply comes from MR = ' , Negative_From_MR , ' %')
print('Negative Reply comes from others = ' , Negative_From_others , ' %')
print('LISP Reply comes from MR = ' , LISP_From_MR , ' %')
print('LISP Reply comes from RLOCs = ' , LISP_From_RLOCs , ' %')
print('LISP Reply comes from others = ' , LISP_From_others , ' %')

sys.exit()