#textwrap.py
import functools
@functools.lru_cache(maxsize=None)
def get_recent(num) :
	print (num)
	return num

get_recent(10)
get_recent(10)
print(get_recent.cache_info())