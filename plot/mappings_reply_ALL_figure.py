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
from config.config import *



map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO


MR_counter = 1
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

   # To automatically produce the size of the figure
   mpl.rcParams['text.usetex'] = True
   #mpl.rcParams.update({'figure.autolayout': True})

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
   plt.ylabel('  mappings  ')
   plt.gcf().autofmt_xdate()

   # plt.xticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
   # plt.yticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")

   try:
       os.stat(os.path.join(FIGURE_PATH))
   except:
       os.makedirs(os.path.join(FIGURE_PATH))
   plt.savefig(os.path.join(FIGURE_PATH, 'Mapping_LISP_Negative_MR_#'+str(MR_counter)+'.eps'), dpi=300,transparent=True)  # you can change the name, just an example
   plt.show()  # When you use the above command to save the figure, you can choose to don't show the figure anymore

   MR_counter+=1
sys.exit()

