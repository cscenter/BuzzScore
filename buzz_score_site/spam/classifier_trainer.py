#! /usr/bin/env python
# coding: utf8

import json
import random
import cPickle
import itertools

from nltk import classify
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
    src_dir = '../../data_set/spam_analysis/en/'

    spam = load_dataset('spam', src_dir + 'spam.json', True)
    ham = load_dataset('ham', src_dir + 'ham.json', True)
    training_spam = spam[:11500]
    training_ham = ham[:11500]
    test_spam = spam[1000:]
    test_ham = ham[1000:]

    classifier = NaiveBayesClassifier.train(training_ham + training_spam)

    with open('classifier_en.pkl', 'wb') as dst:
        cPickle.dump(classifier, dst)

    print 'Test Spam accuracy: %f' % classify.accuracy(classifier, test_spam)
    print 'Test Ham accuracy: %f' % classify.accuracy(classifier, test_ham)
    print classifier.show_most_informative_features(20)


if __name__ == '__main__':
    main()
