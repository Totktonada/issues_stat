#!/usr/bin/env python

from __future__ import print_function

import os
import re
import sys
import argparse
import requests


def status(pages, pages_all, issues, url):
    print('[pages {:2} / {:2}] [issues {:4} / ??] Downloading {}'.format(
          pages, pages_all, issues, url), file=sys.stderr)


parser = argparse.ArgumentParser(description='Show open issues statistics')
parser.add_argument('repo_path', type=str, help='owner/repository')
args = parser.parse_args()
if '/' not in args.repo_path:
    raise ValueError('repo_path must be in the form owner/repository')
owner, repo = args.repo_path.split('/', 1)

token_file = 'token.txt'
if not os.path.exists(token_file):
    raise RuntimeError('{file} is not exists'.format(file=token_file))
if not os.path.isfile(token_file):
    raise RuntimeError('{file} is not a regular file'.format(file=token_file))
with open(token_file, 'r') as f:
    token = f.read().strip()

session = requests.Session()
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': 'token ' + token,
}
params = {
    'state': 'open',
    'per_page': 100,
}
url = 'https://api.github.com/repos/{}/{}/issues'.format(owner, repo)
status(0, '??', 0, url)
r = session.get(url, headers=headers, params=params)
r.raise_for_status()

data = []
data.extend(r.json())

# > The link header will be omitted if the endpoint does not support pagination
# > or *if all results fit on a single page.*
#
# https://docs.github.com/en/rest/guides/using-pagination-in-the-rest-api?apiVersion=2022-11-28
if r.links:
    pages_all_str = '??'
    last_url = r.links['last']['url']
    pages_all_match = re.search(r'[^_]page=(\d+)', last_url)
    if pages_all_match:
        pages_all_str = pages_all_match.group(1)

    pages = 1
    while 'next' in r.links:
        next_url = r.links['next']['url']
        status(pages, pages_all_str, len(data), next_url)
        r = session.get(next_url, headers=headers)
        r.raise_for_status()
        data.extend(r.json())
        pages += 1

label_stat = {}
max_label_len = 0

for issue in data:
    if 'pull_request' in issue:
        continue
    for label_dict in issue['labels']:
        label = label_dict['name']
        if label not in label_stat:
            label_stat[label] = 0
        label_stat[label] += 1

        label_len = len(label)
        if label_len > max_label_len:
            max_label_len = label_len

for label in sorted(label_stat, key=label_stat.get):
    print('{label:{width}} {count}'.format(width=max_label_len + 1,
                                           label=label,
                                           count=label_stat[label]))
