#!/usr/bin/env python3

import sys
import os
import re
import subprocess
from argparse import ArgumentParser
from pprint import pprint

import wikiepisodetable

# Parse the arguments list

parser = ArgumentParser()
parser.add_argument('directory', nargs = '*', default = os.getcwd(), type = os.path.normpath)
parser.add_argument('-n', '--name', type = str, help = 'the series name')
parser.add_argument('-w', '--wiki', type = str, help = 'the wikipedia url from where to get the episodes names')
args = parser.parse_args()

# Parse the wikipedia URL

table = args.wiki and wikiepisodetable.parse(args.wiki)
if table:
	pprint(table)
	answer = input('Use those episode titles? [y/N] ')
	if not answer or not (answer.lower() in ['y', 'yes']):
		table = None					# Invalidate the titles table

# Main script

def script(directory, name = None):

	if isinstance(directory, list):
		if len(directory) > 1:			# Call the script for each separate directory
			for entry in directory:
				script(entry)
			return
		else:							# Cast the list into its first and single element
			directory = directory[0]

	# Get the series name if none was provided

	if not name:						
		name = os.path.basename(directory)

	# Here comes the Frag Dog, honey

	for entry in sorted(os.listdir(directory)):
		path = os.path.join(directory, entry)
		if os.path.isdir(path):			# Call the script recursively for each subdirectory
			script(path, name)
		else:
			m = re.match('^.*s(?P<season>\d+)e(?P<episode>\d+).*\.(?P<extension>\w+)$', entry, re.IGNORECASE)
			if m:
				season = int(m.group('season'))
				episode = int(m.group('episode'))
				extension = m.group('extension')
				title = None
				if table and (season in table):
					if not episode in table[season]:
						offset = episode - min(table[season].keys())
						table[season] = {i + offset: table[season][i] for i in table[season].keys()}
					title = table[season][episode]
				elif table and not (2 in table):
					title = table[1][episode]
				if title:
					title = re.sub('(<|>|:|"|/|\\\|\||\?|\*)', '_', title)
				
				filename = '{} S{:02}E{:02}{}.{}'.format(name, season, episode, title and (' ' + title) or '', extension)
				try:
					os.rename(path, os.path.join(directory, filename))
				except OSError:
					sys.stderr.write("invalid name: '{}'\n".format(filename))

# Launch the script

script(args.directory, args.name)
