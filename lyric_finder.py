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

def chack_song_member(song_lyric):
	check_lyricist = "作詞" in song_lyric
	check_composer = "作曲" in song_lyric
	check_arranger = "編曲" in song_lyric
	check_producer = "監製" in song_lyric
	check_singer = "演唱" in song_lyric
	tmp_lyricist= ""
	tmp_composer = ""
	tmp_arranger = ""
	tmp_producer = ""
	tmp_singer = ""
	last_member = -1
	if check_lyricist:
		tmp_lyricist = song_lyric.split("作詞")[1].split('\n')[0].replace("：","")
		last_member=0
	if check_composer:
		tmp_composer = song_lyric.split("作曲")[1].split('\n')[0].replace("：","")
		last_member=1
	if check_arranger:
		tmp_arranger = song_lyric.split("編曲")[1].split('\n')[0].replace("：","")
		last_member=2
	if check_producer:
		tmp_producer = song_lyric.split("監製")[1].split('\n')[0].replace("：","")
		last_member=3
	if check_singer:
		tmp_singer = song_lyric.split("演唱")[1].split('\n')[0].replace("：","")
		last_member=4
	tmp_song_member = [tmp_lyricist,tmp_composer,tmp_arranger,tmp_producer,tmp_singer,last_member]
	return tmp_song_member

# 取得查詢目標資料
get_target_query = "SELECT song_id,song_title, artist, lyric_link, publish_date, lyrics, on_Rank_count FROM pop_music.song_info order by on_Rank_count desc;"
results = run_query(get_target_query)

for song in results:
	sleep_time=float(random.randint(500,1000))/1000
	song_time=song[4]
	song_id=song[0]
	song_lyric = song[5]
	# lyricist = "" #作詞者
	# composer = "" #作曲者
	# arranger = "" #編曲者
	# producer = "" #監製者
	# singer = "" #演唱者
	find_lyricist_flag=0

	if (song_time == "8888-88") | (song_time == "9999-99") | (song_time is None) | (song_lyric is None):
		continue
	else:
		song_members = chack_song_member(song_lyric)
		lyricist = song_members[0] #作詞者
		composer = song_members[1] #作曲者
		arranger = song_members[2] #編曲者
		producer = song_members[3] #監製者
		singer = song_members[4] #演唱者
		if song_members[5] != -1:
			new_lyric = song_lyric.split(song_members[song_members[5]])[1]
		else:
			new_lyric =song_lyric
		print "作詞者"+lyricist
		print "作曲者"+composer
		print "編曲者"+arranger
		print "監製者"+producer
		print "演唱者"+singer
		update_query = "UPDATE `pop_music`.`song_info` SET `lyrics`='%s', `lyricist`='%s', `composer`='%s', `arranger`='%s', `producer`='%s' WHERE `song_id`='%s';"%(new_lyric.replace("'","\\'"), lyricist.replace("'","\\'"), composer.replace("'","\\'"), arranger.replace("'","\\'"), producer.replace("'","\\'"),song_id)
		# update_link_query=""
		cursor = db.cursor()
		
		try:
		   # Execute the SQL command
		   cursor.execute(update_query)
		   # Commit your changes in the database
		   db.commit()
		   print (Fore.BLUE+"update success!")
		except Exception, e:
		   # Rollback in case there is any error
		   db.rollback()
		   print (Fore.RED+"update faild!")
		   print e
		# results = cursor.fetchall()
		# break
	# break
# disconnect from server
db.close()
