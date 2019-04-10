#!/usr/bin/env python3


import argparse
import os
import re

import seriesnaming


parser = argparse.ArgumentParser()
parser.add_argument('directory', nargs='*', default=[os.getcwd()], type=os.path.normpath)
parser.add_argument('-n', '--name', type=str, help='the series name')
parser.add_argument('-t', '--titles', action='store_true', help='fetch episode titles from the internet')
parser.add_argument('-l', '--language', choices=['en', 'fr'], default='en', help='the language to use for fetching episode titles')
args = parser.parse_args()


def script(directory, naming_helper):

	for inode in os.listdir(directory):
		
		# Get the series name if none was provided
		
		if naming_helper is None:
			if re.match('(?:season|series|saison)\s*\d+\w*', inode, re.IGNORECASE):
				parent_directory = os.path.dirname(directory)
				series_name = os.path.basename(parent_directory)
			else:
				series_name = inode
			sub_naming_helper = seriesnaming.NamingHelper(series_name, args.titles, args.language)
		else:
			sub_naming_helper = naming_helper
	
		# Here comes the Frag Dog, honey
		
		if os.path.isdir(inode):
			subdirectory = os.path.join(directory, inode)
			script(subdirectory, sub_naming_helper)
		else:
			old_filepath = os.path.join(directory, inode)
			try:
				new_filepath = sub_naming_helper.get_updated_filepath(old_filepath)
				new_filedir = os.path.normpath(os.path.dirname(new_filepath))
				print(old_filepath, '->', new_filepath)
				os.makedirs(new_filedir, exist_ok=True)
				os.rename(old_filepath, new_filepath)
			except ValueError:
				pass

			
# Launch the script

if args.name is not None:
	naming_helper = seriesnaming.NamingHelper(args.name, args.titles, args.language)
else:
	naming_helper = None

for directory in args.directory:
	script(directory, naming_helper)


