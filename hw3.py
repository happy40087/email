#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/rscrape1.py
# Recursive scraper built using the Requests library.

import argparse, requests
from urllib.parse import urljoin, urlsplit
from lxml import etree
import urllib,re

def GET(url):
	response = requests.get(url)
	if response.headers.get('Content-Type', '').split(';')[0] != 'text/html':
		return
	text = response.text
	try:
		html = etree.HTML(text)
	except Exception as e:
		print('	   {}: {}'.format(e.__class__.__name__, e))
		return
	links = html.findall('.//a[@href]')
	for link in links:
		yield GET, urljoin(url, link.attrib['href'])

def scrape(start, url_filter):
	further_work = {start}
	already_seen = {start}
	
	i=1
	while further_work:
		call_tuple = further_work.pop()
		function, url, *etc = call_tuple
		print(i,function.__name__, url, *etc)
		
		try:
			response = requests.get(url)
			text = response.text 
			print('\033[32m')
			print(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",text))			
			print('\033[0m\n')	
		except urllib.error.HTTPError as e:
			print(e.code)
			print(e.msg)
			print('\n')
		
		for call_tuple in function(url, *etc):
		
			if call_tuple in already_seen:
				continue
			already_seen.add(call_tuple)
			function, url, *etc = call_tuple
			if not url_filter(url):
				continue
			further_work.add(call_tuple)
		if i>=20:
			break
		i=i+1
def main(GET):
	parser = argparse.ArgumentParser(description='Scrape a simple site.')
	parser.add_argument('url', help='the URL at which to begin')
	start_url = parser.parse_args().url
	starting_netloc = urlsplit(start_url).netloc
	url_filter = (lambda url: urlsplit(url).netloc == starting_netloc)
	scrape((GET, start_url), url_filter)

if __name__ == '__main__':
	main(GET)
