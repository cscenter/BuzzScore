#! /usr/bin/env python


import re
import json
import itertools
from nltk import classify
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier
from nltk.tokenize import wordpunct_tokenize


def load_messages(path, number):
    with open(path, 'r') as f:
        j = json.load(f)
        messages = []
        for item in j:
            messages.extend(item.values()[0])
        return messages[:number]


sw = stopwords.words('english')
sw.extend(['ll', 've'])

def check_word(word):
    return word.isalpha() and len(word) > 1

def prepare_message(msg):
    words = filter(check_word, wordpunct_tokenize(msg.lower()))
    return dict((w, True) for w in set(words).difference(sw))

def load_dataset(label, path, number):
    return [(prepare_message(msg), label)
            for msg in load_messages(path, number)]


def main():
    training_spam = load_dataset('spam', 'spam.json', 1000)
    training_ham = load_dataset('ham', 'ham.json', 1000)
    test_spam = load_dataset('spam', 'spam.json', 3000)[2000:]
    test_ham = load_dataset('ham', 'ham.json', 3000)[2000:]
    nbc = NaiveBayesClassifier.train(training_ham + training_spam)
    print 'Test Spam accuracy: %f' % classify.accuracy(nbc, test_spam)
    print 'Test Ham accuracy: %f' % classify.accuracy(nbc, test_ham)
    print nbc.show_most_informative_features(20)


if __name__ == '__main__':
    main()
