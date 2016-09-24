#!/usr/local/bin/python3

import re
import requests
from bs4 import BeautifulSoup

def parse(url):
	# Upload the given URL

	soup = BeautifulSoup(requests.get(url).content, "html.parser")

	# Create a two-dimensionnal array containing the episodes titles

	l, i = {}, 0

	# Try to find a wikiepisodetable (mainly for english pages)

	tables = soup.find_all("table", "wikitable plainrowheaders wikiepisodetable")
	if len(tables) > 0:
		for i, table in enumerate(tables):
			l[i+1] = {}
			for j, summary in enumerate(table.find_all("td", "summary")):
				l[i+1][j+1] = summary.get_text().strip('\'\"') # TODO: Strip the [...]
		return l

	# Try to find in the header, a non empty list having the string "episode" in its name

	toc = soup.find("div", "toc")
	for section in toc.find_all("li", "toclevel-1"):
		if re.search("\wpisode", section.a.get_text(), re.IGNORECASE | re.UNICODE):
			items = section.find_all("li")
			if len(items) > 0:
				l[i+1] = {}
				for j, item in enumerate(items):
					if not re.search("(series|season|saison)", item.get_text(), re.IGNORECASE | re.UNICODE):
						if item.find("i"):
							l[i+1][j+1] = item.find("i").get_text().strip('\'\"')
						else:
							l[i+1][j+1] = ''
					else:
						l.pop(i+1)
						break
				if i+1 in l:
					i += 1
	if l:
		return l

	# Try to find a list with no class attribute

	tables = soup.find_all("ol", attrs = {'class': None})
	if len(tables) > 0:
		for i, table in enumerate(tables):
			l[i+1] = {}
			for j, li in enumerate(table.find_all("li")):
				l[i+1][j+1] = li.get_text().strip('\'\"') # TODO: Strip the (...)
		return l