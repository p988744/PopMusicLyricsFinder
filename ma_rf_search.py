# encoding: utf-8
import random
import time
import requests
import MySQLdb
import re
import sys
import sys as Sys
from colorama import init
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
import selenium.webdriver.chrome.service as service
init()

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    Sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    Sys.stdout.flush()
    if iteration == total:
        print("\n")

error_counter=0
reload(sys)
sys.setdefaultencoding('utf8')

# 連結DB
db = MySQLdb.connect("localhost","root","12345678","pop_music" )

def run_query(sql_query):
	cursor = db.cursor()
	
	try:
	   # Execute the SQL command
	   cursor.execute(sql_query)
	   # Commit your changes in the database
	   db.commit()
	except:
	   # Rollback in case there is any error
	   db.rollback()
	results = cursor.fetchall()
	# disconnect from server
	# db.close()
	return results


driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.

url = "https://academic.microsoft.com/#/detail/100017521"
# print url
driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
driver.get("%s"%(url));
soup = BeautifulSoup(driver.page_source, "lxml")

print soup.findAll(attrs = {'class' : 'grey-title'}).findAll("Linked References")

for elem in soup.findAll(attrs = {'class' : 'grey-title'}):
	print(elem.get_text())
	
# driver.quit()
