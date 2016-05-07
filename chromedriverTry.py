# encoding: utf-8
import random
import time
import requests
import MySQLdb
import re
import sys
from colorama import init
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
import selenium.webdriver.chrome.service as service
init()

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

# 搜尋目標
targets = ["e-commerce","ubiquitous computing","social media","mobile commerce"]
begindate="2007"
enddate="2016"
sort_type = "0"
has_page=True

driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
check_result = 99999999999999
for target in targets:
	page=0
	total_result = check_result
	flag=0
	# print "(%d/%d)"%(page,total_result)
	urlpart_site = "https://academic.microsoft.com/"
	urlpart_target = "#/search?iq=@%s@&q=%s"%(target,target)
	urlpart_year = "&filters=Y%3C%3D2017"
	urlpart_page = "&from=%d"%page
	urlpart_sort = "&sort=%s"%(sort_type)
	url = urlpart_site+urlpart_target+urlpart_year+urlpart_page+urlpart_sort
	print url
	driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
	driver.get("%s"%(url));

	# 走訪每一頁
	while(page<=(total_result)):

		print "[%d]%f(%d/%d)"%(error_counter,float(page)/total_result*100,page,total_result)
		# page=page+8
		sleep_time=float(random.randint(1000,2000))/1000
		time.sleep(sleep_time) # Let the user actually see something!
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep_time=float(random.randint(1000,2000))/1000
		time.sleep(sleep_time) # Let the user actually see something!

		soup = BeautifulSoup(driver.page_source, "lxml")
		# print soup
		# 取得總結果數
		
		
		entrys=soup.select('.result-stats')
		for entry in entrys:
			# print entry.select('span')[2].get_text()
			if total_result == check_result:
				total_result = int(entry.select('span')[2].get_text())
			page = int(entry.select('span')[1].get_text())

		# 取得標題
		entrys = soup.select('article')
		for entry in entrys:
			paper_authors = ""
			for title in entry.select('.blue-title'):
				paper_title = title.get_text().encode('utf-8')
				paper_url = urlpart_site+title.get("href").encode('utf-8')
				paper_id = paper_url.split('/')[-1]
				# print "title:" + paper_title
				# print "url:" + paper_url
				# print "id:" + paper_id

			for meta in entry.select('.paper-meta'):
				paper_year = meta.select('span')[0].get_text().encode('utf-8')
				# print "year:" + paper_year
				for authors in meta.select('.paper-authors'):
					for author in authors.select('a'):
						# print author.get_text().encode('utf-8')
						paper_authors = paper_authors+author.get_text().encode('utf-8')+" "
					# print "authors:" +paper_authors
			# break
			insert_query = "INSERT INTO `microsoft_academic`.`search` (`id`, `search_target`, `title`, `authors`, `year`, `url`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"%(paper_id,target.replace("'","\\'"),paper_title.replace("'","\\'"),paper_authors.replace("'","\\'"),paper_year,paper_url)
			# print insert_query

			# 執行query
			cursor = db.cursor()
			
			try:
			   # Execute the SQL command
			   cursor.execute(insert_query)
			   # Commit your changes in the database
			   db.commit()
			   print (Fore.BLUE+"update success!")
			except Exception, e:
			   # Rollback in case there is any error
			   db.rollback()
			   if e[0]!=10621:
				   print (Fore.RED+"update faild!")
				   print e
		# break

		# 跳下一頁
		try:
			driver.find_element_by_class_name("icon-angle-right")
			driver.find_element_by_class_name("icon-angle-right").click()
			time.sleep(5) # Let the user actually see something!
        
			url = driver.current_url
			# driver.get(url)

	  		#driver.get(url)
		except Exception, e:
			error_counter=error_counter+1
			if error_counter >5:
				break
			print "[%d]"%error_counter
			print e
			driver.refresh() 
			print "page reflash"
			time.sleep(10) # Let the user actually see something!
			continue

		# print driver.find_element_by_class_name("icon-angle-right")
		# driver.find_element_by_class_name("icon-angle-right").click()
		time.sleep(5) # Let the user actually see something!
        
        # url = driver.current_url
        driver.get(url)
        # print "try:"+url
		
	
	break
# disconnect from server
db.close()
driver.quit()
