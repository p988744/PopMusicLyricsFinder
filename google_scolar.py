# encoding: utf-8
import random
import time
import requests
import MySQLdb
import re
import sys
import db_settings
import functions
from bs4 import BeautifulSoup
import lxml
from colorama import init
from colorama import Fore, Back, Style
from selenium import webdriver

ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
url = "https://academic.microsoft.com/"
# url = "https://scholar.google.com.tw/scholar?cites=6540177324500022107&as_sdt=2005&sciodt=0,5&hl=zh-TW&oe=BIG5"
rs = requests.session()
res = rs.get(url, headers=ua)
# print res.text
soup = BeautifulSoup(res.text, "lxml")
# print soup
entrys=soup.select('.story-title')

for entry in entrys:
	print "get" + entry
	# p_title = entry.select(".gs_rt")[0].get_text().lstrip(" ")

	# p_auther = entry.select(".gs_a")[0].get_text().split("-")[0].lstrip(" ")
	# print(p_auther)
	# if p_auther != "":
	# 	p_year = entry.select(".gs_a")[0].get_text().split("-")[1].lstrip(" ")
	# 	if len(p_year)>4:
	# 		p_type = p_year.split(",")[0].lstrip(" ")
	# 		p_year = p_year.split(",")[1].lstrip(" ")
	# else:
	# 	p_year = ""
	# 	p_type = ""
	# p_site = entry.select(".gs_a")[0].get_text().split("-")[2].lstrip(" ")
	# p_cited = entry.select(".gs_fl")[0].select("a")[0].get_text().split(" ")[1].lstrip(" ")
	# p_cited_link = "https://scholar.google.com.tw"+entry.select(".gs_fl")[0].select("a")[0].get("href").lstrip(" ")
	
	# print ("========================\n[  title ] %s\n[ auther ] %s\n[   Year ] %s\n[   site ] %s\n[  cited ] %s\n[   link ] %s")%(p_title,p_auther,p_year,p_site,p_cited,p_cited_link)
	