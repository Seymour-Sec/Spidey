#!/usr/bin/env python
import argparse
import requests
from time import sleep
from bs4 import BeautifulSoup as soup
from urllib.parse import urldefrag, urlparse, urljoin

version = '0.0.1'
done = []
work = []

def banner():
	print('''\033[1m\033[95m    ____     _    __
   / __/__  (_)__/ /__ __ __
  _\ \/ _ \/ / _  / -_) // /
 /___/ .__/_/\_,_/\__/\_, /
    /_/              /___/
 Multi Purpose Web Crawler
\033[0m\033[95m by @Seymour_Sec
\033[0m''')

def formatLink(link, parent_url):
	parsed_link = urlparse(link)
	parsed_parent_url = urlparse(urldefrag(parent_url)[0])

	#TODO -e to allow offsite crawling
	if parsed_link.netloc == parsed_parent_url.netloc or parsed_link.netloc == '':
		formated_url = urldefrag(urljoin(parent_url, link))[0]
		if formated_url != parent_url:
			return formated_url

def crawl():
	for url in work:
		response = requests.get(url)
		html = soup(response.text, features='html5lib')
		for a in html.find_all('a'):
			found_url = formatLink(a.get('href'), response.url)
			if found_url and found_url not in done and found_url not in work:
				work.append(found_url)
				print(found_url)
		sleep(args.delay/1000)

if __name__ == '__main__':
	parse = argparse.ArgumentParser(
		prog='spidey',
		description='Crwal a URL to accumulate information or create wordlists')

	parse.add_argument('-v', '--version', action='version', version=f'%(prog)s v{version}', help='prints version information')
	parse.add_argument('-u', '--url',  type=str, required=True, help='the URL to crawl')
	parse.add_argument('-d', '--depth', type=int, default=3, help='the maximum recursive depth. default: %(default)s')
	parse.add_argument('-e', '--external', action='store_true', help='allow crawling on other domains. default: %(default)s')
	parse.add_argument('-H', '--header', type=str, help='custom headers for requets')
	parse.add_argument('-a', '--user-agent', type=str, help='a custom user agent for requets')
	parse.add_argument('-c', '--cookie', type=str, help='custom cookies for requests')
	parse.add_argument('-D', '--delay', type=int, default=100, help='crawl delay (ms). default: %(default)s')

	banner()
	args = parse.parse_args()
	print(args.url)
	work.append(args.url)
	crawl()
