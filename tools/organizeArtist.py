# -*- coding: utf-8 -*-  
import csv  
import MySQLdb
# Open database connection
db = MySQLdb.connect("localhost","root","12345678","pop_music" )

# prepare a cursor object using cursor() method
cursor = db.cursor()
sql_query = "SELECT song_title, artist, COUNT(*) AS Rank_counts FROM pop_music.tw_pop WHERE id IS NOT NULL GROUP BY song_title,artist ORDER BY Rank_counts desc;"


try:
   # Execute the SQL command
   cursor.execute(sql_query)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

results = cursor.fetchall()


# 整理文字
def organizeTitle(title_str):
	# title_str=u"缺口 (三立9點華劇【我們發財了】聊愛K歌)"
	# print title_str
	search_first_char=['(','（','【','[','『','「']
	search_last_char=[')','）','】',']','』','」']
	first_search_char=""
	last_search_char=""
	tmp_first_index=len(title_str)
	tmp_last_index=0
	# 搜尋最前面的目標字元
	for i in search_first_char:
		try:
			if title_str.index(i)<tmp_first_index:
				first_search_char=i
				tmp_first_index=title_str.index(i)
			print tmp_first_index
			print "first>>>[%d]%s"%(tmp_first_index,title_str[tmp_first_index])
		except:
			continue
	# 搜尋最後面的目標字元
	for i in search_last_char:
		try:
			if title_str.index(i)>tmp_last_index:
				last_search_char=i
				tmp_last_index=title_str.index(i)
			print "last>>>[%d]%s"%(tmp_last_index,title_str[tmp_last_index])
		except:
			continue

	try:
		main_title =  title_str.split(first_search_char)[0].split(" ")[0]
		sub_title = ""
		for tmp_str in range(1,len(title_str.split(first_search_char))):
			print "[%d]%s"%(tmp_str,title_str.split(first_search_char)[tmp_str])
			sub_title += title_str.split(first_search_char)[tmp_str]
		sub_title=sub_title.split(last_search_char)[0]
		print sub_title

	except:
		main_title = title_str
		sub_title = ""

	result_title=[main_title,sub_title]
	# print title_str+">>>"+result_title[0]
	# print title_str+">>>"+result_title[1]
	return result_title


# 主程式
for record in results: 
 	song_title = record[0]
  	artist = record[1]
  	rank_count=record[2]
  	song_id=hash(song_title+artist)
  	result_artist=organizeTitle(artist)
  	artist=result_artist[0]
  	artist_second_name=result_artist[1]
  	# print "[%s] %s, %s" % (song_title, subtitle, artist)
  	# print "==============================================="
  	# insert_query="INSERT INTO `pop_music`.`song_info` (`song_id`, `song_title`, `artist`, `on_Rank_count`) VALUES ('%s', '%s', '%s', '%s');"%(song_id,song_title,artist,str(rank_count))
  	update_query="UPDATE `pop_music`.`song_info` SET `artist`='%s', `artist_second_name` ='%s' WHERE `song_id` = '%s';"%(artist,artist_second_name,song_id)


  	try:
		# Execute the SQL command
		cursor.execute(update_query)
		# Commit your changes in the database
		db.commit()
		# print "update success!"
	except MySQLdb.Error as e:
		# Rollback in case there is any error
		print "insert failed! \n%s"%(e)
			# update_query="UPDATE `pop_music`.`song_info` SET `on_Rank_count`='%s' WHERE `song_id`='%s';"%(str(count+1),song_id)
			# cursor.execute(update_query)
		db.rollback()
# disconnect from server
db.close()

	# print sql_query
	# output_query+=sql_query


# print datarow
# w.writerows(output_query)
