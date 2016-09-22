
import sys
import time
import re
import os
import  ipaddress
import csv
import glob





with open('test.csv', 'w') as fp:
    a = csv.writer(fp)
    data = ['Me', 'You']
    a.writerow(data)


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

