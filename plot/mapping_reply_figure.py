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



map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO



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
   dates = matplotlib.dates.date2num(TSPs)
   plt.plot_date(dates, mapping_list  , ls= '-' , marker='')
   plt.grid(True)
   plt.title(map_resolver)
   plt.xlabel('Time')
   plt.ylabel(' # mappings ')

   plt.gcf().autofmt_xdate()

   plt.show()

sys.exit()