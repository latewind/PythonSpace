# -*- coding:utf-8 -*-
# 将参数放入到 sql语句中
import string
sqlLog = '''
select :name from :db
'''
data = ':db="user",name=":name"'


class SqlFormatTemplate(string.Template):
    delimiter = ':'


if __name__ == '__main__':
    s = SqlFormatTemplate(sqlLog)

    data = ':db="user",name=":name"'
    newData = data.replace(':', '')
    d = 'dict({})'.format(newData)
    a = eval(d)
    ss = s.safe_substitute(a)
    print(ss)
