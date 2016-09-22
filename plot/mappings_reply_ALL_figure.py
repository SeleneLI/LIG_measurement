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
import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerLine2D




map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO



for map_resolver in map_resolvers:
   TSPs = []
   mapping_list_Negative = []
   mapping_list_LISP = []
   table = open('../Tables/'+map_resolver+'-Negative.csv', 'r')
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
       table = open('../Tables/' + map_resolver + '-Negative.csv', 'r')
       reader = csv.reader(table)
       for row in reader:
           if row[0] == '':
               continue
           del row[0]
           if row[counter_TSP] != '' :
               counter_mapping += 1
       counter_TSP +=1

       mapping_list_Negative.append(counter_mapping)

   counter_TSP = 0
   while counter_TSP < len(TSPs):
       print(counter_TSP)
       counter_mapping = 0
       table = open('../Tables/' + map_resolver + '-LISP.csv', 'r')
       reader = csv.reader(table)
       for row in reader:
           if row[0] == '':
               continue
           del row[0]
           if row[counter_TSP] != '':
               counter_mapping += 1
       counter_TSP += 1

       mapping_list_LISP.append(counter_mapping)


   mapping_ALL = []
   mapping_ALL_Pr = []
   mapping_list_Negative_Pr = []
   mapping_list_LISP_Pr = []
   for x, y in zip(mapping_list_Negative, mapping_list_LISP):
       mapping_ALL.append(x + y)
       if x+y != 0 :
           mapping_list_Negative_Pr.append((x/(x+y))*100)
           mapping_list_LISP_Pr.append((y/(x+y))*100)
           mapping_ALL_Pr.append(((x/(x+y))+(y/(x+y)))*100)
       else:
           mapping_list_Negative_Pr.append(0)
           mapping_list_LISP_Pr.append(0)
           mapping_ALL_Pr.append(0)




   # plot
   dates = matplotlib.dates.date2num(TSPs)
   plt.plot_date([] , [] , color='b', label='LISP Reply', linewidth=5  , linestyle='-')
   plt.plot_date([], [], color='g', label='Negative Reply', linewidth=5 , linestyle='-' )
   plt.stackplot(dates , mapping_list_LISP_Pr , mapping_list_Negative_Pr )
   plt.axis([min(dates) , max(dates) , min(mapping_ALL_Pr) , max(mapping_ALL_Pr)])
   LISP_patch = mpatches.Patch(color='b', label='LISP Reply')
   Negative_patch = mpatches.Patch(color='g', label='Negative Reply')
   plt.legend(handles=[LISP_patch , Negative_patch] , bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.8)
   plt.title(map_resolver)
   plt.xlabel('Time')
   plt.ylabel('  mappings % ')


   plt.gcf().autofmt_xdate()

   plt.show()

sys.exit()

