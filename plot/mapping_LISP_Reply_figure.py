import sys
import time
import re
import os
import csv
import glob
import numpy
import statistics
import datetime
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
#from matplotlib.legend_handler import HandlerLine2D
#from statsmodels.distributions.empirical_distribution import ECDF
from measurements import results_from_lispmon
from config.config import *

# Parameters to Set
map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO
start_date = '20160818'
end_date   = '20160920'
Hour = 12

# Obtaining the Timestamps
TSPs = []
table = open('../Tables/' + map_resolvers[0] + '-LISP.csv', 'r')
reader = csv.reader(table)
for row in reader:
    del row[0]
    for TSP in row:
        Date = datetime.datetime.fromtimestamp(int(TSP))
        Date.timestamp()
        Date_str = str(Date.year)+str('%02d'%Date.month)+str('%02d'%Date.day)
        if int(start_date) <= int(Date_str) <= int(end_date) and Date.hour == 12:
            TSPs.append(datetime.datetime.fromtimestamp(int(TSP)))
    break

# Obtainning the Information from '-LISP.csv'
mapping_lists = []
for map_resolver in map_resolvers:
   counter_TSP = 0
   mapping_list = []
   while counter_TSP < len(TSPs):
       print(counter_TSP)
       counter_mapping = 0
       table = open('../Tables/' + map_resolver + '-LISP.csv', 'r')
       reader = csv.reader(table)
       for row in reader:
           if row[0] == '':
               TSP_position = row.index(str(int(TSPs[counter_TSP].timestamp())))
               continue
           #del row[0]
           if row[TSP_position] != '' :
               counter_mapping += 1
       counter_TSP +=1

       mapping_list.append(counter_mapping)

   mapping_lists.append(mapping_list)


# Getting the Number of LISP Reply from LISPmon
mapping_list_LISPmon =  results_from_lispmon.eid_prefix_num_counter(start_date , end_date)
del mapping_list_LISPmon[5]
del TSPs[14]
del TSPs[15]

# plot

dates = matplotlib.dates.date2num(TSPs)

# Plot the LISP reply for Map resolvers
for x in range(0 , len(map_resolvers)) :
    del mapping_lists[x][14]
    del mapping_lists[x][15]
    plt.plot_date(dates, mapping_lists[x]  , ls= '-' , marker='')

#Plot the LISP Reply for LISPmon
plt.plot_date(dates, mapping_list_LISPmon, ls='-', marker='')

#Setting

# To automatically produce the size of the figure
#mpl.rcParams['text.usetex'] = True
#mpl.rcParams.update({'figure.autolayout': True})
plt.grid(True)
plt.axis([ min(dates) , max(dates)  , 0 , 100 ])
plt.xlabel('Time')
plt.ylabel(' # LISP mappings ')
plt.gcf().autofmt_xdate()
#plt.xticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
#plt.yticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")

plt.show()

sys.exit()