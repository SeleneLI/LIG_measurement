from __future__ import unicode_literals
import ipaddress
import re
import sys


def lister ( dst_EID , EID_Prefix , loc_num ,  Timestamp , resolver_num):

 # Wait until to get the pirmission to write in the file (Flag = 0 )
 try:
   while True :

     controller = open('controller.log', 'r+')
     flag = controller .readlines()
     if len(flag) != 0:
        if flag[1] == '1\n':
           controller.close()
           #controller = open('controller.log', 'r+')
           #flag = controller .readlines()
        else:
            break
     else:
        continue


  # Lock the file  ( Flag = 1)
   flag[1] = '1\n'
   controller = open('controller.log', 'w+')
   controller.writelines(flag)
   controller.close()

 except:

     sys.exit()

 # check if the destination EID belong to the EID_Prefix
 if ipaddress.ip_address(dst_EID) in ipaddress.ip_network(EID_Prefix) :

       file= open('summary/EID_list_'+ str(Timestamp) +'.log' , 'r+')
       info = file.read().split()
       if EID_Prefix in info :
         index = info.index(EID_Prefix)
         while True:
            file = open('summary/EID_list_' + str(Timestamp) + '.log', 'r+')
            info_2 = file.readlines()
            if len(info_2) != 0 and int(index/3) < len(info_2)  :
               data_old_string=info[index+1] # [0,0,0,0...]
               data_old = list(data_old_string)  # [ '[' , '0' , '-1' ,  ...]
               if resolver_num == 1 :
                   data_old[1] = str(loc_num)   # insert the new value
               elif resolver_num == 2:
                   data_old[3] = str(loc_num)  # insert the new value
               elif resolver_num == 3:
                   data_old[5] = str(loc_num)  # insert the new value
               elif resolver_num == 4:
                   data_old[7] = str(loc_num)  # insert the new value
               elif resolver_num == 5:
                   data_old[9] = str(loc_num)  # insert the new value
               elif resolver_num == 6:
                   data_old[11] = str(loc_num)  # insert the new value
               elif resolver_num == 7:
                   data_old[13] = str(loc_num)  # insert the new value
               elif resolver_num == 8:
                   data_old[15] = str(loc_num)  # insert the new value
               elif resolver_num == 9:
                   data_old[17] = str(loc_num)  # insert the new value
               elif resolver_num == 10:
                   data_old[19] = str(loc_num)  # insert the new value
               elif resolver_num == 11:
                   data_old[21] = str(loc_num)  # insert the new value
               elif resolver_num == 12:
                   data_old[23] = str(loc_num)  # insert the new value
               elif resolver_num == 13:
                   data_old[25] = str(loc_num)  # insert the new value
               elif resolver_num == 14:
                   data_old[27] = str(loc_num)  # insert the new value
               data_new=''.join(data_old) #convert the list to string '[0,-1,-1...]'
               info_2[int(index / 3)] = info_2[int(index / 3)].replace(data_old_string, data_new) # update the line
               break
            else:
               file.close()
               continue

         file = open('summary/EID_list_' + str(Timestamp) + '.log', 'w+')
         file.writelines(info_2)
         file.close()



       else:
         if resolver_num == 1:
             file.write( EID_Prefix + '  ' + '['+loc_num+',n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  *\n') #\n
         elif resolver_num == 2:
             file.write( EID_Prefix + '  ' + '[n,'+loc_num+',n,n,n,n,n,n,n,n,n,n,n,n]' + '  *\n')
         elif resolver_num == 3:
             file.write( EID_Prefix + '  ' + '[n,n,'+loc_num+',n,n,n,n,n,n,n,n,n,n,n]' + '  *\n')
         elif resolver_num == 4:
             file.write( EID_Prefix + '  ' + '[n,n,n,'+loc_num+',n,n,n,n,n,n,n,n,n,n]' + '  *\n')
         elif resolver_num == 5:
             file.write( EID_Prefix + '  ' + '[n,n,n,n,'+loc_num+',n,n,n,n,n,n,n,n,n]' + '  *\n')
         elif resolver_num == 6:
             file.write( EID_Prefix + '  ' + '[n,n,n,n,n,'+loc_num+',n,n,n,n,n,n,n,n]' + '  *\n')
         elif resolver_num == 7:
             file.write( EID_Prefix + '  ' + '[n,n,n,n,n,n,'+loc_num+',n,n,n,n,n,n,n]' + '  *\n')
         elif resolver_num == 8:
             file.write( EID_Prefix + '  ' + '[n,n,n,n,n,n,n,'+loc_num+',n,n,n,n,n,n]' + '  *\n')
         elif resolver_num == 9:
             file.write( EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,'+loc_num+',n,n,n,n,n]' + '  *\n')
         elif resolver_num == 10:
             file.write( EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,'+loc_num+',n,n,n,n]' + '  *\n')
         elif resolver_num == 11:
             file.write( EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,'+loc_num+',n,n,n]' + '  *\n')
         elif resolver_num == 12:
             file.write( EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,'+loc_num+',n,n]' + '  *\n')
         elif resolver_num == 13:
             file.write( EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,'+loc_num+',n]' + '  *\n')
         elif resolver_num == 14:
             file.write(EID_Prefix  + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,'+loc_num+']' + '  *\n')


         file.close()


 else:

       file = open('summary/EID_list_' + str(Timestamp) + '.log', 'r+')
       info = file.read().split()
       if EID_Prefix in info:
         index = info.index(EID_Prefix)
         while True :
            file = open('summary/EID_list_' + str(Timestamp) + '.log', 'r+')
            info_2 = file.readlines()
            if len(info_2) != 0 and int(index/3) < len(info_2):
              if info[index+2] != '*' : # check if it's empty
                 if dst_EID in info[index+2]:
                    dst_EID_num = info[index+2].count('|')
                    data = re.split(r"[\:\|\{\}]" , info[index+2]) # separete {dst_EID:[0,0,0,0]|dst_EID:[0,0,0,0]}
                    position = data.index(dst_EID)  # get the position of the dst_EID
                    reply_string = data[position+1]  # get the replies [0,0,0,..,0]
                    reply_list = list(reply_string)
                    if resolver_num == 1 :
                        reply_list[1] = str(loc_num) # insert the new value
                    elif resolver_num == 2 :
                        reply_list[3] = str(loc_num) # insert the new value
                    elif resolver_num == 3 :
                        reply_list[5] = str(loc_num) # insert the new value
                    elif resolver_num == 4 :
                        reply_list[7] = str(loc_num) # insert the new value
                    elif resolver_num == 5 :
                        reply_list[9] = str(loc_num) # insert the new value
                    elif resolver_num == 6 :
                        reply_list[11] = str(loc_num) # insert the new value
                    elif resolver_num == 7 :
                        reply_list[13] = str(loc_num) # insert the new value
                    elif resolver_num == 8 :
                        reply_list[15] = str(loc_num) # insert the new value
                    elif resolver_num == 9:
                        reply_list[17] = str(loc_num)  # insert the new value
                    elif resolver_num == 10:
                        reply_list[19] = str(loc_num)  # insert the new value
                    elif resolver_num == 11:
                        reply_list[21] = str(loc_num)  # insert the new value
                    elif resolver_num == 12:
                        reply_list[23] = str(loc_num)  # insert the new value
                    elif resolver_num == 13:
                        reply_list[25] = str(loc_num)  # insert the new value
                    elif resolver_num == 14:
                        reply_list[27] = str(loc_num)  # insert the new value
                    data_new = ''.join(reply_list)
                    data[position+1] = data_new
                    data_final_list = []
                    data_final_list.append('{')
                    i = 0  #changet from 1
                    n = 1  #changed from 0
                    data_final_list.append(data[n:n + 2]) # added
                    while i < dst_EID_num :  # rewrite the information
                        n = n + 2
                        data_final_list.append('|')
                        data_final_list.append(data[n:n + 2])
                        i = i+1
                    data_final_list.append('}')
                    data_final_string = ''.join(data_final_list[0])
                    info_2[int(index / 3)] = info_2[int(index / 3)].replace(info[index+2], data_final_string) # update the line

                    file = open('summary/EID_list_' + str(Timestamp) + '.log', 'w+')
                    file.writelines(info_2)
                    file.close()
                    break
                 else:
                    if resolver_num == 1 :
                       data_new =  '|' + dst_EID + ':[' + loc_num +',n,n,n,n,n,n,n,n,n,n,n,n,n]' + '}\n' #\n
                    elif resolver_num == 2 :
                       data_new =  '|' + dst_EID + ':[' + 'n,'+loc_num+',n,n,n,n,n,n,n,n,n,n,n,n]' + '}\n'
                    elif resolver_num == 3 :
                       data_new =  '|' + dst_EID + ':[' + 'n,n,'+loc_num+',n,n,n,n,n,n,n,n,n,n,n]' + '}\n'
                    elif resolver_num == 4 :
                       data_new =  '|' + dst_EID + ':[' + 'n,n,n,'+loc_num+',n,n,n,n,n,n,n,n,n,n]' + '}\n'
                    elif resolver_num == 5 :
                       data_new =  '|' + dst_EID + ':[' + 'n,n,n,n,'+loc_num+',n,n,n,n,n,n,n,n,n]' + '}\n'
                    elif resolver_num == 6 :
                       data_new =  '|' + dst_EID + ':[' + 'n,n,n,n,n,'+loc_num+',n,n,n,n,n,n,n,n]' + '}\n'
                    elif resolver_num == 7 :
                       data_new =  '|' + dst_EID + ':[' + 'n,n,n,n,n,n,'+loc_num+',n,n,n,n,n,n,n]' + '}\n'
                    elif resolver_num == 8 :
                       data_new =  '|' + dst_EID + ':[' + 'n,n,n,n,n,n,n,'+loc_num+',n,n,n,n,n,n]' + '}\n'
                    elif resolver_num == 9:
                       data_new =  '|' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,'+loc_num+',n,n,n,n,n]' + '}\n'
                    elif resolver_num == 10:
                       data_new =  '|' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,'+loc_num+',n,n,n,n]' + '}\n'
                    elif resolver_num == 11:
                       data_new =  '|' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,'+loc_num+',n,n,n]' + '}\n'
                    elif resolver_num == 12:
                       data_new =  '|' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,n,'+loc_num+',n,n]' + '}\n'
                    elif resolver_num == 13:
                       data_new =  '|' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,n,n,'+loc_num+',n]' + '}\n'
                    elif resolver_num == 14:
                       data_new =  '|' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,n,n,n,'+loc_num+']' + '}\n'

                    info_2[int(index / 3)] = info_2[int(index / 3)].replace('}\n', data_new)

                    file = open('summary/EID_list_' + str(Timestamp) + '.log', 'w+')
                    file.writelines(info_2)
                    file.close()
                    break
              else:

                 if resolver_num == 1 :
                    data_new = '{' + dst_EID + ':[' + loc_num+',n,n,n,n,n,n,n,n,n,n,n,n,n]' + '}' #\n
                 elif resolver_num == 2 :
                    data_new = '{' + dst_EID + ':[' + 'n,'+loc_num+',n,n,n,n,n,n,n,n,n,n,n,n]' + '}'
                 elif resolver_num == 3 :
                    data_new = '{' + dst_EID + ':[' + 'n,n,'+loc_num+',n,n,n,n,n,n,n,n,n,n,n]' + '}'
                 elif resolver_num == 4 :
                    data_new = '{' + dst_EID + ':[' + 'n,n,n,'+loc_num+',n,n,n,n,n,n,n,n,n,n]' + '}'
                 elif resolver_num == 5 :
                    data_new = '{' + dst_EID + ':[' + 'n,n,n,n,'+loc_num+',n,n,n,n,n,n,n,n,n]' + '}'
                 elif resolver_num == 6 :
                    data_new = '{' + dst_EID + ':[' + 'n,n,n,n,n,'+loc_num+',n,n,n,n,n,n,n,n]' + '}'
                 elif resolver_num == 7 :
                    data_new = '{' + dst_EID + ':[' + 'n,n,n,n,n,n,'+loc_num+',n,n,n,n,n,n,n]' + '}'
                 elif resolver_num == 8 :
                    data_new = '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,'+loc_num+',n,n,n,n,n,n]' + '}'
                 elif resolver_num == 9:
                    data_new = '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,'+loc_num+',n,n,n,n,n]' + '}'
                 elif resolver_num == 10:
                    data_new = '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,'+loc_num+',n,n,n,n]' + '}'
                 elif resolver_num == 11:
                    data_new = '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,'+loc_num+',n,n,n]' + '}'
                 elif resolver_num == 12:
                    data_new = '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,n,'+loc_num+',n,n]' + '}'
                 elif resolver_num == 13:
                    data_new = '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,n,n,'+loc_num+',n]' + '}'
                 elif resolver_num == 14:
                    data_new = '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,n,n,n,'+loc_num+']' + '}'

                 info_2[int(index / 3)] = info_2[int(index / 3)].replace(info[index+2], data_new)

                 file = open('summary/EID_list_' + str(Timestamp) + '.log', 'w+')
                 file.writelines(info_2)
                 file.close()
                 break
            else:
              file.close()
              continue

         #file = open('summary/EID_list_' + str(Timestamp) + '.log', 'w+')
         #file.writelines(info_2)
         #file.close()

       else:
         if resolver_num == 1 :
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + loc_num +',n,n,n,n,n,n,n,n,n,n,n,n,n]' + '}\n' )
         elif resolver_num == 2 :
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,'+loc_num+',n,n,n,n,n,n,n,n,n,n,n,n]' + '}\n' )
         elif resolver_num == 3 :
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,'+loc_num+',n,n,n,n,n,n,n,n,n,n,n]' + '}\n' )
         elif resolver_num == 4 :
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,n,'+loc_num+',n,n,n,n,n,n,n,n,n,n]' + '}\n' )
         elif resolver_num == 5 :
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,n,n,'+loc_num+',n,n,n,n,n,n,n,n,n]' + '}\n' )
         elif resolver_num == 6 :
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,n,n,n,'+loc_num+',n,n,n,n,n,n,n,n]' + '}\n' )
         elif resolver_num == 7 :
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,n,n,n,n,'+loc_num+',n,n,n,n,n,n,n]' + '}\n' )
         elif resolver_num == 8 :
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,'+loc_num+',n,n,n,n,n,n]' + '}\n' )
         elif resolver_num == 9:
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,'+loc_num+',n,n,n,n,n]' + '}\n')
         elif resolver_num == 10:
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,'+loc_num+',n,n,n,n]' + '}\n')
         elif resolver_num == 11:
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,'+loc_num+',n,n,n]' + '}\n')
         elif resolver_num == 12:
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,n,'+loc_num+',n,n]' + '}\n')
         elif resolver_num == 13:
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,n,n,'+loc_num+',n]' + '}\n')
         elif resolver_num == 14:
            file.write(EID_Prefix + '  ' + '[n,n,n,n,n,n,n,n,n,n,n,n,n,n]' + '  ' + '{' + dst_EID + ':[' + 'n,n,n,n,n,n,n,n,n,n,n,n,n,'+loc_num+']' + '}\n')

         file.close()

 # Unlock the file (Flag = 0)
 try:
   flag[1] = '0\n'
   controller = open('controller.log', 'w+')
   controller.writelines(flag)
   controller.close()
 except:
     sys.exit()


