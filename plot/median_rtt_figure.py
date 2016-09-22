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



map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO

Total_median_negative_MRs = []
Total_median_LISP_MRs = []
Total_median_ALL_MRs = []
MRs = [ 1 ,2 ,3 ,4 , 5 , 6 ,7 ,8 ]
for map_resolver in map_resolvers:
   #table = open('test.csv', 'r')
   table = open('../Tables/'+map_resolver+'-Negative.csv', 'r')
   reader = csv.reader(table)
   row_medians = []
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
       #median = statistics.median(sorted(row_floats))
       #row_medians.append(median)

   #Total_median_MR = statistics.median(sorted(row_medians))
   Total_median_MR = statistics.median(sorted(RTTs))
   Total_median_negative_MRs.append(Total_median_MR)


   table.close()


   table = open('../Tables/'+map_resolver+'-LISP.csv', 'r')
   reader = csv.reader(table)
   row_medians = []
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
       #median = statistics.median(sorted(row_floats))
       #row_medians.append(median)


   #Total_median_MR = statistics.median(sorted(row_medians))
   Total_median_MR = statistics.median(sorted(RTTs))
   Total_median_LISP_MRs.append(Total_median_MR)

   table.close()

   table = open('../Tables/'+map_resolver+'-Negative-LISP.csv', 'r')
   reader = csv.reader(table)
   row_medians = []
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
       #median = statistics.median(sorted(row_floats))
       #row_medians.append(median)

   #Total_median_MR = statistics.median(sorted(row_medians))
   Total_median_MR = statistics.median(sorted(RTTs))
   Total_median_ALL_MRs.append(Total_median_MR)

   table.close()



# Plot the Figure

negative , =plt.plot(MRs , Total_median_negative_MRs  , 'ro' , label = 'Negative Map-Reply' )
answered , =plt.plot(MRs , Total_median_LISP_MRs , 'gx' , label = 'LISP Map-Reply')
overall ,  =plt.plot(MRs , Total_median_ALL_MRs , 'b^'  , label = 'overall')
plt.legend(handler_map={negative : HandlerLine2D(numpoints=1)})
plt.legend(handler_map={answered : HandlerLine2D(numpoints=1)})
plt.legend(handler_map={overall: HandlerLine2D(numpoints=1)})
plt.legend(handles=[negative , answered, overall], loc=10)
plt.axis([ 0 , 9 , 0 , max(Total_median_ALL_MRs + Total_median_LISP_MRs + Total_median_negative_MRs)+50])  # 1600
plt.grid(True)
plt.xlabel('resolver')
plt.ylabel(' median rtt(ms)')
#plt.axhspan(ymin= 0 , ymax=550 ,  xmin=0 , xmax=3.5 )   # 3*EUROP , 3*US , 2*ASIA
plt.axvline(x= 3.5, color = 'k', linewidth = 1)
plt.axvline(x= 6.5, color = 'k', linewidth = 1)
plt.text( 1, 1300, 'EUROPE', style='italic' , fontsize=20)
plt.text( 4.5, 1300, 'US', style='italic' , fontsize=20)
plt.text( 7.5, 1300, 'ASIA', style='italic' , fontsize=20)
plt.show()

sys.exit()