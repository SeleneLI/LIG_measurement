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
table = open('../Tables/' + map_resolvers[0] + '-LISP.csv', 'r')
reader = csv.reader(table)
for row in reader:
    del row[0]
    for TSP in row:
        Date = datetime.datetime.fromtimestamp(int(TSP))
        Date.timestamp()
        Date_str = str(Date.year)+str('%02d'%Date.month)+str('%02d'%Date.day)
        if int(start_date) <= int(Date_str) <= int(end_date) :
            TSPs.append(datetime.datetime.fromtimestamp(int(TSP)))
        if int(start_date) <= int(Date_str) <= int(end_date) and Date.hour == 12:
            TSPs_fixed_hour.append(datetime.datetime.fromtimestamp(int(TSP)))

    break

# Obtainning the Information from '-LISP.csv' for all the Timestamps
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
       table = open('../Tables/' + map_resolver + '-LISP.csv', 'r')
       reader = csv.reader(table)
       for row in reader:
           if row[0] == '':
               TSP_position = row.index(str(int(TSPs[counter_TSP].timestamp())))
               continue

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



# Getting the Number of LISP Reply from LISPmon
mapping_list_LISPmon =  results_from_lispmon.eid_prefix_num_counter(start_date , end_date)


# Obtainning the LISP Reply for the whole day
TSP_counter = 2
Day_counter = 2
mapping_overall_day = []
union = set(mapping_overall[0]).union(set(mapping_overall[1]))
while TSP_counter < len(mapping_overall):
    union = set(union).union(set(mapping_overall[TSP_counter]))
    TSP_counter += 1
    Day_counter += 1
    if Day_counter == 12:
        Day_counter = 0
        mapping_overall_day.append(union)
        union = set()

# Plot the overall LISP Replies for all the Timestamps
mapping_overall_day_number = []
for x in mapping_overall_day:
    mapping_overall_day_number.append(len(x) - 1)

# Just Some setting because some exception in some Timestamps
del mapping_list_LISPmon[4]


#measurements

print(max(mapping_list_LISPmon))
print(max(mapping_overall_day_number))
diff = []
for x , y in zip( mapping_overall_day_number , mapping_list_LISPmon):
    diff.append( x-y)

print(max(diff))
counter_20 = 0
for x in diff :
    if x >= 20 :
        counter_20 +=1

# plot

dates_fixed_hour = matplotlib.dates.date2num(TSPs_fixed_hour)  # let the Timestamps readable

days =list(range(1, len(dates_fixed_hour)+1))




# Plot the LISP Reply for LISPmon
plt.plot(days, mapping_list_LISPmon, ls='', marker='o' , label = 'LISPmon' , linewidth= 3 , ms=9)


#Plot the LISP Replies of our project for all the timestamps
plt.plot(days, mapping_overall_day_number,color= 'g', ls='', marker='^' , label = 'LISP-Views' , linewidth= 3 , ms=9)

# Setting

# To automatically produce the size of the figure

mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})
plt.grid(True)
plt.axis([ min(days)-1 , max(days)+1  , min(mapping_list_LISPmon)-5 , max(mapping_overall_day_number)+5 ])
plt.xticks(days)
plt.xlabel('Days'  , fontsize=25)
plt.ylabel(' Number of LISP Map-Reply ' , fontsize=25)
#plt.title('Comparison between LISPmon and Our Project per day')
plt.legend(loc='best' , numpoints=1)


#plt.xticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
plt.yticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")







# To check if the Figures path exists, otherise we create one
try:
    os.stat(os.path.join(FIGURE_PATH))
except:
    os.makedirs(os.path.join(FIGURE_PATH))
plt.savefig(os.path.join(FIGURE_PATH, 'LISPmon_comparison_day.eps'), dpi=300, transparent=True ) # you can change the name, just an example
plt.show() # When you use the above command to save the figure, you can choose to don't show the figure anymore



sys.exit()