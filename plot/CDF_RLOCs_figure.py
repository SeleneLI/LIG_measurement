import sys
import time
import re
import os
import csv
import glob
import numpy as np
import statistics
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from statsmodels.distributions.empirical_distribution import ECDF
from config.config import *


map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO
RLOCs_num = []

for map_resolver in map_resolvers:
   table = open('../Tables/'+map_resolver+'-stability.csv', 'r')
   reader = csv.reader(table)
   for row in reader:
        if row[0] == 'EID Prefix' :
            continue
        if row[1] == 'LISP Reply':
            RLOCs_count = row[3].count(',')+1
            RLOCs_num.append(RLOCs_count)

RLOCs_num = np.array(RLOCs_num)
RLOCs , num = np.unique(RLOCs_num, return_counts=True)
PDF = num / RLOCs_num.size

i = 0
CDF =[ PDF[0]]
while i < len(RLOCs)-1:
    CDF.append(CDF[i]+PDF[i+1])
    i += 1

CDF = np.insert(CDF , 0 , 0)
RLOCs = np.insert(RLOCs , 0 , 0)



# Plot the Figure

# To automatically produce the size of the figure
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})

plt.plot(RLOCs , CDF , 'b-')
plt.xticks(RLOCs)
plt.grid(True)
plt.xlabel('number of RLOCs')
plt.ylabel('cdf')
plt.xticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
plt.yticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")

# To check if the Figures path exists, otherise we create one
try:
    os.stat(os.path.join(FIGURE_PATH))
except:
    os.makedirs(os.path.join(FIGURE_PATH))
plt.savefig(os.path.join(FIGURE_PATH, 'CDF_of_RLOCs.eps'), dpi=300, transparent=True) # you can change the name, just an example
plt.show() # When you use the above command to save the figure, you can choose to don't show the figure anymore



sys.exit()