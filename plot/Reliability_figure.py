import sys
import csv
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from config.config import *



map_resolvers  = ['217.8.97.6', '217.8.98.42' , '193.162.145.50' , '149.20.48.61' , '149.20.48.77' , '206.223.132.89' , '202.214.86.252' , '202.51.247.10'] # 3*EURO
MRs = [ 1 ,2 ,3 ,4 , 5 , 6 ,7 ,8 ]
map_replies_answers = []
for map_resolver in map_resolvers:
   No_answer_counter = 0
   row_counter = 0
   #table = open('test.csv', 'r')
   table = open('../Tables/'+map_resolver+'-Negative-LISP.csv', 'r')
   reader = csv.reader(table)
   row_medians = []
   for row in reader:
       if row[0] == '':
           del row[0]
           TSPs_len = len(row)
           continue
       No_answer_counter = No_answer_counter + row.count('')
       row_counter = row_counter +1

   total_count = row_counter * TSPs_len
   map_reply_answer = (1-(No_answer_counter/total_count))*100
   map_replies_answers.append(map_reply_answer)




# Plot the Figure
# To automatically produce the size of the figure
mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})

overall , =plt.plot(MRs , map_replies_answers  , 'ro' , label = 'Two weeks' )
plt.legend(handler_map={overall: HandlerLine2D(numpoints=1)})
plt.legend(handles=[overall], loc=4)
plt.axis([ 0 , 9 , 0 , 100])
plt.grid(True)
plt.xlabel('resolver')
plt.ylabel('Map Replies Answers ')
plt.axvline(x= 3.5, color = 'k', linewidth = 1)
plt.axvline(x= 6.5, color = 'k', linewidth = 1)
plt.text( 1, 90, 'EUROPE', style='italic' , fontsize=20)
plt.text( 4.5, 90, 'US', style='italic' , fontsize=20)
plt.text( 7.5, 90, 'ASIA', style='italic' , fontsize=20)
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