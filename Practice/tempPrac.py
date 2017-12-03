#tempPrac.py
from fileinput import FileInput
import glob
with FileInput(glob.glob('D:/Test/*.log')) as input :
	for line in input :
		print('{0}:{1}:{2}'.format(input.filename(),input.lineno(),line[:-1]))
import os
from os.path import join, getsize
for root, dirs, files in os.walk('D:/'):
	if not dirs and not files :
		print(root)

