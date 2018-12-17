#!/usr/bin/env python
import argparse

version = '0.0.1'

if __name__ == '__main__':
	parse = argparse.ArgumentParser(
		prog='spidey',
		description='Crwal a URL to accumulate information or create wordlists')

	parse.add_argument('-v', '--version', action='version', version=f'%(prog)s v{version}', help='prints version information')
	parse.add_argument('-u', '--url',  required=True, help='the URL to crawl')
	parse.add_argument('-d', '--depth', type=int, default=3, help='the maximum recursive depth to crawl. default: %(default)s')
	parse.add_argument('-e', '--external', default=False, help='crawl sites on a different domain to initial target. default: %(default)s')
	parse.add_argument('-H', '--header', help='a custom header for requets')
	parse.add_argument('-a', '--user-agent', help='a custom user agent for requets')
	parse.add_argument('-c', '--cookie', help='custom cookies for requests')
	parse.add_argument('-D', '--delay', type=int, default=100, help='crawl delay. default: %(default)sms')
	args = parse.parse_args()
	print(args)
