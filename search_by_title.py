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
init()


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

# 取得查詢目標資料
get_target_query = "SELECT song_id,song_title, artist, lyric_link, publish_date, lyrics FROM pop_music.song_info order by on_Rank_count desc;"
results = run_query(get_target_query)

for song in results:
	sleep_time=float(random.randint(500,1000))/1000
	
	song_id=song[0]
	song_title=song[1]
	artist=song[2]
	song_link=song[3]
	song_time=song[4]
	song_lyric = song[5]
	if (song_time == "8888-88") | (song_time == "9999-99") | (song_time is None):
		continue
	else:
		# print lyric_link
		current_target=[song_title,artist]
		# current_link="https://www.google.com.tw/search?q=site:https://mojim.com+%s+\"%s\"+歌詞"%(current_target[1],current_target[0])
		current_link=song_link
		# if functions.is_exist(current_link)==True:
		print (Fore.YELLOW+current_link)
		rs = requests.session()
		res = rs.get(current_link, verify=True)
		res_text = res.text.replace('更多更詳盡歌詞 在 <a href="http://mojim.com" >※ Mojim.com　魔鏡歌詞網 </a>','').replace("<br />","\n")
		soup = BeautifulSoup(res_text, "lxml")
		# print soup
		entrys=soup.select('.fsZx3')
		for entry in entrys:
			song_lyric = entry.get_text()
			print (Fore.WHITE+song_lyric)
			# print entry.get_text().replace("更多更詳盡歌詞 在 ※ Mojim.com　魔鏡歌詞網","")
		print (Fore.WHITE+"[%s]%s"%(song_title,song_lyric))
		
		update_link_query="UPDATE `pop_music`.`song_info` SET `lyrics`='%s' WHERE `song_id`='%s';"%(song_lyric.replace("'","\\'"),song_id)
		# update_link_query=""
		cursor = db.cursor()
		
		try:
		   # Execute the SQL command
		   cursor.execute(update_link_query)
		   # Commit your changes in the database
		   db.commit()
		   print (Fore.BLUE+"update success!")
		except:
		   # Rollback in case there is any error
		   db.rollback()
		   print (Fore.RED+"update faild!")
		   print update_link_query
		# results = cursor.fetchall()
		# break
		print "================================"
# disconnect from server
db.close()
