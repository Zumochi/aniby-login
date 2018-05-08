#!/usr/bin/python3
"""Animebytes Login

Usage:
    aniby-login.py (-f | --file) FILE
    aniby-login.py (-h | --help)
    aniby-login.py --version
Options:
    -f --file   Path to yaml file containing username/password
    -h --help   Show this help
    --version   Show version

"""
from docopt import docopt
import sys
from logging import error, info, warning
import requests
from bs4 import BeautifulSoup
import yaml

VERSION = '0.0.1'
ANIBY_URL = 'https://animebytes.tv'
REQ_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
REQ_HOST = 'animebytes.tv'

REQ_HEADERS = {
    'User-Agent':   REQ_AGENT,
    'Host':         REQ_HOST,
}


session = requests.Session()


def get_auth_info(auth_file):
    try:
        with open(arguments['FILE'], 'r') as auth_file:
            try:
                auth_data = yaml.safe_load(auth_file)
                if not auth_data:
                    error("Authentication file empty!")
                    sys.exit(1)
                username = auth_data['username']
                password = auth_data['password']
            except yaml.YAMLError as ymlerr:
                error('Loading yaml authentication file failed: {ymlerr}'.format(ymlerr=ymlerr))
                sys.exit(1)
    except EnvironmentError as ee:
        error("Couldn't load authentication file {auth_file}".format(auth_file=auth_file))
        sys.exit(1)

    return {
        'username': username,
        'password': password,
    }


def get_csrf_data(html):
    soup = BeautifulSoup(html)
    csrf_index = soup.find('input', type='hidden', name='_CSRF_INDEX')
    csrf_token = soup.find('input', type='hidden', name='_CSRF_TOKEN')
    print()


def aniby_login(auth_info):
    req_url = ANIBY_URL + '/user/login'
    req_aniby_login_page = session.get(req_url, headers=REQ_HEADERS)
    print(req_aniby_login_page.url)
    print('Headers')
    print(req_aniby_login_page.headers)
    print('Cookies')
    print(req_aniby_login_page.cookies)

    csrf_index = False
    csrf_token = False

    REQ_HEADERS['Referer'] = ANIBY_URL

    REQ_COOKIES = {
        '__cfduid': req_aniby_login_page.cookies['__cfduid'],
        'transient': req_aniby_login_page.cookies['transient'],
    }
    REQ_PARAMS = {
        'username': auth_info['username'],
        'password': auth_info['password'],
        'login':    'Log+In!',
        '_CSRF_INDEX':  csrf_index,
        '_CSRF_TOKEN':  csrf_token,
    }


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Animebytes Login {version}'.format(help=True, version=VERSION))
    auth_info = get_auth_info(arguments['FILE'])

    aniby_login(auth_info)
