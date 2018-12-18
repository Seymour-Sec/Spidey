#!/usr/bin/env python
import argparse
import requests
from bs4 import BeautifulSoup as soup
from urllib.parse import urldefrag, urlparse, urljoin

version = '0.0.1'

discovered_urls = []

def isUnique(url):
	if url == None: return True
	return url not in discovered_urls

def recordURL(url):
		discovered_urls.append(url)
		print(f'FOUND: {url}')

def formatLink(link, parent_url):
	parsed_link = urlparse(link)
	parsed_parent_url = urlparse(urldefrag(parent_url)[0])

	#TODO -e to allow offsite crawling
	if parsed_link.netloc == parsed_parent_url.netloc or parsed_link.netloc == '':
		formated_url = urldefrag(urljoin(parent_url, link))[0]
		if formated_url != parent_url:
			return formated_url

def crawl(url, depth):
	response = requests.get(url)
	html = soup(response.text, features='html5lib')
	for a in html.find_all('a'):
		found_url = formatLink(a.get('href'), response.url)
		if found_url and depth+1<args.depth:
			if isUnique(found_url):
				recordURL(found_url)
			crawl(found_url,depth+1)

if __name__ == '__main__':
	parse = argparse.ArgumentParser(
		prog='spidey',
		description='Crwal a URL to accumulate information or create wordlists')

	parse.add_argument('-v', '--version', action='version', version=f'%(prog)s v{version}', help='prints version information')
	parse.add_argument('-u', '--url',  type=str, required=True, help='the URL to crawl')
	parse.add_argument('-d', '--depth', type=int, default=3, help='the maximum recursive depth to crawl. default: %(default)s')
	parse.add_argument('-e', '--external', action='store_true', help='allow crawling on different domains to initial URL. default: %(default)s')
	parse.add_argument('-H', '--header', type=str, help='custom headers for requets')
	parse.add_argument('-a', '--user-agent', type=str, help='a custom user agent for requets')
	parse.add_argument('-c', '--cookie', type=str, help='custom cookies for requests')
	parse.add_argument('-D', '--delay', type=int, default=100, help='crawl delay (ms). default: %(default)s')
	args = parse.parse_args()

	crawl(args.url, 0)
