# coding=utf-8

import os
import itertools
import pickle
import numpy as np
from nltk.tokenize import regexp_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.pipeline import Pipeline
from buzz_score_site.settings import DATASET_ROOT

path_neg = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'neg')
path_pos = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'pos')


def word_feats(words):
    # return dict([(word, True) for word in word_tokenize(words)])
    # with open(os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'stopwords.pkl'), 'rb') as f: # добавить stopwords
    #     stopwords = pickle.load(f)
    #return dict([(word, True) for word in regexp_tokenize(words, "[\w']+") if word not in stopwords])
    return dict([(word, True) for word in regexp_tokenize(words, "[\w']+")])


add_label = lambda lst, lab: [(x, lab) for x in lst]

pipeline = Pipeline([
    # ('cvec', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    #                  ('chi2', SelectKBest(chi2, k=100)),
                     ('nb', MultinomialNB())])
classifier = SklearnClassifier(pipeline)

pos_set = map(word_feats, open(path_pos).readlines())
neg_set = map(word_feats, open(path_neg).readlines())

PART = 10000 * 4/5
SCOPE = int(len(pos_set) * PART/10000)

# features = zip(pos_set[:SCOPE], itertools.repeat("pos")) + \
#            zip(neg_set[:SCOPE], itertools.repeat("neg"))
features = zip(neg_set[:SCOPE], itertools.repeat("neg")) + \
           zip(pos_set[:SCOPE], itertools.repeat("pos"))



if __name__ == '__main__':
    classifier.train(features)

    def unicode_print(list_a_words):
        for word in list_a_words:
            print("%s: %d " % (word, list_a_words[word]))

    # print(classifier._feature_index)
    feature_count = classifier._clf.named_steps['nb'].feature_count_
    for i in xrange(1, 1000, 100):
        print i, feature_count[0, i], feature_count[1, i]

    # l_pos = np.array(classifier.batch_classify(pos_set[SCOPE:]))
    # l_neg = np.array(classifier.batch_classify(neg_set[SCOPE:]))
    #
    # print("Confusion matrix:\n%d\t%d\n%d\t%d" % (
    #     (l_pos == 'pos').sum(), (l_pos == 'neg').sum(),
    #     (l_neg == 'pos').sum(), (l_neg == 'neg').sum()))
    #
    # print("Процент положительных в pos_set %d\n"
    #   "Процент отрицательных в pos_set %d\n"
    #   "Процент отрицательных в neg_set %d\n"
    #   "Процент положиетльных в neg_set %d\n" % (
    # (l_pos == 'pos').sum() * 10000 / (len(pos) - SCOPE),
    # (l_pos == 'neg').sum() * 10000 / (len(pos) - SCOPE),
    # (l_neg == 'neg').sum() * 10000 / (len(neg) - SCOPE),
    # (l_neg == 'pos').sum() * 10000 / (len(neg) - SCOPE)))


