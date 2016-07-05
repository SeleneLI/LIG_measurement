from __future__ import unicode_literals
import ipaddress


def lister ( dst_EID , EID_Prefix , loc_num ,  Timestamp , map_resolver):

 # Wait until to get the pirmission to write in the file (Flag = 0 )
 while True :
   controller = open('controller.log', 'r+')
   flag = controller .readlines()
   if len(flag) != 0:
       if flag[1] == '1\n':
          controller.close()
          controller = open('controller.log', 'r+')
          flag = controller .readlines()
       else:
           break
   else:
       continue

 # Lock the file  ( Flag = 1)
 flag[1] = '1\n'
 controller = open('controller.log', 'w+')
 controller.writelines(flag)
 controller.close()

 # check if the destination EID belong to the EID_Prefix
 if ipaddress.ip_address(dst_EID) in ipaddress.ip_network(EID_Prefix) :

       file= open('EID_list_'+ str(Timestamp) +'.log' , 'r+')
       info = file.read().split()
       if EID_Prefix in info :
         index = info.index(EID_Prefix)
         while True:
            file = open('EID_list_' + str(Timestamp) + '.log', 'r+')
            info_2 = file.readlines()
            if len(info_2) != 0 and int(index/3) < len(info_2)  :
               info_2[int(index/3)] = info_2[int(index/3)].replace(']\n', ',' + loc_num + ']\n')
               break
            else:
               file.close()
               continue

         file = open('EID_list_' + str(Timestamp) + '.log', 'w+')
         file.writelines(info_2)
         file.close()



       else:
         file.write( EID_Prefix +  '   *   ' + '['+ loc_num + ']\n')
         file = open('EID_list_' + str(Timestamp) + '.log', 'r+')
         info_2 = file.readlines()
         file = open('EID_list_' + str(Timestamp) + '.log', 'w+')
         file.writelines(info_2)
         file.close()


 else:

       file = open('EID_list_' + str(Timestamp) + '.log', 'r+')
       info = file.read().split()
       if EID_Prefix in info:
         index = info.index(EID_Prefix)
         while True :
            file = open('EID_list_' + str(Timestamp) + '.log', 'r+')
            info_2 = file.readlines()
            if len(info_2) != 0 and int(index/3) < len(info_2):
              if info[index+1] != '*' :
                 info_2[int(index / 3)] = info_2[int(index / 3)].replace(']\n', ',' + loc_num + ']\n')
                 info_2[int(index / 3)] = info_2[int(index / 3)].replace(info[index+1] , info[index+1]+'|' + dst_EID)
                 break
              else:
                 info_2[int(index / 3)] = info_2[int(index / 3)].replace(']\n', ',' + loc_num + ']\n')
                 info_2[int(index / 3)] = info_2[int(index / 3)].replace(info[index + 1] , dst_EID)
                 break
            else:
              file.close()
              continue

         file = open('EID_list_' + str(Timestamp) + '.log', 'w+')
         file.writelines(info_2)
         file.close()



       else:
         file.write( EID_Prefix + '  '+  dst_EID + '  '+'['+ loc_num + ']\n')
         file = open('EID_list_' + str(Timestamp) + '.log', 'r+')
         info_2 = file.readlines()
         file = open('EID_list_' + str(Timestamp) + '.log', 'w+')
         file.writelines(info_2)
         file.close()

 # Unlock the file (Flag = 0)
 flag[1] = '0\n'
 controller = open('controller.log', 'w+')
 controller.writelines(flag)
 controller.close()






# if ipaddress.ip_address(dst_EID) in ipaddress.ip_network(EID_Prefix) :

#       file= open('EID_list_'+ str(Timestamp) +'.log' , 'r+')
#       info = file.read().split()
#       if EID_Prefix in info :
#         index = info.index(EID_Prefix)
#         file = open('EID_list_' + str(Timestamp) + '.log', 'r+')
#         info_2 = file.readlines()
#         info_2[int(index/3)] = info_2[int(index/3)].replace(']\n', ',' +loc_num  + ']\n')
#         file = open('EID_list_'+ str(Timestamp) +'.log' , 'w+')
#         file.writelines(info_2)
#         file.close()

#       else:
#         file.write( EID_Prefix +  '   *   ' + '['+ loc_num  + ']\n')
#         file.close()

