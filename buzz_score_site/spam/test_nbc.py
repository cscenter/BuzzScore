#! /usr/bin/env python


import re
import json
import cPickle
import itertools
import time

from nltk import classify
from nltk import clean_html
from nltk import NaiveBayesClassifier

from nltk.corpus import stopwords as sw
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize


def load_messages(path, number):
    with open(path, 'r') as src:
        j = json.load(src)
    messages = []
    for item in j:
        messages.extend(item.values()[0])
    return messages[:number]


stopwords = sw.words('english')
stopwords.extend(['ll', 've'])

link_re = re.compile(r'<a.*?>.*?</a>')
url_re = re.compile(r'(?i)(?:https?://)?(?:www.)?'
                    r'(?:(?:[a-z0-9-]+\.)+[a-z]{2,6})'
                    r'/?\S*')
at_re = re.compile(r'@\w+?')
entity_re = re.compile(r'&[a-z]+|(?:#\d+);')

wnl = WordNetLemmatizer()

def prepare_message(msg):
    msg = clean_html(link_re.sub('', msg))
    msg = url_re.sub('', msg)
    msg = at_re.sub('', msg)
    msg = entity_re.sub('', msg).lower()
    words = set(wordpunct_tokenize(msg)).difference(stopwords)
    words = filter(lambda w: w.isalpha() and len(w) > 1, words)
    return dict((wnl.lemmatize(w), True) for w in words)


def load_dataset(label, path, number):
    return [(prepare_message(msg), label)
            for msg in load_messages(path, number)]


def main():
    wd = '../../data_set/spam_analysis/en/'

    t = time.time()
    training_spam = load_dataset('spam', wd + 'spam.json', 9000)
    training_ham = load_dataset('ham', wd + 'ham.json', 9000)
    test_spam = load_dataset('spam', wd + 'spam.json', 13000)[4000:]
    test_ham = load_dataset('ham', wd + 'ham.json', 13000)[4000:]
    print 'Datasets loading: %f s' % (time.time() - t)

    t = time.time()
    nbc = NaiveBayesClassifier.train(training_ham + training_spam)
    print 'Training: %f s' % (time.time() - t)

    t = time.time()
    with open('nbc.pkl', 'wb') as dst:
        cPickle.dump(nbc, dst)
    print 'NBC dumping: %f s' % (time.time() - t)

    t = time.time()
    with open('nbc.pkl', 'rb') as src:
        nbc = cPickle.load(src)
    print 'NBC loading: %f s' % (time.time() - t)
    print

    print 'Test Spam accuracy: %f' % classify.accuracy(nbc, test_spam)
    print 'Test Ham accuracy: %f' % classify.accuracy(nbc, test_ham)
    print nbc.show_most_informative_features(20)


if __name__ == '__main__':
    main()
