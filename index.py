import os
import sys
from upload_file import upload_file

local_dir = sys.argv[1]

def is_done(item):
	return item.split('.')[0] == 'done'

def upload(dir):
	for item in os.listdir(dir): 
		path = os.path.join(dir, item)
		if os.path.isdir(path):
			upload(path)
		elif is_done(item):
			continue
		else:
			upload_file(item, dir, dir[19:])

upload(local_dir)