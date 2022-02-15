import os
import requests
from requests.auth import HTTPBasicAuth
import time
import xmltodict
import json
from datetime import datetime
import sqlite3
from tqdm import tqdm
from xml.etree import ElementTree
url = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit=1000&json=0'
pid = 0
seen = {}
cwd = os.getcwd()
year = datetime.now().year
month = datetime.now().month
day = datetime.now().day
columns = ['height', 'score', 'file_url', 'parent_id', 'sample_url', 'sample_width', 
	'sample_height', 'preview_url', 'rating', 'tags', 'id', 'width', 'change'
	'md5', 'creator_id', 'has_children', 'created_at', 'status', 'sorce'
	'has_notes', 'has_comments', 'preview_width', 'preview_height']

db = sqlite3.connect('{}/rule34-total-{}-{}-{}.sqlite'.format(cwd, year, month, day))
c = db.cursor() 
c.execute('CREATE TABLE IF NOT EXISTS rule34 ({})'.format(' text,'.join(columns)))

def insert_sqlite(values):
	insert_query = 'INSERT INTO rule34 ({}) VALUES (?{})'.format(','.join(columns), ',?'*(len(columns)-1))
	c.executemany(insert_query, values)

def get_posts_count():
	r = requests.get('{}'.format(url))
	if r.status_code != 200:
		print(r.status_code)
		exit()

	data = json.dumps(xmltodict.parse(r.content))
	#with open('o.txt', 'w') as o:
	#	o.write(data) 
	data = json.loads(data)
	return data['posts']['@count']

count = get_posts_count()

with tqdm(total=int(count)/1000+1) as pbar:
	while True:
		r = requests.get('{}&pid={}'.format(url, pid))
		if r.status_code != 200:
			print(r.status_code)
			time.sleep(15)
			continue
		s = time.time()

		data = json.loads(json.dumps(xmltodict.parse(r.content)))
		value = []
		values = []
		for post in data['posts']['post']:
			_id = post['@id']
			md5 = post['@md5']
			if md5 in seen:
				continue
			seen[md5] = 1
			#print(_id)
			for item in columns:
				value.append(json.dumps(dict(post).get(item)))
			values.append(list(value))
			value.clear()

		if len(values) == 0:
			break

		insert_sqlite(values)
		time.sleep(1-(time.time()-s))
		pbar.update(1)
		pid += 1

db.commit()
c.close()
print('fetched {} records, with {} requests'.format(len(seen), start_id/320+1))
