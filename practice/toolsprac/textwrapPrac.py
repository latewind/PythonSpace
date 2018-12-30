#textwrap.py
import functools
@functools.lru_cache(maxsize=None)
def get_recent(num) :
	print (num,"in method")
	return num

print(get_recent(10))
print(get_recent(10))
print(get_recent.cache_info())