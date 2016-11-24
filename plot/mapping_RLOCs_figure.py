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
table = open('../Tables/' + map_resolvers[0] + '-LISP-#RLOCs.csv', 'r')
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
       counter_RLOC = 0
       table = open('../Tables/' + map_resolver + '-LISP-#RLOCs.csv', 'r')
       reader = csv.reader(table)
       for row in reader:
           if row[0] == '':
               TSP_position = row.index(str(int(TSPs[counter_TSP].timestamp())))
               continue
           #del row[0]
           if row[TSP_position] != '' :
               counter_RLOC += int(row[TSP_position])
       counter_TSP +=1

       mapping_list.append(counter_RLOC)

   mapping_lists.append(mapping_list)


# Getting the Number of LISP Reply from LISPmon
mapping_list_LISPmon =  results_from_lispmon.rloc_num_counter(start_date , end_date)


del mapping_list_LISPmon[5]
del TSPs[14]
del TSPs[15]

# plot

dates = matplotlib.dates.date2num(TSPs)

plt.figure(figsize=(20, 9))  # adjust the size of the figure
# Plot the LISP reply for Map resolvers
for x in range(0 , len(map_resolvers)) :
    del mapping_lists[x][14]
    del mapping_lists[x][15]
    plt.plot_date(dates, mapping_lists[x]  , ls= '-' , marker='' , label = 'MR ' + str(x+1))

#Plot the LISP Reply for LISPmon
plt.plot_date(dates, mapping_list_LISPmon, ls='-', marker='' , label = 'LISPmon')

#Setting

# To automatically produce the size of the figure
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})
plt.grid(True)
plt.axis([ min(dates) , max(dates)  , 0 , 100 ])
plt.xlabel('Time')
plt.ylabel(' Number of RLOCs ')
plt.legend( bbox_to_anchor=(1.01, 1.), loc=2, borderaxespad=0.)
plt.gcf().autofmt_xdate()


try:
    os.stat(os.path.join(FIGURE_PATH))
except:
    os.makedirs(os.path.join(FIGURE_PATH))
plt.savefig(os.path.join(FIGURE_PATH, 'Mapping_RLOCs.eps'), dpi=300,transparent=True)  # you can change the name, just an example
plt.show()  # When you use the above command to save the figure, you can choose to don't show the figure anymore

sys.exit()