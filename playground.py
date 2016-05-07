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
get_target_query = "SELECT song_id,song_title, artist, lyric_link, publish_date FROM pop_music.song_info order by on_Rank_count desc;"
results = run_query(get_target_query)

for song in results:
	sleep_time=float(random.randint(500,1000))/1000
	
	song_id=song[0]
	song_title=song[1]
	artist=song[2]
	song_album=""
	song_time=song[4]
	if (song_time != "9999-99") & (song_time != None):
		continue
	else:
		song_time="9999-99"
		song_link=""

		lyric_link=song[3]
		# print lyric_link
		current_target=[song_title,artist]
		# current_link="https://www.google.com.tw/search?q=site:https://mojim.com+%s+\"%s\"+歌詞"%(current_target[1],current_target[0])
		current_link='https://mojim.com/%s.html?t3'%(song_title)
		# if functions.is_exist(current_link)==True:
		print (Back.YELLOW +current_link)
		rs = requests.session()
		res = rs.get(current_link, verify=True)
		# print res.text
		soup = BeautifulSoup(res.text, "lxml")
		# print soup
		entrys=soup.select('dd')
		# print entrys
		tmp_song_link = ""
		tmp_song_title = ""
		tmp_song_artist = ""
		found_flag = 0
		for entry in entrys:
			if found_flag == 1:
				break
			# 取得時間
			if len(entry.select('.mxsh_ss5')) > 0:
				tmp_song_time = entry.select('.mxsh_ss5')[0].get_text()
				# print tmp_song_time
			# 取得專輯
			if len(entry.select('.mxsh_ss3 a')) > 0:
				tmp_song_album = entry.select('.mxsh_ss3 a')[0].get_text()
				# print tmp_song_album
			# 取得歌名
			if len(entry.select('.mxsh_ss4 a')) > 0:
				tmp_song_data = entry.select('.mxsh_ss4 a')[0]
				tmp_song_link =  "https://mojim.com"+tmp_song_data.get('href')
				tmp_song_title = tmp_song_data.get('title').split("歌詞")[0][:-1]
				tmp_song_artist = tmp_song_data.get('title').split("歌詞")[1][1:]
				try:
					tmp_song_artist=tmp_song_artist.split('(')[0]
				except:
					tmp_song_artist=tmp_song_artist
				# 取得查詢列表
				# for link in entry.select('.mxsh_ss4 a'):
				# 	tmp_song_link =  "https://mojim.com"+link.get('href')
				# 	tmp_song_title = link.get('title').split(" ")[0]
				# 	tmp_song_artist = link.get('title').split(" ")[2]
				# 	try:
				# 		tmp_song_artist=tmp_song_artist.split('(')[0]
				# 	except:
				# 		tmp_song_artist=tmp_song_artist
				# print (Back.BLACK+"title:[%s][%s]"%(tmp_song_title,song_title))
				# print (Back.BLACK+"artist:[%s][%s]"%(tmp_song_artist,artist))
				print (Back.BLACK+">>>>>>>>>>>>>>>>>>")
				if  ((tmp_song_artist.lower()) == (artist.lower())) :
					song_title = tmp_song_title
					song_time = "8888-88"
					print (Back.BLUE +"****title:[%s][%s]"%(tmp_song_title,song_title))
					print (Back.BLUE +"****artist:[%s][%s]"%(tmp_song_artist,artist))
					print (Back.BLACK+">>>>>>>>>>>>>>>>>>")
				if ((tmp_song_title.lower()) == (song_title.lower())) & ((tmp_song_artist.lower()) == (artist.lower())) :
					print ">>right one"
					try:
						if int(tmp_song_time.split('-')[0])<int(song_time.split('-')[0]):
							song_time=tmp_song_time
							song_album=tmp_song_album
							song_link=tmp_song_link
							print (Back.BLUE +"time:[%s]"%(tmp_song_time))
							print (Back.BLUE +"album:[%s]"%(tmp_song_album))
							print (Back.BLUE +"title:[%s]"%(tmp_song_title))
							print (Back.BLUE +"artist:[%s]"%(tmp_song_artist))
							print (Back.BLUE +"-----------------")
					except Exception, e:
						song_time="unknow"
						song_album=tmp_song_album
						song_link=tmp_song_link
						print (Back.BLUE +"time:[%s]"%(tmp_song_time))
						print (Back.BLUE +"album:[%s]"%(tmp_song_album))
						print (Back.BLUE +"title:[%s]"%(tmp_song_title))
						print (Back.BLUE +"artist:[%s]"%(tmp_song_artist))
						print (Back.BLUE +"-----------------")
						print e
						# print "pass"
			# if len(link.get('href').split('x')) is 3:
			# 	lyric_link = link.get('href').split('/url?q=')[1]
			# 	print lyric_link
			else:
				continue

			# 	break
		if song_time == "9999-99":
			print (Back.RED+"[%s]%s, %s, %s, %s"%(song_time,song_title,song_album,artist,song_link))
		else:
			print (Back.GREEN+"[%s]%s, %s, %s, %s"%(song_time,song_title,song_album,artist,song_link))
		
		update_link_query="UPDATE `pop_music`.`song_info` SET `publish_date`='%s', `lyric_link`='%s', `album`='%s' WHERE `song_id`='%s';"%(song_time,song_link,song_album.replace("'","\\'"),song_id)
		
		cursor = db.cursor()
		
		try:
		   # Execute the SQL command
		   cursor.execute(update_link_query)
		   # Commit your changes in the database
		   db.commit()
		   print "update success!"
		except:
		   # Rollback in case there is any error
		   db.rollback()
		   print "update faild!"
		   print update_link_query
		# results = cursor.fetchall()
		# break
		print "================================"
# disconnect from server
db.close()
