#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import sys
from bs4 import BeautifulSoup

# Parse arguments
if len(sys.argv) > 1:
	if sys.argv[1] is not None:
		baseURL = sys.argv[1]
else:
	# Print usage if no arguments given
	print("Usage: kijiji-mapper.py [Starting URL] [number of pages]\n" + "Example: kijiji-mapper.py \"http://www.kijiji.ca/b-garage-sale-yard-sale/ottawa/c638l1700185\" 5 \n" + "\n Since no URL specified, using default (Ottawa garage sales):\n")
	baseURL = "http://www.kijiji.ca/b-garage-sale-yard-sale/ottawa/c638l1700185"
if len(sys.argv) > 2:
	if sys.argv[2] is not None:
		pageLimit = int(sys.argv[2])
else:
	pageLimit = 15


content = urllib2.urlopen(baseURL)
soup = BeautifulSoup(content, from_encoding=content.info().getparam('charset'))
i = 1

while i < pageLimit:
    # Get all the addresses
    for link in soup.find_all('a'):
        linkURL = link.get('href')
        if (re.match("^/v-", str(linkURL)) is not None and re.match(".*topAdSearch$", str(linkURL)) is None):
            newLinkURL = linkURL = 'http://www.kijiji.ca' + str(link.get('href'))
            linkContent = urllib2.urlopen(newLinkURL)
    #        print(newLinkURL)
            linkSoup = BeautifulSoup(linkContent, from_encoding=linkContent.info().getparam('charset'))
            for td in linkSoup.find_all('td'):
                tdText = td.get_text()
                if re.search("[A-Z][0-9][A-Z] [0-9][A-Z][0-9]", unicode(tdText)) is not None:
                    print(tdText.encode('utf8', 'replace').split("\n")[0])   
    # Define the next page           
    i += 1
    nextPage = 'page-' + str(i)
    # Scrape for the next page link
    for nextLink in soup.find_all('a'):
        linkURL = nextLink.get('href')
        if re.search(nextPage, str(linkURL)) is not None:
            baseURL = 'http://www.kijiji.ca' + linkURL    
    content = urllib2.urlopen(baseURL)
    soup = BeautifulSoup(content, from_encoding=content.info().getparam('charset'))
    
    

        
        
    