import re

a= '   a      '

b = re.findall('^\s+',a)
print(b)