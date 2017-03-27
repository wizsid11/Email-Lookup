import sys
import re
import itertools

def generate_emails_from_name_and_domain(name, domain):
	parts = re.sub(r' +', ' ', name).lower().split(' ')
	if len(parts) == 1:
		return generate_emails_parent(first=parts[0], domain=domain)
	elif len(parts) == 2:
		return generate_emails_parent(
			first=parts[0], second=parts[1], domain=domain)
	elif len(parts) == 3:
		return generate_emails_parent(
			first=parts[0], second=parts[1], third=parts[2], domain=domain)
	else:
		raise Exception('names can be of type "a", "a b" and "a b c" only.')


def generate_emails_parent(domain, first, second=None, third=None):
	at='@'
	if second is None and third is None:
		l = [first + at + domain, first[0] + at + domain]
		return l
	elif third is None:
		l = generate_emails(at, domain, first, second)
		return l
	else:
		l = generate_emails(at, domain, first, second, third)
		return l


def generate_emails(at, domain, first, second, third=None):
	if third is not None:
		l1 = generate_emails(at, domain, first, second)
		l2 = generate_emails(at, domain, first, third)
		l3 = generate_emails(at, domain, second, third)
		l = []

		obj = {
			'a': first,
			'b': second,
			'ak': first[0],
			'bl': second[0],
			'c': third,
			'cm': third[0],
			'dt': '.',
			'no': '',
			'un': '_'
		}
		for x in l1:
			for y in ['c', 'cm']:
				for z in ['dt', 'no', 'un']:
					ltemp = ''
					ltemp = ltemp + obj[y]
					ltemp = ltemp + obj[z]

					for token in x:
						ltemp = ltemp + token
					l.append(ltemp)
		for x in l2:
			for y in ['b', 'bl']:
				for z in ['dt', 'no', 'un']:
					ltemp = ''
					ltemp = ltemp + obj[y]
					ltemp = ltemp + obj[z]

					for token in x:
						ltemp = ltemp + token
					l.append(ltemp)
		for x in l3:
			for y in ['a', 'ak']:
				for z in ['dt', 'no', 'un']:
					ltemp = ''
					ltemp = ltemp + obj[y]
					ltemp = ltemp + obj[z]

					for token in x:
						ltemp = ltemp + token
					l.append(ltemp)
		for x in ['a', 'ak', 'b', 'bl', 'c', 'cm']:
			l.append(obj[x] + at + domain)
		return l

	else:
		l1 = []
		addTo(l1, permutations(['a', 'b']))
		addTo(l1, permutations(['a', 'bl']))
		addTo(l1, permutations(['ak', 'b']))
		addTo(l1, permutations(['ak', 'bl']))
		l2 = []
		for x in ['dt', 'no', 'un']:
			for y in l1:
				ltemp = []
				ltemp.append(y[0])
				ltemp.append(x)
				ltemp.append(y[1])
				l2.append(ltemp)
		for x in ['a', 'ak', 'b', 'bl']:
			l2.append([x])
		obj = {
			'a': first,
			'b': second,
			'ak': first[0],
			'bl': second[0],
			'dt': '.',
			'no': '',
			'un': '_'
		}
		r = []
		for x in l2:
			rtemp = ''
			for token in x:
				rtemp = rtemp + obj[token]
			rtemp = rtemp + at + domain
			r.append(rtemp)
		return r


def permutations(items):
	l = []
	l_iter = itertools.permutations(items)
	for x in l_iter:
		ltemp = []
		for y in x:
			ltemp.append(y)
		l.append(ltemp)
	return l


def addTo(l, items):
	for x in items:
		l.append(x)

if __name__ == '__main__':
	print generate_emails_from_name_and_domain(name="saranya chowdary", domain="venturesity.com")
