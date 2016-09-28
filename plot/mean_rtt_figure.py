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


map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO

Total_mean_negative_MRs = []
Total_mean_LISP_MRs = []
Total_mean_ALL_MRs = []
MRs = [ 1 ,2 ,3 ,4 , 5 , 6 ,7 ,8 ]
for map_resolver in map_resolvers:
   #table = open('test.csv', 'r')
   table = open('../Tables/'+map_resolver+'-Negative.csv', 'r')
   reader = csv.reader(table)
   row_means = []
   RTTs = []
   for row in reader:
       if row[0] == '':
           continue
       row_floats = []
       del row[0]
       for x in row:
           if x != '':
               #row_floats.append(float(x))
                RTTs.append(float(x))
       #mean = statistics.mean(sorted(row_floats))
       #row_means.append(mean)

   #Total_mean_MR = statistics.mean(sorted(row_means))
   Total_mean_MR = statistics.mean(sorted(RTTs))
   Total_mean_negative_MRs.append(Total_mean_MR)


   table.close()


   table = open('../Tables/'+map_resolver+'-LISP.csv', 'r')
   reader = csv.reader(table)
   row_means = []
   RTTs = []
   for row in reader:
       if row[0] == '':
           continue
       row_floats = []
       del row[0]
       for x in row:
           if x != '':
               #row_floats.append(float(x))
               RTTs.append(float(x))
       #mean = statistics.mean(sorted(row_floats))
       #row_means.append(mean)

   #Total_mean_MR = statistics.mean(sorted(row_means))
   Total_mean_MR = statistics.mean(sorted(RTTs))
   Total_mean_LISP_MRs.append(Total_mean_MR)

   table.close()

   table = open('../Tables/'+map_resolver+'-Negative-LISP.csv', 'r')
   reader = csv.reader(table)
   row_means = []
   RTTs = []
   for row in reader:
       if row[0] == '':
           continue
       row_floats = []
       del row[0]
       for x in row:
           if x != '':
               #row_floats.append(float(x))
               RTTs.append(float(x))
       #mean = statistics.mean(sorted(row_floats))
       #row_means.append(mean)

   #Total_mean_MR = statistics.mean(sorted(row_means))
   Total_mean_MR = statistics.mean(sorted(RTTs))
   Total_mean_ALL_MRs.append(Total_mean_MR)


   table.close()



# Plot the Figure
# To automatically produce the size of the figure
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})

negative , =plt.plot(MRs , Total_mean_negative_MRs  , 'ro' , label = 'Negative Map-Reply' )
answered , =plt.plot(MRs , Total_mean_LISP_MRs , 'gx' , label = 'LISP Map-Reply')
overall ,  =plt.plot(MRs , Total_mean_ALL_MRs , 'b^'  , label = 'overall')
plt.legend(handler_map={negative : HandlerLine2D(numpoints=1)})
plt.legend(handler_map={answered : HandlerLine2D(numpoints=1)})
plt.legend(handler_map={overall: HandlerLine2D(numpoints=1)})
plt.legend(handles=[negative , answered, overall], loc=4)
plt.axis([ 0 , 9 , 200 , max(Total_mean_ALL_MRs + Total_mean_LISP_MRs + Total_mean_negative_MRs)+50]) # 200 , 1200
plt.grid(True)
plt.xlabel('resolver')
plt.ylabel(' mean rtt(ms)')
plt.axvline(x= 3.5, color = 'k', linewidth = 1)
plt.axvline(x= 6.5, color = 'k', linewidth = 1)
plt.text( 1, 950, 'EUROPE', style='italic' , fontsize=20)
plt.text( 4.5, 950, 'US', style='italic' , fontsize=20)
plt.text( 7.5, 950, 'ASIA', style='italic' , fontsize=20)
plt.xticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
plt.yticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
# To check if the Figures path exists, otherise we create one
try:
    os.stat(os.path.join(FIGURE_PATH))
except:
    os.makedirs(os.path.join(FIGURE_PATH))
plt.savefig(os.path.join(FIGURE_PATH, 'mean_of_RTT.eps'), dpi=300, transparent=True) # you can change the name, just an example
plt.show() # When you use the above command to save the figure, you can choose to don't show the figure anymore

sys.exit()