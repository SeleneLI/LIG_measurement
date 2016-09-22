
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

map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50'   ,'149.20.48.61' , '149.20.48.77',  '206.223.132.89', '202.214.86.252' , '202.51.247.10' ] # 3*EURO
#map_resolvers  = ['217.8.97.6',  '206.223.132.89', '202.214.86.252'  ]
#'149.20.48.61' , '149.20.48.77', '202.51.247.10'
TSPs = []
mapping_list = []
table = open('Tables/' + map_resolvers[0] + '-LISP.csv', 'r')
reader = csv.reader(table)
for row in reader:
    del row[0]
    for TSP in row:
        TSPs.append(datetime.datetime.fromtimestamp(int(TSP)))
    break

Num_MR = len(map_resolvers)

Day = 1




EIDs_MRs_list = []
RLOCs_MRs_list = []
MR_counter = 0
while MR_counter < Num_MR:
        TSP_counter = len(TSPs) - (12 * Day)
        EIDs_MR = []
        while TSP_counter < len(TSPs):
            file = open('Tables/' + map_resolvers[MR_counter] + '-LISP.csv', 'r')
            reader = csv.reader(file)
            for row in reader:
                if row[0] == '':
                    continue
                if row[TSP_counter] != '':
                   if row[0] not in EIDs_MR :
                       EIDs_MR.append(row[0])
            TSP_counter += 1
        MR_counter += 1

        EIDs_MRs_list.append(EIDs_MR)


intersect = set(EIDs_MRs_list[0]).intersection(EIDs_MRs_list[1])
i = 2
while i < len(EIDs_MRs_list) :
        intersect = set(intersect).intersection(EIDs_MRs_list[i])
        i += 1

union = set(EIDs_MRs_list[0]).union(EIDs_MRs_list[1])
i = 2
while i < len(EIDs_MRs_list) :
        union = set(union).union(EIDs_MRs_list[i])
        i += 1
#Avg_correlation_table = [[1]*8]*8
#Avg_correlation_table = Avg_correlation_table /2
#x = [ '1' , '2','3']
#y = [ '1' , '2']
#z = set(x).intersection(y)
#z = list(z)
#index = z.index('1')
#x = 3.456789
#y = round (x , 2)
#z = math.ceil(x*1000)/1000



#x = [ 2 , 2 , 3]
#y = [2 , 1 , 3 ]
#i = set(x).intersection(y)
#z =  np.corrcoef( x , y )[0 , 1]
#y =  np.array(y)
#indexes = np.where( y == 0)[0]
#c = y.index(0)
#c = [ x ,  y ]
#e = max(c)
#z = np.corrcoef( x , y )[0 , 1]
#x = '0.0./3'
#z = x.split('/')

#x = [ int(ipaddress.IPv4Address('0.0.0.0')) , int(ipaddress.IPv4Address('1.1.1.1')) ,int(ipaddress.IPv4Address('3.3.3.3')) ]
#y= [ int(ipaddress.IPv4Address('0.0.0.0')) , int(ipaddress.IPv4Address('1.1.1.1')) ,int(ipaddress.IPv4Address('3.3.3.3')) ]
#s = int('1.1.1.13')
#z = np.correlate(x , y  , mode= 'valid')
#c = np.corrcoef( x , y )[0 , 1]

#z = frist[0]/second[0]

#for x, y in zip(frist, second) :
#     z = x +y


#Z = np.array([1,1,1,2,2,4,5,6,6,6,7,8,8])
#X, F = np.unique(Z, return_counts=True)
#F=F/Z.size

#i = 0
#CDF =[F[0]]
#while i < len(X)-1:
#    CDF.append(CDF[i]+F[i+1])
#    i +=1

#x = datetime.datetime.fromtimestamp(int("1284101485")).strftime('%m%d')
#y = int(datetime.datetime.fromtimestamp(int("1284101485")).strftime('%m%d'))

#print( datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S'))




#x= re.split( r"[/]" , '85.184.3.0/27')[0]
#if ipaddress.ip_network('37.77.128.0/17').overlaps(IPv4Network('37.77.32.0/20')) :
#   print('yes')

#print(list(ipaddress.ip_network('85.184.3.0/27').hosts()))
#print(list(ipaddress.ip_network('85.184.3.0/26').hosts()))

