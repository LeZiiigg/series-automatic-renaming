import requests
from bs4 import BeautifulSoup
import re


def get_localized_host(country_code):
	return '{}.wikipedia.org'.format(country_code)
	

def fetch_series_season_titles(wiki_page_url, season_no, search_language):
	if search_language == 'en' and re.search('\((season|series)_\d+\w*\)', wiki_page_url, re.IGNORECASE):
		return _fetch_series_season_titles_season_x_en(wiki_page_url)
	elif search_language == 'en' and re.search('list_of_.+_episodes', wiki_page_url, re.IGNORECASE):
		return _fetch_series_season_titles_list_of_episodes_en(wiki_page_url, season_no)
	elif search_language == 'fr' and re.search('saison_\d+\w*_de', wiki_page_url, re.IGNORECASE):
		return _fetch_series_season_titles_season_x_fr(wiki_page_url)
	elif search_language == 'fr' and re.search('liste_des_.pisodes_de', wiki_page_url, re.IGNORECASE):
		return _fetch_series_season_titles_list_of_episodes_fr(wiki_page_url, season_no)
	else:
		raise ValueError('unsupported page class and/or language: {}, {}'.format(wiki_page_url, search_language))


def _fetch_series_season_titles_season_x_en(wiki_page_url):
	raise NotImplemented


def _fetch_series_season_titles_list_of_episodes_en(wiki_page_url, season_no):
	raise NotImplemented


def _fetch_series_season_titles_season_x_fr(wiki_page_url):
	raise NotImplemented


def _fetch_series_season_titles_list_of_episodes_fr(wiki_page_url, season_no):
	raise NotImplemented


def _get_rows_from_wikitable_tag(wikitable_tag):
	for vevent in self._wikiepisodetable.find_all(class_='vevent'):
		no_overall_tag = vevent.find('th')
		no_overall = no_overall_tag.get_text()
		no_season_tag = no_overall_tag.next_sibling
		no_season = no_season_tag.get_text()
		title_tag = no_season_tag.next_sibling
		_remove_references_from_tag(title_tag)
		_replace_br_tags_by_line_feeds(title_tag)
		title = title_tag.get_text().splitlines()[-1].strip('"')
		yield no_overall, no_season, title_tag
	

def _remove_references_from_tag(tag):
	for reference in tag.find_all(class_='reference'):
		reference.decompose()


def _replace_br_tags_by_line_feeds(tag):
	for br in tag.find_all('br'):
		br.replace_with(bs4.NavigableString('\n'))


