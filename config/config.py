# -*- coding: utf-8 -*-
__author__ = 'yueli'
'''In this python script, we plan to define some globl variables'''


import os
from pylab import *
import matplotlib.pyplot as plt
import csv
import matplotlib as mpl
import urllib3  # the lib that handles the url stuff
import urllib.request



# Plot part

FIGURE_PATH = os.path.join('Figures')

fontLabel = {
    'fontname'   : 'Times New Roman',
    'color'      : 'k',
    'fontsize'   : 40
       }

fontTick = {
    'fontname'   : 'Times New Roman',
    'color'      : 'k',
    'fontsize'   : 30
       }

font3D = {
    'fontname'   : 'Times New Roman',
    'color'      : 'k',
    'fontsize'   : 52
       }