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

#FIGURE_PATH = os.path.join('Figures')

map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO

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

Negative_RTTs = []
LISP_RTTs = []
overall_RTTs = []

for map_resolver in map_resolvers:

   table = open('../Tables/'+map_resolver+'-Negative.csv', 'r')
   reader = csv.reader(table)
   for row in reader:
       if row[0] == '':
           Start_position = row.index(TSPs[0])
           End_position = row.index(TSPs[len(TSPs)-1])
           continue
       del row[0]
       #for Negative_RTT in row:
       TSP_counter = Start_position
       while TSP_counter <= End_position:
           #if Negative_RTT != '':
           if row[TSP_counter] != '':
               Negative_RTTs.append(float(row[TSP_counter]))#Negative_RTT
               TSP_counter += 1
           else:
               TSP_counter += 1


   table.close()


   table = open('../Tables/'+map_resolver+'-LISP.csv', 'r')
   reader = csv.reader(table)
   for row in reader:
       if row[0] == '':
           Start_position = row.index(TSPs[0])
           End_position = row.index(TSPs[len(TSPs) - 1])
           continue
       del row[0]
       # for Negative_RTT in row:
       TSP_counter = Start_position
       while TSP_counter <= End_position:
           # if Negative_RTT != '':
           if row[TSP_counter] != '':
               LISP_RTTs.append(float(row[TSP_counter]))  # Negative_RTT
               TSP_counter += 1
           else:
               TSP_counter += 1


   table.close()

   table = open('../Tables/'+map_resolver+'-Negative-LISP.csv', 'r')
   reader = csv.reader(table)
   for row in reader:
       if row[0] == '':
           Start_position = row.index(TSPs[0])
           End_position = row.index(TSPs[len(TSPs) - 1])
           continue
       del row[0]
       # for Negative_RTT in row:
       TSP_counter = Start_position
       while TSP_counter <= End_position:
           # if Negative_RTT != '':
           if row[TSP_counter] != '':
               overall_RTTs.append(float(row[TSP_counter]))  # Negative_RTT
               TSP_counter += 1
           else:
               TSP_counter += 1


   table.close()


#Results

rtt_counter_500 = 0
rtt_counter_1000 = 0
rtt_counter_1500 = 0
rtt_counter_500_Negative = 0
rtt_counter_within_500_Negative = 0
rtt_counter_500_LISP = 0
rtt_counter_within_500_LISP = 0
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
    if 500 <= RTT < 600:
        rtt_counter_within_500_Negative +=1
for RTT in LISP_RTTs :
    if  RTT >= 500 :
        rtt_counter_500_LISP += 1
    if 500 <= RTT < 600 :
        rtt_counter_within_500_LISP +=1

rtt_counter_500 = (rtt_counter_500 / len(overall_RTTs))*100
rtt_counter_1000 = (rtt_counter_1000 / len(overall_RTTs))*100
rtt_counter_1500 = (rtt_counter_1500 / len(overall_RTTs))* 100
rtt_counter_500_Negative = (rtt_counter_500_Negative / len(Negative_RTTs))* 100
rtt_counter_within_500_Negative = (rtt_counter_within_500_Negative / len(Negative_RTTs))* 100
rtt_counter_500_LISP = (rtt_counter_500_LISP / len(LISP_RTTs))* 100
rtt_counter_within_500_LISP = (rtt_counter_within_500_LISP / len(LISP_RTTs))* 100


print( 'exceed 500 ms = ' + str(rtt_counter_500) +'%')
print( 'exceed 1000 ms = ' + str(rtt_counter_1000)+'%')
print( 'exceed 1500 ms = ' + str(rtt_counter_1500)+'%')
print( 'Negative Reply exceed 500 ms = ' + str(rtt_counter_500_Negative)+'%')
print( 'Negative Reply within 500 ms = ' + str(rtt_counter_within_500_Negative)+'%')
print( 'LISP Reply exceed 500 ms = ' + str(rtt_counter_500_LISP)+'%')
print( 'LISP Reply within 500 ms = ' + str(rtt_counter_within_500_LISP)+'%')


# Obtains the ECDF

ecdf_negative = ECDF(Negative_RTTs)
ecdf_lisp = ECDF(LISP_RTTs)
ecdf_overall = ECDF(overall_RTTs)


# Plot the Figure
# To automatically produce the size of the figure
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})

# you can use "linewidth" to modify the width of line
negative , =plt.plot(ecdf_negative.x , ecdf_negative.y  , 'r-' , label = 'Negative Map-Reply')
answered , =plt.plot(ecdf_lisp.x , ecdf_lisp.y , 'g--' , label = 'LISP Map-Reply')
overall ,  =plt.plot(ecdf_overall.x , ecdf_overall.y , 'b-.'  , label = 'overall')
plt.legend(handler_map={negative : HandlerLine2D(numpoints=1)})
plt.legend(handler_map={answered : HandlerLine2D(numpoints=1)})
plt.legend(handler_map={overall: HandlerLine2D(numpoints=1)})
plt.legend(handles=[negative , answered, overall], loc=4)
plt.axis([ 0 , 3000 , 0 , 1])
plt.grid(True)
plt.xlabel('RTT(ms)', fontsize=25)
plt.ylabel('ECDF', fontsize=25)
plt.xticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
plt.yticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
# To check if the Figures path exists, otherise we create one
try:
    os.stat(os.path.join(FIGURE_PATH))
except:
    os.makedirs(os.path.join(FIGURE_PATH))
plt.savefig(os.path.join(FIGURE_PATH, 'ecdf_of_RTT.eps'), dpi=300, transparent=True) # you can change the name, just an example
plt.show() # When you use the above command to save the figure, you can choose to don't show the figure anymore

sys.exit()