#! /usr/bin/env python
# coding: utf8

import re
from nltk import clean_html
from nltk.corpus import stopwords as sw
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize


STOPWORDS = sw.words('english')
STOPWORDS_EXTENSION = ['ll', 've']
STOPWORDS.extend(STOPWORDS_EXTENSION)

USERNAME_RE = re.compile(r'@\w+?')
HTML_LINK_RE = re.compile(r'<a.*?>.*?</a>')
ENTITY_RE = re.compile(r'&[a-z]+|(?:#\d+);')

RAW_URL_RE = re.compile(r'(?i)(?:https?://)?(?:www.)?'
                        r'(?:(?:[a-z0-9-]+\.)+[a-z]{2,6})'
                        r'/?\S*')


def extract_features(message):
    message = clean_html(HTML_LINK_RE.sub('', message))

    message = RAW_URL_RE.sub('', message)
    message = USERNAME_RE.sub('', message)
    message = ENTITY_RE.sub('', message).lower()

    words = set(wordpunct_tokenize(message)).difference(STOPWORDS)
    words = filter(lambda w: w.isalpha() and len(w) > 1, words)

    return dict((WordNetLemmatizer().lemmatize(w), True) for w in words)