#EID = [ [IPv4Network('37.77.56.64/26') , '0' , '0'] , [IPv4Network('205.203.201.0/24'), '1' , '0'] , [IPv4Network('153.0.0.0/31' ), '2' , '1']]
#EID_2 = str(sorted(EID))

#map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10']
#counter  = 0

#for map_resolver in map_resolvers:
#        file_names = glob.glob('data/' + str(map_resolver)  + '/*.log')
#        for file_name in file_names:
#            file = open(file_name , 'r')
#            data = file.readlines()
#            if 'LOCATOR_COUNT' in data[8]:
#               if (re.split(r"[=]", data[12])[1]).strip('\n') != 'False' :
#                  counter +=1


#file = open('Mobility.log' , 'w')
#file.writelines(str(counter))
#file.close()


#m = '00000'
#r = '00000'
#if m != r :
#    x = 0

#file = open( 'summary/EID.log' , 'w+')

#file.writelines('0.0.0.0/3   [000000]  *\n')
#file.writelines('0.0.0.0/3   [000000]  *\n\n\n')
#file.writelines('0.0.0.0/3   [000000]  *\n')
#file.writelines('0.0.0.0/3   [000000]  *\n')
#file.writelines('0.0.0.0/3   [000000]  *\n')
#file.close()

#file = open( 'summary/EID.log' , 'r+')
#data = file.read()
#data2 = data.split()
#i = 0
#while i < len(data2):
#    if '/' in data2[i]:
#        i = i+3
#    else:
#        i +=1






#file = open ( 'Timestamp_list.log' , 'w')
#file.writelines('1471125601\n' )
#file.writelines('1471168801\n' )
#file.writelines('1471212001\n' )
#file.writelines('1471255201\n' )
#file.writelines('1471276801\n' )

#file.close()


#try:
#    socket.inet_aton('153.16.192.0')
    # legal
#except socket.error:
#    print('not valid')

#grades = [93.5, 93, 60.8, 94.5, 82, 87.5, 91.5, 99.5, 86, 93.5, 92.5, 78, 76, 69, 94.5,
       #   89.5, 92.8, 78, 65.5, 98, 98.5, 92.3, 95.5, 76, 91, 95, 61]

#cdf = ECDF(grades)
#x = cdf.x
#y = cdf.y


#plt.plot(x, y,'ro')
#line1, = plt.plot([1 ,2 , 3], [1 ,2 , 3], 'ro', label='negative')
#line2, = plt.plot([4 ,3.5 , 2], [4 ,3.5 , 2], 'bx', label='LISP')
#plt.legend(handler_map={line1: HandlerLine2D(numpoints=1)})
#plt.legend(handler_map={line2: HandlerLine2D(numpoints=1)})
#plt.legend(handles=[line2 , line1], loc=11)
#plt.axis([0, 5, 0, 5])
#plt.grid(True)
#plt.show()



#x = [ 1 , 2, 3 ,6, 4 , 5 , 6]
#y = ['1' , '2' , '3' , '4' , '5' , '6']
#z = statistics.median(x)
#c = statistics.median(y)

#z=[]
#f = open('test.csv', 'r')
#reader = csv.reader(f)
#for row in reader:
#    z = []
#    del row[0]
#    for x in row :
#        if x != '':
#          z.append(float(x))
#    y= statistics.median(z)

#f.close()
#a = ['a' , 'b']
#e = [''] +a
#c = [e]
#b = [['1' , '2'] , ['3' , '4']]
#z= c + b

#file = open('xyz.log', 'a+')
#x= file.read()
#file.write('123')
#file.close()
#x = [''] * 2

#x = glob.glob('data/*.csv')
#y = [['EID' , '12' , 23] , ['EID1' , '11' ]]

#with open('test.csv', 'w', newline='') as fp:
#    a = csv.writer(fp, delimiter=',')
#    data = [['Me', 'You'],
#            ['293', '219'],
#            ['54', '13']]
#    a.writerows(data)
#row = [8]
#for x in row :
#    x = str(x)

#y = 'locator=123ms'
#z = y.replace('ms' , '')
#data = re.split(r"[=\m]" , y )


