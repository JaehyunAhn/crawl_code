# encoding: utf-8
__desc__ = 'basic beautifulsoup function'
__author__ = 'sogo'

from bs4 import BeautifulSoup
import requests
import configparser

def get_bs_object(url, session_=None):
    """
    get bs object
    :param url:
    :return: bs obj
    """
    # general settings
    _headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.44 Safari/534.7',
    }
    # get random session
    if session_ is None:
        session = requests.Session()
    else:
        session = session_

    # get beautifulSoup object
    r = session.get(url, headers=_headers)
    # encoding problem (solved) : http://pythonstudy.xyz/python/article/403-%ED%8C%8C%EC%9D%B4%EC%8D%AC-Web-Scraping
    r.raise_for_status()
    r.encoding = None

    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    return soup

def read_config(file_location=None):
    """
    try to read './settings.cfg' configuration file
    :return: if Yes returns a dict, if not returns empty dict
    """
    _file_location = './settings.cfg'
    if file_location:
        _file_location = file_location
    config = configparser.ConfigParser()
    try:
        # read file
        config.read(_file_location)
        _return_dict = {
            'prefix': config.get('SITE_INFO', '_prefix'),
            'save_file_prefix': config.get('SITE_INFO', '_save_file_prefix'),
            'test1': config.get('TEST_LINK', '_cno_url'),
            'test2': config.get('TEST_LINK', '_article_url')
        }
        print()
        return _return_dict
    except configparser.NoSectionError:
        print('[ERROR] No section Error in {}'.format(_file_location))
        return {}

def chunks(list_, size):
    _return_list = []
    for i in range(0, len(list_), size):
        _return_list.append(list_[i:i + size])
    return _return_list

if __name__ == '__main__':
    read_config()