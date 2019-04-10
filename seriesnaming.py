import os
import re
import warnings

import google
import wikipedia


class NamingHelper:

	def __init__(self, series_name, titles_enabled, titles_language):
		self.series_name = series_name
		self.titles_enabled = titles_enabled
		self.titles_language = titles_language
		self._season_titles_cache = {}
	
	def get_updated_filepath(self, old_filepath):
		season_no, eps_no, eps_title, file_ext = self._parse_filepath(old_filepath)
		if self.titles_enabled:
			updated_eps_title = self._fetch_episode_title(season_no, eps_no)
			if updated_eps_title is not None:
				eps_title = updated_eps_title
		else:
			eps_title = None
		filedir = os.path.dirname(old_filepath)
		return self._build_filepath(filedir, season_no, eps_no, eps_title, file_ext)
	
	def _parse_filepath(self, filepath):
		match = re.search('S(?P<season_no>\d+)\s*E(?P<eps_no>\d+)(?P<junk>.*?)\.(?P<file_ext>\w+)$', filepath, re.IGNORECASE)
		if match is None:
			raise ValueError(filepath)
		season_no = match.group('season_no').lstrip('0')
		eps_no = match.group('eps_no').lstrip('0')
		if ' ' in match.group('junk'):
			eps_title = match.group('junk').strip(' ')
		else:
			eps_title = None
		file_ext = match.group('file_ext')
		return season_no, eps_no, eps_title, file_ext

	def _fetch_episode_title(self, season_no, eps_no):
		if not season_no in self._season_titles_cache:
			self._season_titles_cache[season_no] = dict(
				google.fetch_series_season_titles(self.series_name, season_no, self.titles_language))
		if season_no in self._season_titles_cache:
			if eps_no in self._season_titles_cache[season_no]:
				return self._season_titles_cache[season_no][eps_no]
			else:
				warnings.warn('no title available for episode: {}.{}.{}'.format(
					self.series_name,
					season_no,
					eps_no))
		return None
	
	def _build_filepath(self, filedir, season_no, eps_no, eps_title, file_ext):
		if eps_title is not None:
			eps_title = re.sub('(<|>|:|"|/|\\\|\||\?|\*)', '_', eps_title)
		filename = '{} S{:>02s}E{:>02s}{}.{}'.format(
			self.series_name,
			season_no,
			eps_no,
			' ' + eps_title if eps_title is not None else '',
			file_ext)
		return os.path.join(filedir, filename)
	
	
