#!/bin/sh

#log script started
logger LISP Crawler launched by cron!

# TO be done : Put output in log file 
# check error condition 
# use one single script with argument taken from file 
# v6???

nohup /usr/local/bin/python3.4 /home/crawler/ligcrawler_B.py
 
