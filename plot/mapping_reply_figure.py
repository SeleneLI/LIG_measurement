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
from config.config import *


map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO


MR_counter = 1
for map_resolver in map_resolvers:
   TSPs = []
   mapping_list = []
   table = open('../Tables/'+map_resolver+'-Negative-LISP.csv', 'r')
   reader = csv.reader(table)
   for row in reader:
       del row[0]
       for TSP in row :
           TSPs.append(datetime.datetime.fromtimestamp(int(TSP)))
       break
   counter_TSP = 0
   while counter_TSP < len(TSPs):
       print(counter_TSP)
       counter_mapping = 0
       table = open('../Tables/' + map_resolver + '-Negative-LISP.csv', 'r')
       reader = csv.reader(table)
       for row in reader:
           if row[0] == '':
               continue
           del row[0]
           if row[counter_TSP] != '' :
               counter_mapping += 1
       counter_TSP +=1

       mapping_list.append(counter_mapping)


   # plot
   # To automatically produce the size of the figure
   mpl.rcParams['text.usetex'] = True
   mpl.rcParams.update({'figure.autolayout': True})

   dates = matplotlib.dates.date2num(TSPs)
   plt.plot_date(dates, mapping_list  , ls= '-' , marker='')
   plt.grid(True)
   plt.title(map_resolver)
   plt.xlabel('Time')
   plt.ylabel(' Number of mappings ')

   plt.gcf().autofmt_xdate()

   # plt.xticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
   # plt.yticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
   # To check if the Figures path exists, otherise we create one
   try:
       os.stat(os.path.join(FIGURE_PATH))
   except:
       os.makedirs(os.path.join(FIGURE_PATH))
   plt.savefig(os.path.join(FIGURE_PATH, 'Mapping_MR_#'+str(MR_counter)+'.eps'), dpi=300,transparent=True)  # you can change the name, just an example
   plt.show()  # When you use the above command to save the figure, you can choose to don't show the figure anymore
   MR_counter += 1


sys.exit()