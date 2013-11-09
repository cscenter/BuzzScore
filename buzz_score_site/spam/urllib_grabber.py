#! /usr/bin/env python

import re
import sys
import json
from urllib import urlopen
from itertools import izip
from contextlib import closing


msg_re = re.compile('<div class="tweet-text".*?><div.*?>(.*?)</div></div>')
lnk_re = re.compile('<div class="w-button-more"><a href="(.*?)">')

def get_messages(username, max_number=None, recursive=True):
    '''Returns list containing last messages of <username> (with retweets)'''
    messages = []
    url = 'http://mobile.twitter.com/%s' % username
    while not max_number or len(messages) < max_number:
        with closing(urlopen(url)) as page:
            html = page.read()
        messages.extend(msg_re.findall(html))
        lnk = lnk_re.findall(html)
        url = lnk[0] if lnk else ''
        if not recursive or not url:
            break
    return messages[:max_number]

def main():
    usernames = [un.strip() for un in sys.stdin]
    max_number = int(sys.argv[1]) if len(sys.argv) == 2 else None
    messages = (get_messages(un, max_number) for un in usernames)
    json_data = [{un: msg} for un, msg in izip(usernames, messages) if msg]
    json.dump(json_data, sys.stdout,
              sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    main()
