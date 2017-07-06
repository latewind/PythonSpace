import re
sqls=[]
with open('E:/Work/csv/地方级2017年2月.csv','r') as f:
	for line in  f:
		if line.startswith(' 1'):
				newline = re.split(' +|"|\n',line)
				l=[ x.replace(',','') for x in newline if x is not '']
				sqls.append('insert into table (col1,col2,col3,col4) values (\'{0}\',\'{1}\',\'{2}\',\'{3}\');'.format(*l))
with open('E:/sql.sql','w') as f:
	for sql in sqls:
		f.write(sql+'\n')