#Name: LISP-Views 
--------------------------------------------------------------------------------------------
#Function: 
--------------------------------------------------------------------------------------------
LISP-Views is a monitor querying all the Map-Resolvers of LISP mapping system and providing all the necessary mapping information to the users.  

--------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------
#Contents:
--------------------------------------------------------------------------------------------
- Ligcrewleres:
      o	MR_tester.py: tests the functionality of a specific Map-Resolver  ( map_resolver = str('137.194.18.132') # the Map Resolver which will be tested)
      o	Controller.py/ending_controller.py:  Managing the start and the end of the "ligcrawler-MR*.py",  gets the timestamp a save it in "Timestamp_list.log".
Ex: Time = (5*60*60)+(58*60)
      o Ligcrawler-MR*.py: Send and receive respectively the Map-Request and the Map-Reply  for a specific  Map-Resolver (MR0, MR1,ÖÖÖÖ., MR13) as follow table , Then produce the report by using "lispy": 
		Map Resolver 	IP address 
		MR0	'149.20.48.77'
		MR1	'149.20.48.61'
		MR2	'198.6.255.40'
		MR3	'217.8.98.42'
		MR4	'217.8.98.46'
		MR5	'193.162.145.50'
		MR6	'217.8.97.6'
		MR7	'202.51.247.10'
		MR8	'173.36.254.164'
		MR9	'198.6.255.37'
		MR10	'206.223.132.89'
		MR11	'202.214.86.252'
		MR12	'137.194.18.132'
		MR13	'132.227.62.246'
 
      o	Ligcrawler_B.py:  responsible for creating the Raw data by using the report which is created by "lispy"
-plot: provides several plots such as : the mean rtt of each Map resolver, the cdf of RLOC..etc.
-lispy: creates the reports and the raw data by using "display_information.py" and "display_information_B.py"
-metric: provides a statistical information from "LISP-Veiws"
-Tables: contains all the statistical information for each Map-Resolver.
-measurements: provides a statistical information from "LISPmon"
-pylisp/lig-scr: capsulation of the Map-Request and encapsulation of Map-Replay based on on RFC 6830. 
-------------------------------------------------------------------------------------------
#Usage: 
-------------------------------------------------------------------------------------------
1-download all the files.
2-<run LISP-crawler.sh>  .
3-<run LISP-crawler_B.sh>  After the first 6 hours ("controller.py" and "end_condtroller.py" setting).
4-The Report is saved in "summary" in format : <summary/EID_list_'+ str(Timestamp) +'.log'> .
5-The Raw Data is save in "data" in format : <data/' + map_resolver > :
      o LISP-Reply/ Negative Reply  format:  <data/'+ map_resolver +'/TPT-'+ EID_Prefix +'-' + map_resolver +'-' +  str(Timestamp)+ '.log'> .
      o	Time-out format:  <data/'+ map_resolver +'/TPT-'+ dst_EID + '-' + map_resolver + '-' + str(Timestamp)+'.log'>.
6-Using the plot folder the user can plot the : the mean rtt of each Map resolver, the cdf of RLOC..etc. 
--------------------------------------------------------------------------------------------



