# -*- coding: utf-8 -*-  
import csv  
import MySQLdb
# Open database connection
db = MySQLdb.connect("localhost","root","12345678","pop_music" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

f = open('output.tsv', 'r')  
output = open("output_ok.sql","w")  
w = csv.writer(output)  
i=0
maxlen=0
max_str=""
tmp=""
pre_str=""
datarow=[]
output_query=[]
output_query.append([""])
for row_rec in csv.reader(f):  
	i=i+1
	artist = str(row_rec[len(row_rec)-3])
	rank = int(row_rec[len(row_rec)-2])
	date = int(row_rec[len(row_rec)-1])
	rec_id = '%d%03d'%(date,rank)
	now=0
	for rowlen in range(0,(len(row_rec)-3)):
		now+=1
		tmp=tmp+str(row_rec[rowlen])
		if now!=len(row_rec)-3:
			tmp=tmp+","
	max_str=tmp
	tmp=""
	song_title=str(max_str)
	# print rec_id
	datarow.append([rec_id,song_title,artist,rank,date])
	song_title=song_title.replace("'","&sbquo&")
	artist=artist.replace("'","&sbquo&")
	sql_query="INSERT INTO `pop_music`.`tw_pop` (`id`, `song_title`, `artist`, `rank`, `date`) VALUES ('%s', '%s', '%s', '%s', '%s');"%(str(rec_id),song_title,artist,str(rank),str(date))


	try:
	   # Execute the SQL command
	   cursor.execute(sql_query)
	   # Commit your changes in the database
	   db.commit()
	except:
	   # Rollback in case there is any error
	   db.rollback()

# disconnect from server
db.close()

	# print sql_query
	# output_query+=sql_query


# print datarow
# w.writerows(output_query)  
f.close()  


