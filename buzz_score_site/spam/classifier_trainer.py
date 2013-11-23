#! /usr/bin/env python
# coding: utf8

import sys
import json
import random
import cPickle

from nltk.classify import accuracy
from nltk import NaiveBayesClassifier

from feature_extractor import extract_features


def load_messages(path):
    messages = []
    with open(path, 'r') as src:
        for item in json.load(src):
            messages.extend(item.values()[0])
    return messages


def load_dataset(label, path, shuffle=False):
    messages = load_messages(path)
    if shuffle:
        random.shuffle(messages)
    return [(extract_features(msg), label) for msg in messages]


def main():
    spam = load_dataset('spam', sys.argv[1], True)
    ham = load_dataset('ham', sys.argv[2], True)
    training_spam = spam[:11500]
    training_ham = ham[:11500]
    test_spam = spam[1000:]
    test_ham = ham[1000:]

    nbc = NaiveBayesClassifier.train(training_ham + training_spam)
    cPickle.dump(nbc, sys.stdout)

    sys.stderr.writelines(['Spam accuracy: %f\n' % accuracy(nbc, test_spam),
                           'Ham accuracy: %f\n' % accuracy(nbc, test_ham)])


if __name__ == '__main__':
    main()
