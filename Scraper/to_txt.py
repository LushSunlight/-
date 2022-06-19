import json
import os
import pymysql
def connect_mysql():
    conn = pymysql.connect(
    )
    return conn

conn = connect_mysql()
cursor = pymysql.cursors.SSCursor(conn)
cursor.execute(r'select news_id,news_title,news_content,news_date from sina_news;')
# for i in range(10):
while True:
    row = cursor.fetchone()
    if not row:
        break
    if not os.path.isdir('./txts/' + str(row[3]).split(' ')[0]):
        os.mkdir('./txts/' + str(row[3]).split(' ')[0])
    f = open('./txts/' + str(row[3]).split(' ')[0] + '/' + row[0] + '.txt', mode = 'w', encoding='utf8')
    f.write(row[2].replace('/',''))
    f.close()
cursor.close()
conn.close()