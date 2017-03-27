import requests
import json
import sys
import time
from oauth_token import fetch_oauth_token
from combinations import generate_emails_from_name_and_domain
from emailahoy import VerifyEmail
# from validate_email import validate_email
from termcolor import colored


def fetch_info_by_email(email):
    url = 'https://api.linkedin.com/v1/people/email=' + email + \
        ':(first-name,last-name,headline,location,positions,twitter-accounts,im-accounts,phone-numbers,picture-urls::(original),site-standard-profile-request,public-profile-url)'
    headers = {'content-type': 'application/json',
               'oauth_token': fetch_oauth_token(),
               'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36',
               'x-li-format': 'json'
               }
    res = requests.get(url, headers=headers)
    return json.loads(res.text)


def fetch_info_by_personal_details(first_name, last_name, company_name):
    # url = 'https://api.linkedin.com/v1/people/~'
    url = 'https://api.linkedin.com/v1/people-search?first-name=' + \
        first_name + '&last-name=' + last_name + \
        '&company-name=' + company_name

    headers = {'content-type': 'application/json',
               'oauth_token': fetch_oauth_token(),
               'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36',
               'x-li-format': 'json'
               }
    res = requests.get(url, headers=headers)
    return json.loads(res.text)


def fetch_info_by_keywords_and_location(keywords, postal_code, distance, start, count):
    url = 'https://api.linkedin.com/v1/people-search?keywords=' + keywords + \
        '&postal-code=' + postal_code + '&distance=' + \
        distance + '&start=' + str(start) + '&count=' + str(count)

    headers = {'content-type': 'application/json',
               'oauth_token': fetch_oauth_token(),
               'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36',
               'x-li-format': 'json'
               }
    res = requests.get(url, headers=headers)
    return json.loads(res.text)


def fetch_info_by_id(user_id):
    # url = 'https://api.linkedin.com/v1/people/~'
    url = 'https://api.linkedin.com/v1/people/id=' + user_id + \
        ':(first-name,last-name,headline,location,positions,twitter-accounts,im-accounts,phone-numbers,picture-urls::(original),site-standard-profile-request,public-profile-url)'
    headers = {'content-type': 'application/json',
               'oauth_token': fetch_oauth_token(),
               'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36',
               'x-li-format': 'json'
               }
    res = requests.get(url, headers=headers)
    return json.loads(res.text)


def get_all_verified_emails(name, domain):

    start_time = time.time()
    emails = generate_emails_from_name_and_domain(
        name=name, domain=domain)
    print emails
    found_using_linkedin = []
    found_using_emailahoy = []
    # found_using_validate_email = []
    for email in emails:
        print '------'
        print 'checking ', colored(email, 'blue')
        print '------'
        info_by_email = fetch_info_by_email(email)
        if 'message' in info_by_email.keys():
            message = info_by_email['message']
            if 'Throttle' in message:
                print message
            elif 'unauthorized' in message:
                print message
            else:
                print colored('not found using linkedin', 'red'), message
        else:
            found_using_linkedin.append(email)
            # print json.dumps(info_by_email, indent=4)
        e = VerifyEmail()
        status = e.verify_email_smtp(
            email=email,
            from_host='hackerrank.com',
            from_email='help@hackerrank.com'
        )
        if e.was_found(status):
            found_using_emailahoy.append(email)
            print >> sys.stderr, colored(
                "found using emailahoy check:", 'green'), status

        elif e.not_found(status):
            print >> sys.stderr, colored(
                "not found using emailahoy check:", 'red'), status
        else:
            print >> sys.stderr, colored("unverifiable:", 'red'), status

        # is_valid = validate_email(email, verify=True)
        # if is_valid:
        # 	found_using_validate_email.append(email)
        # 	print colored('found using validate_email', 'green')
        # else:
        # 	print colored('not found using validate_email', 'red')

    print '------'
    print 'found using linkedin'
    print colored(found_using_linkedin, 'green')
    print '------'
    print 'found using emailahoy'
    print colored(found_using_emailahoy, 'green')
    print '------'
    # print 'found using validate_email'
    # print colored(found_using_validate_email, 'green')
    # print '------'
    time_taken = int(time.time() - start_time)
    minutes = time_taken/60
    seconds = time_taken % 60
    print 'finished in ' + str(minutes) + ' minute(s) and ' + str(seconds) + ' second(s).'
    return {'using_linkedin': list(set(found_using_linkedin)), 'using_emailahoy': list(set(found_using_emailahoy))}
