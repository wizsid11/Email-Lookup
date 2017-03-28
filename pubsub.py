import sqlite3
import redis
import json
import re, itertools
from helper.info import get_all_verified_emails

conn = sqlite3.connect('./app/db.sqlite3')
c = conn.cursor()


class PubSub(object):



    def __init__(self, redis, channel="default"):
        self.redis = redis
        self.channel = channel

    def publish(self, data):
        self.redis.publish(self.channel, json.dumps(data))

    def subscribe(self, handler):
        redis = self.redis.pubsub()
        redis.subscribe(self.channel)

        for data_raw in redis.listen():
            if data_raw['type'] != "message":
                continue

            data = json.loads(data_raw["data"])
            handler(data)


def handler(data):
    print data
    cleaned_name = re.sub(r' +', ' ', data['name']).lower().strip()
    cleaned_domain = data['domain'].lower().strip()
    parts = cleaned_name.split(' ')
    if len(parts) == 1:
        all_emails = get_all_verified_emails(cleaned_name, cleaned_domain)
    else:
        all_combinations = list(itertools.combinations(parts, 2))
        all_emails = {'using_emailahoy':[],'using_linkedin': []}
        for x in all_combinations:
            all_verified_emails = get_all_verified_emails(" ".join(x), cleaned_domain)
            all_emails['using_emailahoy'] = all_emails['using_emailahoy'] + all_verified_emails['using_emailahoy']
            all_emails['using_linkedin'] = all_emails['using_linkedin'] + all_verified_emails['using_linkedin']
 
    c.execute("""UPDATE email_hack_emailfinder SET verified_emails = ? WHERE id = ?""" , (json.dumps(
        all_emails), str(data['id'])))
    # print all_emails
    conn.commit()


def main():

    r = redis.Redis()

    q = PubSub(r, "channel")
    q.publish("test data")
 
    q.subscribe(handler)

if __name__ == '__main__':
    main()