#x = 'summary/EID_list_12345.log'
#data = re.split(r"[\:\|\{\}]" , info[index+2])
#data = re.split(r"[\_\.]" , x)
#z =[]
#for y in x :
#  y = ''.join(re.split('/' , y)[1])
#  z.append(y)
#network = ipaddress.ip_network(str('0.0.0.1/32'))
#addrs_num = network.num_addresses

#x= list(ipaddress.ip_network('153.16.55.0/24'))

#print( x)

#x = ['0.0.0.0/32' , '0.0.0.0/10' ]
#y = ''.join((re.split('/' , x[0]))[0])

#x = ''.join(y[0])

#st = '1222'
#cont = st.count('|')

#os.remove('controller.log')

#file = open('summary/EID_list_current.log' , 'w+')
#file.write('0.0.0.0/3  [n,n,n,n,n,n,n]   {1.1.1.1/3[0,0,0,0,0,0]}\n')
#file.write('0.1.0.0/3  [n,n,n,n,n,n,n]   {1.1.1.1/3[0,0,0,0,0,0]}\n')
#file.write('0.0.1.0/3  [0,n,n,n,n,n,n]   {1.1.1.1/3[0,0,0,0,0,0]}\n')
#file.write('0.0.0.1/3  [n,n,n,n,n,n,n]   {1.1.1.1/3[0,0,0,0,0,0]}\n')
#file.write('2.0.0.0/3  [n,n,n,n,n,n,n]   {1.1.1.1/3[0,0,0,0,0,0]}\n')
#file.write('0.2.0.0/3  [n,n,n,n,n,n,n]   {1.1.1.1/3[0,0,0,0,0,0]}\n')
#file.close()
#file = open('data/text2.log' , 'w+')
#file.close()

#FILE_PATH = 'data_2/text.log'

#try:
 #   os.stat(os.path.join(FILE_PATH))
#except:
 #   os.makedirs(os.path.join(FILE_PATH))

#print(list(ipaddress.ip_network('153.16.96.0/19')))


#save_path = '/data'
#os.path.join(os.path.expanduser('~'),'data',completeName)
#completeName = os.path.join(save_path, 'controller.log')
#controller = open('data/controller.log' , 'w+')
#controller.close()
#flag = controller.read().split()
#x= list(flag[0])
#x = '[1,1,11,1]'
#x = list(x)
#x = [ '1' , '2' ,  '3' ,  '4' ]
#y = []
#y.append(x[0:2])
#z = ''.join(y[0])

#x='{0.0.0.0/3:[1,2,2,3,4,4]|1.1.1.1/3:[1,2,2,3,4,4]}'
#if '1.1.1.1/3' in x:
#    print('yes')
#counter = x.count('|')
#y= re.split(r"[\:\|\{\}]" , x)
#z=y[1:1+2]
#i = 0
#if i < counter :

#c = '[-12344]'
#c=list(c)

#z = '{'.join(y)
#z = z.join('}')

#print(x)
#y= x.split()





#t1 = Thread(target=scan, args=('Thread1', '0.0.0.0', '153.16.6.255', Timestamp))
#t2 = Thread(target=scan, args=('Thread2', '153.16.7.0', '153.16.17.255', Timestamp))
#t3 = Thread(target=scan, args=('Thread3', '153.16.18.0', '153.16.25.255', Timestamp))
#t4 = Thread(target=scan, args=('Thread4', '153.16.26.0', '153.16.39.255', Timestamp))
#t5 = Thread(target=scan, args=('Thread5', '153.16.40.0', '153.16.54.255', Timestamp))
#t6 = Thread(target=scan, args=('Thread6', '153.16.55.0', '153.16.120.255', Timestamp))
#t7 = Thread(target=scan, args=('Thread7', '153.16.121.0', '153.16.144.255', Timestamp))
#t8 = Thread(target=scan, args=('Thread8', '153.16.145.0', '153.16.150.255', Timestamp))
#t9 = Thread(target=scan, args=('Thread9', '153.16.151.0', '153.16.155.255', Timestamp))
#t10 = Thread(target=scan, args=('Thread10', '153.16.156.0', '153.16.202.225', Timestamp))
#t11 = Thread(target=scan, args=('Thread11', '153.16.203.0', '255.255.255.255', Timestamp))







sys.exit()

