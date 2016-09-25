__author__ = 'yueli'

from config.config import *
import datetime

# To get current date
now = datetime.datetime.now()

# ==========================================Section: constant variable declaration======================================
START_DATE = '20160818'
STOP_DATE = '20160920'

# Build the 'year', 'month' and 'day'
year_list = [str(year) for year in range(2010, 2017)]
month_list = []
for month in range(1, 13):
    month_list.append(str('%02d'%month))
day_list = []
for day in range(1, 32):
    day_list.append(str('%02d'%day))



# ==========================================Section: functions declaration======================================
# To calculate the number of EID-prefix
def eid_prefix_num_counter(start_date, stop_date):
    print('The number of EID-prefixes:')
    eid_prefix_num_list = []

    for year in year_list:
        for month in month_list:
            for day in day_list:
                if int(start_date) <= int('{0}{1}{2}'.format(year, month, day)) <= int(stop_date):
                    target_url = 'http://lispmon.net/mappings/EID4_mappings_{0}{1}{2}.txt'.format(year, month, day)
                    # print(target_url)
                    eid_prefix_list = []

                    try:
                        response = urllib.request.urlopen(target_url)
                        html = response.read()
                        for line in html.split(b'\n'):
                            # Remove the sentence beginning with '#', '&' and '>', as well as the empty line
                            if line.startswith(b'#') or line.startswith(b'&') or line.startswith(b'>') or line == b'':
                                continue
                            # The returned legency/EID prefix
                            elif len(line.split(b',')) > 1:
                                if line.split(b',')[1] == b'1':
                                    # eid_counter += 1
                                    eid_prefix_list.append(line.split(b',')[0])

                        eid_prefix_counter = len(list(set(eid_prefix_list)))
                        eid_prefix_num_list.append(eid_prefix_counter)
                        print('{0}-{1}-{2}:'.format(year, month, day), eid_prefix_counter)

                    except urllib.request.HTTPError:
                        print('HTTP Error 404: Not Found')



    print('eid_prefix_num_list =', eid_prefix_num_list)
    return eid_prefix_num_list


# To calculate the number of RLOC
def rloc_num_counter(start_date, stop_date):
    print('The number of RLOCs:')
    rloc_num_list = []
    for year in year_list:
        for month in month_list:
            for day in day_list:
                if int(start_date) <= int('{0}{1}{2}'.format(year, month, day)) <= int(stop_date):
                    target_url = 'http://lispmon.net/mappings/EID4_mappings_{0}{1}{2}.txt'.format(year, month, day)
                    print(target_url)
                    rloc_list = []

                    try:
                        response = urllib.request.urlopen(target_url)
                        html = response.read()
                        for line in html.split(b'\n'):
                            # Only count the sentence beginning with '&'
                            if line.startswith(b'>'):
                                rloc_list.append(line.split(b' ')[1])

                        rloc_counter = len(list(set(rloc_list)))
                        rloc_num_list.append(rloc_counter)
                        print('{0}-{1}-{2}:'.format(year, month, day), rloc_counter)



                    except urllib.request.HTTPError:
                        print('HTTP Error 404: Not Found')

    print('rloc_num_list =', rloc_num_list)

    return rloc_num_list




# ==========================================Section: main function declaration======================================
if __name__ == "__main__":
    # To calculate the number of EID-prefix
    eid_prefix_num_counter(START_DATE, STOP_DATE)
    # To calculate the number of RLOC
    rloc_num_counter(START_DATE, STOP_DATE)