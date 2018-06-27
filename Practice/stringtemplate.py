# -*- coding:utf-8 -*-
import string
import re

pattern = r'''
    (?::(?P<name>%(id)s)(?==)|
    (?<==)(?P<str>'%(val)s')|
    (?<==)(?P<num>%(val)s))
'''

pattern = pattern % {
    'id': r'[_a-z][_a-z0-9]+',
    'val': r'[_a-z0-9]+'
}

sql_log = '''
SELECT ID  FROM :TABLE WHERE AGE = :AGE AND NAME = :NAME 
'''
data = ":TABLE=USER,:NAME='Tom',:AGE=2d"


class SqlFormatTemplate(string.Template):
    delimiter = ':'


if __name__ == '__main__':
    p = re.compile(pattern, re.VERBOSE | re.IGNORECASE)

    def rep(mo):
        name = mo.group('name')
        str_value = mo.group('str')
        num_value = mo.group('num')
        if name is not None:
            return str(name)
        if str_value is not None:
            return '"{}"'.format(str_value)
        if num_value is not None:
            return r"'{}'".format(num_value)
    print(sql_log)
    print(data)
    ret = p.sub(rep, data)
    d = eval('dict({})'.format(ret))
    sql_template = SqlFormatTemplate(sql_log)
    sql = sql_template.safe_substitute(d)
    print(sql)