# else:

  #     file = open('EID_list_' + str(Timestamp) + '.log', 'r+')
  #     fcntl.flock(file, fcntl.LOCK_EX)
  #     info = file.read().split()
  #     if EID_Prefix in info:
  #       index = info.index(EID_Prefix)
  #       file = open('EID_list_' + str(Timestamp) + '.log', 'r+')
  #       info_2 = file.readlines()
  #       if info[index+1] != '*' :
  #           info_2[int(index / 3)] = info_2[int(index / 3)].replace(']\n', ',' + loc_num  + ']\n')
  #           info_2[int(index / 3)] = info_2[int(index / 3)].replace(info[index+1] , ' , ' + dst_EID)
  #       else:
  #           info_2[int(index / 3)] = info_2[int(index / 3)].replace(']\n', ',' + loc_num  + ']\n')
  #           info_2[int(index / 3)] = info_2[int(index / 3)].replace(info[index + 1] , dst_EID)

   #      file = open('EID_list_' + str(Timestamp) + '.log', 'w+')
   #      file.writelines(info_2)
   #      file.close()

#       else:
#         file.write(EID_Prefix + '   *   ' + '[' + loc_num  + ']\n')
#         file.close()





#file = open('EID_list_' + str(Timestamp) + '.log', 'r')
#info = file.read().split()
#if EID_Prefix in info:
#    index = info.index(EID_Prefix)
#    file = open('EID_list_' + str(Timestamp) + '.log', 'r')
#    info_2 = file.readlines()
#    info_2[int(index / 2)] = info_2[int(index / 2)].replace(']\n', ',' + loc_num + ']\n')
#    # data = info_2[int(index/2)]
#    # data= data.strip(']\n')
#    # info_2[int(index/2)]=data + ',' + loc_num + ']\n'
#    file = open('EID_list_' + str(Timestamp) + '.log', 'w+')
#    file.writelines(info_2)
#    file.close()
#else:
#    file.write(EID_Prefix + '    ' + '[' + loc_num + ']\n')
#    file.close()



#if ipaddress.ip_address(dst_EID) in ipaddress.ip_network(EID_Prefix) :
#   while True :
#     try:
#       file= open('EID_list_'+ str(Timestamp) +'.log' , 'r+')
#       fcntl.flock(file, fcntl.LOCK_EX)
#       info = file.read().split()
#       if EID_Prefix in info :
#         index = info.index(EID_Prefix)
#         file = open('EID_list_' + str(Timestamp) + '.log', 'r+')
#         info_2 = file.readlines()
#         info_2[int(index/3)] = info_2[int(index/3)].replace(']\n', ',' + loc_num + ']\n')
#         file = open('EID_list_'+ str(Timestamp) +'.log' , 'w+')
#         file.writelines(info_2)
#         fcntl.flock(file, fcntl.LOCK_UN)
#         file.close()
#         break
#       else:
#         file.write( EID_Prefix +  '   *   ' + '['+ loc_num + ']\n')
#         fcntl.flock(file, fcntl.LOCK_UN)
#         file.close()
#         break
#     except:
#        continue
# else:
#   while True:
#     try:
#       file = open('EID_list_' + str(Timestamp) + '.log', 'r+')
#       fcntl.flock(file, fcntl.LOCK_EX)
#       info = file.read().split()
#       if EID_Prefix in info:
#         index = info.index(EID_Prefix)
#         file = open('EID_list_' + str(Timestamp) + '.log', 'r+')
#         info_2 = file.readlines()
#         if info[index+1] != '*' :
#             info_2[int(index / 3)] = info_2[int(index / 3)].replace(']\n', ',' + loc_num + ']\n')
#             info_2[int(index / 3)] = info_2[int(index / 3)].replace(info[index+1] , ' , ' + dst_EID)
#         else:
#             info_2[int(index / 3)] = info_2[int(index / 3)].replace(']\n', ',' + loc_num + ']\n')
#             info_2[int(index / 3)] = info_2[int(index / 3)].replace(info[index + 1] , dst_EID)

#         file = open('EID_list_' + str(Timestamp) + '.log', 'w+')
#         file.writelines(info_2)
#         fcntl.flock(file, fcntl.LOCK_UN)
#         file.close()
#         break
#       else:
#         file.write(EID_Prefix + '   *   ' + '[' + loc_num + ']\n')
#         fcntl.flock(file, fcntl.LOCK_UN)
#         file.close()
#         break
#     except:
#         continue
