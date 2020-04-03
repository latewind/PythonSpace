# sqlitePrac.py
import sqlite3
import collections

User = collections.namedtuple('User', ['username', 'password'])
conn = sqlite3.connect('D:\Tools\SQLite\wind')
c = conn.cursor()
# c.execute(''' INSERT INTO user
#				(user_name,password) VALUES 
#				('lsqwell','123456')''')
# conn.commit()
c.execute(''' SELECT user_name,password FROM USER ''')

# User._make(c.fetchall());
# print(c.fetchall())
username = 'lsqwell and 1=1'
c.execute('select user_name,password from user where user_name = ?',
          (username,))

print(str(c))
for _ in c.fetchall():
    u = User._make(_)
    print(u, '1')

m = map(User._make, c.fetchall())
for u in m:
    print(u.key, u.value)
conn.close()
