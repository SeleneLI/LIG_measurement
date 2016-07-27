#!/bin/sh

# Log script started
logger LISP Crawler launched by cron!

# TO be done: Put output in log file
# check error condition
# use one single script with argument taken from file
# v6???

nohup /usr/local/bin/python3.4 /home/crawler/controller.py ;

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR0.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR1.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR2.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR3.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR4.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR5.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR6.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR7.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR8.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR9.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR10.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR11.py &

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler-MR12.py &

nohup /usr/local/bin/python3.4 /home/crawler/ending_controller.py 

 
