import requests
import re
import time
import json	
import redis
redis_client = redis.Redis()
from random import choice
li_ats = ['AQEDAQKrG64FJrpFAAABVDfASIQAAAFUjDkFH00AotiJwWLcAeqsQDhJbB_ce0k0v56COcFZpyiZyBoPn-4YRDVIK4Vu8Zhy7sV0Y1wfe_dnrnfFki9MwOGCzGI7FjDVFvk73yXWSrO7f1g9M0Mm_OFE']

def fetch_oauth_token():
		oauth_token = redis_client.get('oauth_token')
		if oauth_token:
			return oauth_token
		else:
			url = 'https://www.linkedin.com/uas/js/userspace'
			
			params = {'apiKey': '4XZcfCb3djUl-DHJSFYd1l0ULtgSPl9sXXNGbTKT2e003WAeT6c2AqayNTIN5T1s',
								'authorize': 'true'}
			li_at = choice(li_ats)

			print li_at
			cookies = {'li_at': li_at}
			headers = {'referer': 'https://mail.google.com/mail/u/0/',
								 'Cache-Control': 'no-cache',
								 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13'
								 }
			res = requests.get(url, headers=headers, cookies=cookies, params=params)

			pattern = r'l.oauth_token = \"(.{36})\";'
			oauth_token = re.findall(pattern, res.text)[0]
			print oauth_token
			redis_client.set('oauth_token', oauth_token)
			redis_client.expire('oauth_token', 1700)	
			return oauth_token

if __name__ == '__main__':
		print fetch_oauth_token()
