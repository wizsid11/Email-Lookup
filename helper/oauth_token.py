import requests
import re
import time
import json	
import redis
redis_client = redis.Redis()
from random import choice
li_ats = ['AQEDAQKrG64FJrpFAAABVDfASIQAAAFUjDkFH00AotiJwWLcAeqsQDhJbB_ce0k0v56COcFZpyiZyBoPn-4YRDVIK4Vu8Zhy7sV0Y1wfe_dnrnfFki9MwOGCzGI7FjDVFvk73yXWSrO7f1g9M0Mm_OFE']
# li_ats = ['AQEDARz2fR4AoiTzAAABVNwmD9YAAAFU3JPs1ksAS-KL1TO_YjGyoep2vAPsa14dAmnWfW2LTZuAZ1YThTAR3RDKXFQKoOgd62q5mWiSk0RMcyAzUv7iCK1guZNSwHY1DMSrvIH2dAhJuk_GjEn83j5h',
# 'AQEDARl0XnUFvi5zAAABVNwkysMAAAFU3JKnw0sAmCs1of8r1I8khZMmIgakSWkm620BU9VAh_KKm8rYNWWzIJdETvNlYwhfBxvYONEbwMj3t9RvhSoxgrzX5o72TttpYnMBrMH2tK0IY5vziDahQSB8',
# 'AQEDARtmw1kEr9zPAAABVNw3CYAAAAFU3KTmgEsAM00NCDJ1mq4b-rfjg8bEj_2yu39IgyDFVcsGo5jEqsi-69Q6b-JoAh5DaDJi_5q-32LS6I96KSWmfumpj_7ItU4jFJr_qgPZVRddxBKeIO7JmzZm',
# 'AQEDAQvLkHgErZfBAAABVM18Q78AAAFU3Gi3iEsAD9p1sfQ_XEFZAtwAMoTc6hktI33O4pEjE-O6ZN0DV1ctN-xNw_0HD3BMjnrlB2Xwfm2tad_pG5NtxaIcsXnSGlgWQGGovQe7K0jz8hyNXBbfQhjS',
# 'AQEDARY92GoBsOJxAAABVKOOGpsAAAFU3HpGXksAy9h-UevI0NoiIiotFpTwnCJ8VdQ-_r64mzZAXDpjhFLOvT9ErvXq50xsr7XeU9SZP9Kf5sftU-bYDMVA1yMHHs6zIEEvey0kHiUVk6pvrV1S5mJo',
# 'AQEDARtYC2ICrpJjAAABVNwxAjwAAAFU3J7fPEsALeDJlQNYIvxVLPPqcnDyW4QFdKoZt6l5Nr1-RLINJC-s4X01rTPBHtegBPOnrh6k4_AqJanBpdlXG9HTPdMpmTVcWAejib9vBN2vQxUd2Wv1PGfO']
def fetch_oauth_token():
		oauth_token = redis_client.get('oauth_token')
		if oauth_token:
			return oauth_token
		else:
			url = 'https://www.linkedin.com/uas/js/userspace'
			
			params = {'apiKey': '4XZcfCb3djUl-DHJSFYd1l0ULtgSPl9sXXNGbTKT2e003WAeT6c2AqayNTIN5T1s',
								'authorize': 'true'}
			li_at = choice(li_ats)
			# li_at = li_ats[1]
			print li_at
			cookies = {'li_at': li_at}
			headers = {'referer': 'https://mail.google.com/mail/u/0/',
								 'Cache-Control': 'no-cache',
								 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13'
								 }
			res = requests.get(url, headers=headers, cookies=cookies, params=params)
			# print res.text
			pattern = r'l.oauth_token = \"(.{36})\";'
			oauth_token = re.findall(pattern, res.text)[0]
			print oauth_token
			redis_client.set('oauth_token', oauth_token)
			redis_client.expire('oauth_token', 1700)	
			return oauth_token

if __name__ == '__main__':
		print fetch_oauth_token()
