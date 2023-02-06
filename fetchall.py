from datetime import datetime
import json
import os
import requests
from requests.auth import HTTPBasicAuth
import sqlite3
import time
from tqdm import tqdm
import xmltodict
from xml.parsers.expat import ExpatError

#https://rule34.xxx/index.php?page=forum&s=view&id=4216&pid=345
#using ?tag=id: rather than ?pid= beacuse pid requests return api abuse error
url = 'https://api.rule34.xxx//index.php?page=dapi&q=index&s=post&pid=0&limit=1000'

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
#c.execute('DELETE FROM rule34')

def insert_sqlite(values):
	insert_query = 'INSERT INTO rule34 ({}) VALUES (?{})'.format(','.join(columns), ',?'*(len(columns)-1))
	c.executemany(insert_query, values)
	db.commit() #commit every time instead of bulk incase of failure

def get_posts_count():
	try:
		r = requests.get(url)
	except Exception as e:
		print('\n'+str(e))
		exit()
	if r.status_code != 200:
		print('\n'+str(r.status_code))
		exit()

	data = json.loads(json.dumps(xmltodict.parse(r.content, attr_prefix='')))
	return data['posts']['count']

def get_start_id():
	try:
		r = requests.get(url)
	except Exception as e:
		print('\n'+str(e))
		exit()
	if r.status_code != 200:
		print('\n'+str(r.status_code))
		exit()

	data = json.loads(json.dumps(xmltodict.parse(r.content, attr_prefix='')))
	for post in data['posts']['post']:
		return post['id']

count = int(get_posts_count()) #separate total posts count from id because id does not consider deleted posts
start_id = #int(get_start_id())
error_num = 1
with tqdm(total=count/1000+1) as pbar:
	while True:
		try:
			r = requests.get('{}&tags=id:%3C{}'.format(url, start_id))
		except Exception as e:
			print('\n'+str(e))
			time.sleep(60)
			continue
		if r.status_code != 200:
			print('\n'+str(r.status_code))
			time.sleep(60)
			continue

		s = time.time()
		try:
			data = json.loads(json.dumps(xmltodict.parse(r.content, attr_prefix='')))
		except Exception as e:
			print('\n'+str(e)+'\nSkipped ID {} through {}'.format(start_id, start_id-1000))
			start_id-= 1000
			error_num += 1
			continue

		value = []
		values = []
		try:
			for post in data['posts']['post']:
				md5 = post['md5']
				if md5 in seen:
					continue
				seen[md5] = 1
				for column in columns:
					value.append(dict(post).get(column))
				values.append(list(value))
				value.clear()
		except Exception as e:
			print('\n'+str(e))
			time.sleep(60)
			continue

		if len(values) == 0:
			break

		insert_sqlite(values)
		try: #incase time is negative
			time.sleep(1-(time.time()-s))
		except:
			pass
		pbar.update(1)
		start_id -= 1000
	except Exception as e:
		print('\n'+str(e))
		time.sleep(60)
		continue

c.close()
print('\nFetched {} records, with {} requests, with {} errors'.format(len(seen), count/1000+1, error_num))
