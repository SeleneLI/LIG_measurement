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
start_date = '20160904'
end_date   = '20161004'

# Obtaining the Timestamps
TSPs = []
TSPs_fixed_hour = []
table = open('../Tables/' + map_resolvers[0] + '-Negative-LISP.csv', 'r')
reader = csv.reader(table)
for row in reader:
    del row[0]
    for TSP in row:
        Date = datetime.datetime.fromtimestamp(int(TSP))
        Date.timestamp()
        Date_str = str(Date.year)+str('%02d'%Date.month)+str('%02d'%Date.day)
        if int(start_date) <= int(Date_str) <= int(end_date) :
           TSPs.append(datetime.datetime.fromtimestamp(int(TSP)))

    break

# Obtainning the Information from '-Negative-LISP.csv' for all the Timestamps
mapping_lists = [] #for each map resolver
mapping_overall = [] #combined all the map resolvers
MR_counter = 0
for map_resolver in map_resolvers:
   counter_TSP = 0
   mapping_list = []

   while counter_TSP < len(TSPs):
       print(counter_TSP)
       counter_mapping = 0
       x = []
       table = open('../Tables/' + map_resolver + '-Negative-LISP.csv', 'r')
       reader = csv.reader(table)
       for row in reader:
           if row[0] == '':
               TSP_position = row.index(str(int(TSPs[counter_TSP].timestamp())))
               continue
           #del row[0]
           if row[TSP_position] != '' :
               counter_mapping += 1
               if MR_counter == 0 :
                   x.append(row[0])
               else:
                   if row[0] not in mapping_overall[counter_TSP] :
                       mapping_overall[counter_TSP].append(row[0])

       counter_TSP +=1
       mapping_list.append(counter_mapping)
       if MR_counter == 0 :
            mapping_overall.append(x)
   mapping_lists.append(mapping_list)
   MR_counter += 1



# Plot the overall LISP Replies for all the Timestamps
mapping_overall_number = []
for x in mapping_overall:
    mapping_overall_number.append(len(x))


Zero_position = mapping_overall_number.index(2)
mapping_overall_number[Zero_position] = mapping_overall_number[Zero_position-1]

Zero_position = mapping_overall_number.index(2)
mapping_overall_number[Zero_position] = mapping_overall_number[Zero_position-1]

Zero_position = mapping_overall_number.index(2)
mapping_overall_number[Zero_position] = mapping_overall_number[Zero_position-1]
# plot

#dates = matplotlib.dates.date2num(TSPs)  # let the Timestamps readable

plt.figure(figsize=(10, 5))  # adjust the size of the figure

#Plot the LISP Replies of our project for all the timestamps
plt.plot_date(TSPs, mapping_overall_number,color= 'g', ls='-', marker='' , label = 'LISP-Views' )

# Setting

# To automatically produce the size of the figure

mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})
plt.grid(True)
#plt.axis([ TSPs[0] , TSPs[len(TSPs)-1]  , 0 , max(mapping_overall_number)+5 ])
#plt.xticks()
plt.xlabel('Time' , fontsize=20)
plt.ylabel(' Number of Mappings ' , fontsize=20)
#plt.title('Mapping Number')
plt.legend(loc='best')
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 2))
plt.xticks( fontsize=10, fontname="Times New Roman") # np.arange(min(TSPs), max(TSPs), 2),
plt.yticks(fontsize=15, fontname="Times New Roman")







# To check if the Figures path exists, otherise we create one
try:
    os.stat(os.path.join(FIGURE_PATH))
except:
    os.makedirs(os.path.join(FIGURE_PATH))
plt.savefig(os.path.join(FIGURE_PATH, 'Mapping_for_ALL_MRs.eps'), dpi=300, transparent=True ) # you can change the name, just an example
plt.show() # When you use the above command to save the figure, you can choose to don't show the figure anymore



sys.exit()