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
from statsmodels.distributions.empirical_distribution import ECDF
from config.config import *



map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO
Negative_RTTs = []
LISP_RTTs = []
overall_RTTs = []

for map_resolver in map_resolvers:
  # table = open('test.csv', 'r')
   table = open('../Tables/'+map_resolver+'-Negative.csv', 'r')
   reader = csv.reader(table)
   for row in reader:
       if row[0] == '':
           continue
       del row[0]
       for Negative_RTT in row:
           if Negative_RTT != '':
               Negative_RTTs.append(float(Negative_RTT))


   table.close()


   table = open('../Tables/'+map_resolver+'-LISP.csv', 'r')
   reader = csv.reader(table)
   for row in reader:
       if row[0] == '':
           continue
       del row[0]
       for LISP_RTT in row:
           if LISP_RTT != '':
               LISP_RTTs.append(float(LISP_RTT))


   table.close()

   table = open('../Tables/'+map_resolver+'-Negative-LISP.csv', 'r')
   reader = csv.reader(table)
   for row in reader:
       if row[0] == '':
           continue
       del row[0]
       for overall_RTT in row:
           if overall_RTT != '':
               overall_RTTs.append(float(overall_RTT))


   table.close()


#Results
rtt_counter_500 = 0
rtt_counter_1000 = 0
rtt_counter_1500 = 0
rtt_counter_500_Negative = 0
rtt_counter_500_LISP = 0
for RTT in overall_RTTs :
    if RTT >= 500 :
        rtt_counter_500 += 1
    if RTT >= 1000 :
        rtt_counter_1000 += 1
    if RTT >= 1500 :
        rtt_counter_1500 += 1
for RTT in Negative_RTTs :
    if RTT >= 500 :
        rtt_counter_500_Negative += 1
for RTT in LISP_RTTs :
    if RTT >= 500 :
        rtt_counter_500_LISP += 1

rtt_counter_500 = (rtt_counter_500 / len(overall_RTTs))*100
rtt_counter_1000 = (rtt_counter_1000 / len(overall_RTTs))*100
rtt_counter_1500 = (rtt_counter_1500 / len(overall_RTTs))* 100
rtt_counter_500_Negative = (rtt_counter_500_Negative / len(Negative_RTTs))* 100
rtt_counter_500_LISP = (rtt_counter_500_LISP / len(LISP_RTTs))* 100


print( 'exceed 500 ms = ' + str(rtt_counter_500) +'%')
print( 'exceed 1000 ms = ' + str(rtt_counter_1000)+'%')
print( 'exceed 1500 ms = ' + str(rtt_counter_1500)+'%')
print( 'Negative Reply exceed 500 ms = ' + str(rtt_counter_500_Negative)+'%')
print( 'LISP Reply exceed 500 ms = ' + str(rtt_counter_500_LISP)+'%')


# Obtains the ECDF

ecdf_negative = ECDF(Negative_RTTs)
ecdf_lisp = ECDF(LISP_RTTs)
ecdf_overall = ECDF(overall_RTTs)


# Plot the Figure
# To automatically produce the size of the figure
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})

negative , =plt.plot(ecdf_negative.x , ecdf_negative.y  , 'r-' , label = 'Negative Map-Reply' )
answered , =plt.plot(ecdf_lisp.x , ecdf_lisp.y , 'g--' , label = 'LISP Map-Reply')
overall ,  =plt.plot(ecdf_overall.x , ecdf_overall.y , 'b-.'  , label = 'overall')
plt.legend(handler_map={negative : HandlerLine2D(numpoints=1)})
plt.legend(handler_map={answered : HandlerLine2D(numpoints=1)})
plt.legend(handler_map={overall: HandlerLine2D(numpoints=1)})
plt.legend(handles=[negative , answered, overall], loc=4)
plt.axis([ 0 , 5000 , 0 , 1])
plt.grid(True)
plt.xlabel('rtt(ms)', fontLabel)
plt.ylabel('ecdf', fontLabel)
plt.xticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
plt.yticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
plt.show()

sys.exit()