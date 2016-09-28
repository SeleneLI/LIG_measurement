import sys
import time
import re
import os
import  ipaddress
import csv
import glob
import numpy as np
from scipy.stats.stats import pearsonr
import math
import statistics
#import matplotlib.pyplot as plt
#from matplotlib.legend_handler import HandlerLine2D
from statsmodels.distributions.empirical_distribution import ECDF
import socket
from ipaddress import IPv4Address, IPv4Network
import datetime
import operator
import pandas as pd

#map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50'   ,'149.20.48.61' , '149.20.48.77',  '206.223.132.89', '202.214.86.252' , '202.51.247.10' ] # 3*EURO



#Num_MR = len(map_resolvers)


#MR_counter = 0
#while MR_counter < Num_MR:
#            file = open('Tables/' + map_resolvers[MR_counter] + '-stability.csv', 'r')
#            reader = csv.reader(file)
#            for row in reader:
#                if row[1] == 'Negative Reply' :
#                    if row[12] == '0' and row[13] == '0' :
#                        print( 'EID_Prefix : ' , row[0] , ' Map Resolver :  ' , map_resolvers[MR_counter])


#            MR_counter += 1





x = [[set()]]*8



print (x)


