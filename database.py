import sqlite3

conn = sqlite3.connect("/var/www/html/BFS_OA/db.sqlite3")
c = conn.cursor()
c.execute("select user_id,id from 'topic_manager_meetingrecord' where real_name=''")
data = c.fetchone()
user_id = data[0]
id = data[1]
print("id:" + str(id))
print("user_id:" + str(user_id))
c.execute("select real_name from 'user_info_user' where id='"+str(user_id)+"'")
username = c.fetchone()[0]
print("username:" + username)
c.execute("update 'topic_manager_meetingrecord' set real_name='"+username+"' where id=" + str(id) + "")
print(c.fetchone())
conn.commit()
conn.close()