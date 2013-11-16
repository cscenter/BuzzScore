#! /usr/bin/env python
# coding: utf8

from cPickle import load
from settings import APPLICATION_ROOT as root
from feature_extractor import extract_features


with open(root + '/spam/classifier_en.pkl', 'rb') as src:
    classifier_en = load(src)


def is_spam(tweet, lang):
    if lang != 'en':
        return tweet
    return 'spam' == classifier_en.classify(extract_features(tweet['text']))
