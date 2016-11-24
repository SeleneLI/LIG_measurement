import sys
import time
import re
import os
import csv
import glob
import numpy
import statistics
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from config.config import *


map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50'  , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO
#'149.20.48.61' , '149.20.48.77'

start_date = '20160904'
end_date   = '20161004'

# Obtaining the Timestamps
TSPs = []

table = open('../Tables/' + map_resolvers[0] + '-Negative.csv', 'r')
reader = csv.reader(table)
for row in reader:
    del row[0]
    for TSP in row:
        Date = datetime.datetime.fromtimestamp(int(TSP))
        Date.timestamp()
        Date_str = str(Date.year)+str('%02d'%Date.month)+str('%02d'%Date.day)
        if int(start_date) <= int(Date_str) <= int(end_date) :
            TSPs.append(TSP)  #datetime.datetime.fromtimestamp(int(TSP))
    break

Total_median_negative_MRs = []
Total_median_LISP_MRs = []
Total_median_ALL_MRs = []
MRs = [ 1 ,2 ,3 ,4 , 5 , 6  ]
for map_resolver in map_resolvers:

   table = open('../Tables/'+map_resolver+'-Negative.csv', 'r')
   reader = csv.reader(table)
   row_medians = []
   RTTs = []
   for row in reader:
       if row[0] == '':
           Start_position = row.index(TSPs[0])
           End_position = row.index(TSPs[len(TSPs) - 1])
           continue
       row_floats = []
       del row[0]
       TSP_counter = Start_position
       while TSP_counter <= End_position:
           if row[TSP_counter] != '':
               RTTs.append(float(row[TSP_counter]))
               TSP_counter += 1
           else:
               TSP_counter += 1

   Total_median_MR = statistics.median(sorted(RTTs))
   Total_median_negative_MRs.append(Total_median_MR)


   table.close()


   table = open('../Tables/'+map_resolver+'-LISP.csv', 'r')
   reader = csv.reader(table)
   row_medians = []
   RTTs = []
   for row in reader:
       if row[0] == '':
           Start_position = row.index(TSPs[0])
           End_position = row.index(TSPs[len(TSPs) - 1])
           continue
       row_floats = []
       del row[0]

       TSP_counter = Start_position
       while TSP_counter <= End_position:
           if row[TSP_counter] != '':

               RTTs.append(float(row[TSP_counter]))
               TSP_counter += 1
           else:
               TSP_counter += 1

   Total_median_MR = statistics.median(sorted(RTTs))
   Total_median_LISP_MRs.append(Total_median_MR)

   table.close()

   table = open('../Tables/'+map_resolver+'-Negative-LISP.csv', 'r')
   reader = csv.reader(table)
   row_medians = []
   RTTs = []
   for row in reader:
       if row[0] == '':
           Start_position = row.index(TSPs[0])
           End_position = row.index(TSPs[len(TSPs) - 1])
           continue
       row_floats = []
       del row[0]
       # for x in row:
       TSP_counter = Start_position
       while TSP_counter <= End_position:
           if row[TSP_counter] != '':

               RTTs.append(float(row[TSP_counter]))
               TSP_counter += 1
           else:
               TSP_counter += 1

   Total_median_MR = statistics.median(sorted(RTTs))
   Total_median_ALL_MRs.append(Total_median_MR)

   table.close()



# Plot the Figure
# To automatically produce the size of the figure
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})

negative , =plt.plot(MRs , Total_median_negative_MRs  , 'ro' , label = 'Negative Map-Reply' , ms= 10 )
answered , =plt.plot(MRs , Total_median_LISP_MRs , 'gx' , label = 'LISP Map-Reply' , ms= 10)
overall ,  =plt.plot(MRs , Total_median_ALL_MRs , 'b^'  , label = 'overall' , ms= 10)

plt.legend(handles=[negative , answered, overall], loc=10 , numpoints=1)
plt.axis([ 0 , 7 , 0 , max(Total_median_ALL_MRs + Total_median_LISP_MRs + Total_median_negative_MRs)+50])  # 1600
plt.grid(True)
plt.xlabel('Map Resolver' , fontsize=25)
plt.ylabel(' Median RTT(ms)' , fontsize=25)

plt.axvline(x= 3.5, color = 'k', linewidth = 1)
plt.axvline(x= 4.5, color = 'k', linewidth = 1)
plt.text( 1, 1300, 'EUROPE', style='italic' , fontsize=20)
plt.text( 3.7, 1300, 'US', style='italic' , fontsize=20)
plt.text( 5.5, 1300, 'ASIA', style='italic' , fontsize=20)
plt.xticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
plt.yticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
# To check if the Figures path exists, otherise we create one
try:
    os.stat(os.path.join(FIGURE_PATH))
except:
    os.makedirs(os.path.join(FIGURE_PATH))
plt.savefig(os.path.join(FIGURE_PATH, 'median_of_RTT.eps'), dpi=300, transparent=True) # you can change the name, just an example
plt.show() # When you use the above command to save the figure, you can choose to don't show the figure anymore

sys.exit()