#! /usr/bin/env python
# coding: utf8

import os
from cPickle import load
from settings import CLASSIFIER_ROOT as ROOT
from feature_extractor import extract_features


with open(os.path.join(ROOT, 'spam_classifier_en.pkl'), 'rb') as src:
    CLASSIFIER_EN = load(src)


def is_spam(tweet, lang):
    if lang != 'en':
        return False
    return 'spam' == CLASSIFIER_EN.classify(extract_features(tweet['text']))
