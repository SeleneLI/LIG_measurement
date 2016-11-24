import sys
import csv
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from config.config import *



map_resolvers  = ['217.8.97.6' , '217.8.98.42' , '193.162.145.50' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO
#'149.20.48.61' , '149.20.48.77'
start_date = '20160904'
end_date   = '20161004'

# Obtaining the Timestamps
TSPs = []

table = open('../Tables/' + map_resolvers[0] + '-Negative.csv', 'r')
reader = csv.reader(table)
for row in reader:
    del row[0]
    for TSP in row:
        Date = datetime.datetime.fromtimestamp(int(TSP))
        Date.timestamp()
        Date_str = str(Date.year)+str('%02d'%Date.month)+str('%02d'%Date.day)
        if int(start_date) <= int(Date_str) <= int(end_date) :
            TSPs.append(TSP)  #datetime.datetime.fromtimestamp(int(TSP))
    break

MRs = [ 1 ,2 ,3 ,4 , 5 , 6]
map_replies_answers = []
for map_resolver in map_resolvers:
   No_answer_counter = 0
   row_counter = 0

   table = open('../Tables/'+map_resolver+'-Negative-LISP.csv', 'r')
   reader = csv.reader(table)
   row_medians = []
   for row in reader:
       if row[0] == '':
           Start_position = row.index(TSPs[0])
           End_position = row.index(TSPs[len(TSPs)-1]) + 1
           del row[0]
           TSPs_len = len(TSPs)
           continue
       row = row[Start_position : End_position]
       No_answer_counter = No_answer_counter + row.count('')
       row_counter = row_counter +1

   total_count = row_counter * TSPs_len
   map_reply_answer = (1-(No_answer_counter/total_count))*100
   map_replies_answers.append(map_reply_answer)




# Plot the Figure
# To automatically produce the size of the figure
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})

overall , =plt.plot(MRs , map_replies_answers  , 'ro' , label = 'one month' , ms=10)

plt.axis([ 0 , 7 , 0 , 100])
plt.grid(True)
plt.xlabel('Map Resolver' , fontsize=25)
plt.ylabel('Map Replies Answers \%' , fontsize=25)
plt.axvline(x= 3.5, color = 'k', linewidth = 1)
plt.axvline(x= 4.5, color = 'k', linewidth = 1)
plt.text( 1, 90, 'EUROPE', style='italic' , fontsize=20)
plt.text( 3.7, 90, 'US', style='italic' , fontsize=20)
plt.text( 5.5, 90, 'ASIA', style='italic' , fontsize=20)
plt.xticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
plt.yticks(fontsize=fontTick['fontsize'], fontname="Times New Roman")
# To check if the Figures path exists, otherise we create one
try:
    os.stat(os.path.join(FIGURE_PATH))
except:
    os.makedirs(os.path.join(FIGURE_PATH))
plt.savefig(os.path.join(FIGURE_PATH, 'Reliability.eps'), dpi=300, transparent=True) # you can change the name, just an example
plt.show() # When you use the above command to save the figure, you can choose to don't show the figure anymore

sys.exit()