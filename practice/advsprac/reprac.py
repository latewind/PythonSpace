import re

a = '   obj.values      '

b = re.findall('^\s+', a)
print(b)

m = re.match(r'(?P<space>^\s+)obj.(?P<value>\w+)', a)
# m = re.match(r'(?P<space>^\s+)obj\.(?P<value>\w+)',a)
print(m.group("space"))
print(m.group('value'))