if __name__ == '__main__':
    # info_by_email = fetch_info_by_email('saranya@venturesity.com')
    # print json.dumps(info_by_email, indent=4)
    # info_by_name = fetch_info_by_personal_details(first_name = 'saranya', last_name = 'chowdary', company_name = 'venturesity')
    # print json.dumps(info_by_name, indent=4)
    # info_by_id = fetch_info_by_id(user_id='OkcTVSsLh_')
    # print json.dumps(info_by_id, indent=4)

    # user_ids = []
    # for x in xrange(0, 7000, 25):
    # 	info_by_keywords_and_location = fetch_info_by_keywords_and_location(
    # 		keywords='cto', postal_code='560001', distance='1', start=x, count=25)
    # 	# json.dumps(info_by_keywords_and_location, indent=4)
    # 	print json.dumps(info_by_keywords_and_location, indent=4)
    # 	try:
    # 		values = info_by_keywords_and_location['people']['values']
    # 		for value in values:
    # 			user_ids.append(value['id'])
    # 	except:
    # 		for user_id in user_ids:
    # 			info_by_id = fetch_info_by_id(user_id=user_id)
    # 			first_name = info_by_id['firstName']
    # 			last_name = info_by_id['lastName']
    # 			file_name = first_name.lower().strip() + '_' + last_name.lower().strip() + '_' + user_id + '.json'
    # 			print first_name + ' ' + last_name
    # 			open('people/' + file_name, 'w').write(json.dumps(info_by_id, indent=4))
    # 		print '--------------------'
    # 		print 'done'
    # 		break
                # print user_ids
                # break
    start_time = time.time()
    emails = generate_emails_from_name_and_domain(
        name="saranya chowdary", domain="venturesity.com")
    print emails
    found_using_linkedin = []
    found_using_emailahoy = []
    # found_using_validate_email = []
    for email in emails:
        print '------'
        print 'checking ', colored(email, 'blue')
        print '------'
        info_by_email = fetch_info_by_email(email)
        if 'message' in info_by_email.keys():
            message = info_by_email['message']
            if 'Throttle' in message:
                print message
            elif 'unauthorized' in message:
                print message
            else:
                print colored('not found using linkedin', 'red'), message
        else:
            found_using_linkedin.append(email)
            # print json.dumps(info_by_email, indent=4)
        e = VerifyEmail()
        status = e.verify_email_smtp(
            email=email,
            from_host='hackerrank.com',
            from_email='help@hackerrank.com'
        )
        if e.was_found(status):
            found_using_emailahoy.append(email)
            print >> sys.stderr, colored(
                "found using emailahoy check:", 'green'), status

        elif e.not_found(status):
            print >> sys.stderr, colored(
                "not found using emailahoy check:", 'red'), status
        else:
            print >> sys.stderr, colored("unverifiable:", 'red'), status

        # is_valid = validate_email(email, verify=True)
        # if is_valid:
        # 	found_using_validate_email.append(email)
        # 	print colored('found using validate_email', 'green')
        # else:
        # 	print colored('not found using validate_email', 'red')

    print '------'
    print 'found using linkedin'
    print colored(found_using_linkedin, 'green')
    print '------'
    print 'found using emailahoy'
    print colored(found_using_emailahoy, 'green')
    print '------'
    # print 'found using validate_email'
    # print colored(found_using_validate_email, 'green')
    # print '------'
    time_taken = int(time.time() - start_time)
    minutes = time_taken/60
    seconds = time_taken % 60
    print 'finished in ' + str(minutes) + ' minute(s) and ' + str(seconds) + ' second(s).'
