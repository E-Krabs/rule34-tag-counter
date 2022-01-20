import requests
from requests.auth import HTTPBasicAuth
import time
import json

url = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit=1000&json=1"
e621_agent = {
   'User-Agent': 'TagData (by USERNAME)', # replace with your username
   'login': 'EKrabs', # your username
   'api_key': '' # your api key
}

login = '' # your username
api_key = '' # your api key

page_id = 0 #3053317 3011070 2992268 518808
seen = {} #[]
run = 0
directory = 'C:/Scripts/Python/r34/'
''' When refreshing data, change 'w' to 'a' '''
with open('{}JSON/r34-total-2022-01-20-a.json'.format(directory), 'w') as f:
	''' When refreshing data, replace f.write('[') to (',') '''
	f.write('[')
	while True:
		while_start = time.time()
		''' When refreshing data, change page=b{} to page=a{} '''
		r = requests.get('{}&pid={}'.format(url, page_id))#headers=e621_agent, auth=HTTPBasicAuth(login, api_key))
		#print('{}&pid={}'.format(url, page_id))
		if r.status_code != 200:
			print('Error {}, waiting 10 seconds'.format(r.status_code))
			time.sleep(10)
			break

		data = r.json()
		for item in data:
			post_id = item['id']
			file_hash = item['hash']
			''' Check if image was already indexed by comparing md5 '''
			if file_hash in seen:
				continue
			seen[file_hash] = 1
			#seen.append(item['file']['md5'])
			print('#{} dumped {}'.format(run, post_id))
			f.write(json.dumps(item)) #+ '\n'
			f.write(',')
		''' When refreshing data, change -= 320 to += 320 '''
		time.sleep(2)
		now = time.time()
		#if now-while_start < 3:
		#	break
		print('Loop {}: {}'.format(run, now-while_start))
		print(len(seen))
		page_id += 1
		run += 1
	f.write(']')

print('Fetched {} records, with {} requests'.format(len(seen), run-1))
