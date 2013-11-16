#! /usr/bin/env python
# coding: utf8

import re
from nltk import clean_html
from nltk.corpus import stopwords as sw
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize


stopwords = sw.words('english')
stopwords.extend(['ll', 've'])

at_re = re.compile(r'@\w+?')
link_re = re.compile(r'<a.*?>.*?</a>')
entity_re = re.compile(r'&[a-z]+|(?:#\d+);')

url_re = re.compile(r'(?i)(?:https?://)?(?:www.)?'
                    r'(?:(?:[a-z0-9-]+\.)+[a-z]{2,6})'
                    r'/?\S*')

lemmatizer = WordNetLemmatizer()


def extract_features(msg):
    msg = clean_html(link_re.sub('', msg))

    msg = url_re.sub('', msg)
    msg = at_re.sub('', msg)
    msg = entity_re.sub('', msg).lower()

    words = set(wordpunct_tokenize(msg)).difference(stopwords)
    words = filter(lambda w: w.isalpha() and len(w) > 1, words)

    return dict((lemmatizer.lemmatize(w), True) for w in words)


if __name__ == '__main__':
    pass
