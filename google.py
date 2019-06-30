import requests
from bs4 import BeautifulSoup
import re


def get_localized_host(country_code):
	return 'www.google.com'


def search(search_string, search_language):

	search_string_formatted = search_string.replace(' ', '+')
	query_url = 'https://{}/search?q={}&ie=utf-8&oe=utf-8&hl={}'.format(
		get_localized_host(search_language),
		search_string_formatted,
		search_language)
	query_result = requests.get(query_url)
	soup = BeautifulSoup(query_result.text, 'html.parser')
	
	for g in soup.find(id='search').find_all(class_='g'):
		r = g.find(class_='r')
		if r is None:
			continue
		a = r.find('a', href=True)
		if a is None:
			raise ValueError(repr(r))
		result_title = a.get_text()
		result_url = re.search('[a-z]+://[^&]*', a['href']).group()
		result_url = re.sub('%25', '%', result_url)
		yield result_title, result_url
	

def fetch_series_season_titles(series_name, season_no, search_language):

	if search_language == 'en':
		search_string = 'season {} of {}'.format(season_no, series_name)
	else:
		ValueError("language '{}' not supported".format(search_language))
		
	search_string_formatted = search_string.replace(' ', '+')
	query_url = 'https://{}/search?q={}&ie=utf-8&oe=utf-8&hl={}'.format(
		get_localized_host(search_language),
		search_string_formatted,
		search_language)
	query_result = requests.get(query_url)
	soup = BeautifulSoup(query_result.text, 'html.parser')
	
	eps_re = re.compile('^S(?P<season_no>\d+\w*)\s*E(?P<eps_no>\d+\w*)\W*(?P<eps_title>.*)\Z', re.IGNORECASE)
	for text in soup.find_all(text=eps_re):
		match = eps_re.match(text)
		eps_no = match.group('eps_no').lstrip('0')
		eps_title = match.group('eps_title')
		yield eps_no, eps_title


