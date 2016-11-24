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


Negative_RTTs_list = []
LISP_RTTs_list = []
overall_RTTs_list = []

for map_resolver in map_resolvers:
   Negative_RTTs = []
   LISP_RTTs = []
   overall_RTTs = []
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



   Negative_RTTs_list.append(Negative_RTTs)
   LISP_RTTs_list.append(LISP_RTTs)
   overall_RTTs_list.append(overall_RTTs)






# Obtains the ECDF

ecdf_negative = []
ecdf_lisp = []
ecdf_overall =[]
for MR in Negative_RTTs_list :
   ecdf_negative.append(ECDF(MR))

for MR in LISP_RTTs_list :
   ecdf_lisp.append(ECDF(MR))

for MR in overall_RTTs_list :
   ecdf_overall.append(ECDF(MR))


# Plot the Figure

# To automatically produce the size of the figure
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})

for x in range(0 , len(map_resolvers)):
    negative , = plt.plot(ecdf_negative[x].x , ecdf_negative[x].y  , label = 'Negative Map-Reply' )
    answered , =  plt.plot(ecdf_lisp[x].x , ecdf_lisp[x].y  , label = 'LISP Map-Reply')
    overall ,  =  plt.plot(ecdf_overall[x].x , ecdf_overall[x].y   , label = 'overall')

    # To automatically produce the size of the figure
    mpl.rcParams['text.usetex'] = True
    mpl.rcParams.update({'figure.autolayout': True})

    plt.legend(handler_map={negative : HandlerLine2D(numpoints=1)})
    plt.legend(handler_map={answered : HandlerLine2D(numpoints=1)})
    plt.legend(handler_map={overall: HandlerLine2D(numpoints=1)})
    plt.legend(handles=[negative , answered, overall], loc=4)
   # plt.title(map_resolvers[x])
    plt.axis([ 0 , 3000 , 0 , 1])
    plt.grid(True)
    plt.xlabel('RTT(ms)' , fontsize=25)
    plt.ylabel('ECDF' , fontsize=25)
    plt.xticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
    plt.yticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
    # To check if the Figures path exists, otherise we create one
    try:
        os.stat(os.path.join(FIGURE_PATH))
    except:
        os.makedirs(os.path.join(FIGURE_PATH))
    plt.savefig(os.path.join(FIGURE_PATH, 'ecdf_of_RTT_MR_'+str(x+1)+'.eps'), dpi=300,
                transparent=True)  # you can change the name, just an example
    plt.show()  # When you use the above command to save the figure, you can choose to don't show the figure anymore

sys.exit()