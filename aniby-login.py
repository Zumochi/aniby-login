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

HEADERS = {
    'User-Agent': REQ_AGENT,
    'Host': REQ_HOST,
}

session = requests.Session()


def get_auth_info(auth_file):
    try:
        with open(auth_file, 'r') as f:
            try:
                auth_data = yaml.safe_load(f)
                if not auth_data:
                    error("Authentication file empty!")
                    sys.exit(1)
                return auth_data
            except yaml.YAMLError as ymlerr:
                error('Loading yaml authentication file failed: {ymlerr}'.format(ymlerr=ymlerr))
                sys.exit(1)
    except EnvironmentError as ee:
        error("Couldn't load authentication file {filename}: {error}".format(filename=ee.filename, error=ee.strerror))
        sys.exit(1)


def get_csrf_data(html):
    soup = BeautifulSoup(html, 'lxml')
    token = soup.find('input', {'name': '_CSRF_TOKEN'})
    index = soup.find('input', {'name': '_CSRF_INDEX'})

    return {'token': token['value'], 'index': index['value']}


def aniby_login(auth):
    prv_url = ANIBY_URL
    req_url = ANIBY_URL + '/user/login'
    req_aniby_login_page = session.get(req_url, headers=HEADERS)
    csrf_data = get_csrf_data(req_aniby_login_page.content)

    req_headers = HEADERS
    req_headers['Referer'] = prv_url

    req_params = {'username': auth['username'],
                  'password': auth['password'],
                  'login': 'Log+In!',
                  '_CSRF_INDEX': csrf_data['index'],
                  '_CSRF_TOKEN': csrf_data['token']}
    req_cookies = {'__cfduid': req_aniby_login_page.cookies['__cfduid'],
                   'transient': req_aniby_login_page.cookies['transient']}

    post_login = session.post(req_url, data=req_params, headers=req_headers)
    print(post_login.text)
    print(post_login.status_code)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Animebytes Login {version}'.format(help=True, version=VERSION))
    auth_info = get_auth_info(arguments['FILE'])

    aniby_login(auth_info)
