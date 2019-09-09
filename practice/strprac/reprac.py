import re

pattern = r'''(?P<task_type>\w+)\((?P<cur>\d+)/(?P<total>\d+)'''

s = '''师门-收集物品(9/10)'''
m = re.search(pattern, s)
print(m)
print(m.group('cur'))
print(m.group('total'))
print(m.group('task_type'))
