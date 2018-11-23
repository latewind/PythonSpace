import re
def read_file():
    with open('E:/Work/csv/地方级2017年2月.csv','r') as f:
        for line in  f:
            if line.startswith(' 1'):
                    newline = re.split(' +|"|\n',line)
                    l=[ x.replace(',','') for x in newline if x is not '']
                    yield 'insert into table (col1,col2,col3,col4) values (\'{0}\',\'{1}\',\'{2}\',\'{3}\');'.format(*l)

with open('E:/sql.sql','a') as f:
    for sql in read_file():
        f.write(sql+'\n')