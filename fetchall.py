from datetime import datetime
import json
import os
import requests
from requests.auth import HTTPBasicAuth
import sqlite3
import time
from tqdm import tqdm
import xmltodict

url = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit=1000&json=0'

pid = 0
seen = {}
cwd = os.getcwd()
year = datetime.now().year
month = datetime.now().month
day = datetime.now().day
columns = ['height', 'score', 'file_url', 'parent_id', 'sample_url', 'sample_width', 
	'sample_height', 'preview_url', 'rating', 'tags', 'id', 'width', 'change',
	'md5', 'creator_id', 'has_children', 'created_at', 'status', 'source',
	'has_notes', 'has_comments', 'preview_width', 'preview_height']

db = sqlite3.connect('{}/rule34-total-{}-{}-{}.sqlite'.format(cwd, year, month, day))
c = db.cursor() 
c.execute('CREATE TABLE IF NOT EXISTS rule34 ({})'.format(' text,'.join(columns)))
c.execute('DELETE FROM rule34')

def insert_sqlite(values):
	insert_query = 'INSERT INTO rule34 ({}) VALUES (?{})'.format(','.join(columns), ',?'*(len(columns)-1))
	c.executemany(insert_query, values)

def get_posts_count():
	try:
		r = requests.get(url)
	except Exception as e:
		print(e)
		exit()
	if r.status_code != 200:
		print(r.status_code)
		exit()

	data = json.loads(json.dumps(xmltodict.parse(r.content, attr_prefix='')))
	return data['posts']['count']

count = get_posts_count()

with tqdm(total=int(count)/1000+1) as pbar:
	while True:
		try:
			r = requests.get('{}&pid={}'.format(url, pid))
		except Exception as e:
			print('\n'+str(e))
			time.sleep(60)
			continue
		if r.status_code != 200:
			print('\n'+str(r.status_code))
			time.sleep(60)
			continue

		s = time.time()
		data = json.loads(json.dumps(xmltodict.parse(r.content, attr_prefix='')))
		value = []
		values = []
		for post in data['posts']['post']:
			#_id = post['id']
			md5 = post['md5']
			if md5 in seen:
				continue
			seen[md5] = 1
			#print(_id)
			for column in columns:
				value.append(dict(post).get(column))
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
print('\nfetched {} records, with {} requests'.format(len(seen), count/1000+1))
