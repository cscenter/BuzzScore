# coding=utf-8
import os
import itertools
import pickle
import numpy as np
from nltk.tokenize import regexp_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.pipeline import Pipeline
from buzz_score_site.settings import DATASET_ROOT

path_neg = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'neg')
path_pos = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'pos')


def word_feats(words):
    # return dict([(word, True) for word in word_tokenize(words)])
    # with open(os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'stopwords.pkl'), 'rb') as f:
    #     stopwords = pickle.load(f)
    #     return dict([(word, True) for word in regexp_tokenize(words, "[\w']+") if word not in stopwords])
    return dict([(word, True) for word in regexp_tokenize(words, "[\w']+")])


add_label = lambda lst, lab: [(x, lab) for x in lst]

pipeline = Pipeline([
    # ('tfidf', TfidfTransformer()),
    #                  ('chi2', SelectKBest(chi2, k=100)),
                     ('nb', MultinomialNB())])
classifier = SklearnClassifier(pipeline)

pos = map(word_feats,
          open(path_pos).readlines())
neg = map(word_feats,
          open(path_neg).readlines())

PART = 10000*4/5
SCOPE = int(len(pos) * PART/10000)

# features = zip(pos[:SCOPE], itertools.repeat("pos")) + \
#            zip(neg[:SCOPE], itertools.repeat("neg"))
features = zip(neg[:SCOPE], itertools.repeat("neg")) + \
           zip(pos[:SCOPE], itertools.repeat("pos"))


if __name__ == '__main__':
    classifier.train(features)

    def unicode_print(list_a_words):
        for word in list_a_words:
            print("%s: %d " % (word, list_a_words[word]))

    print(classifier._feature_index)

    l_pos = np.array(classifier.batch_classify(pos[SCOPE:]))
    # l_neg = np.array(classifier.batch_classify(neg[SCOPE:]))
    #
    # print("Confusion matrix:\n%d\t%d\n%d\t%d" % (
    #     (l_pos == 'pos').sum(), (l_pos == 'neg').sum(),
    #     (l_neg == 'pos').sum(), (l_neg == 'neg').sum()))
    #
    # print("Процент положительных в pos %d\n"
    #   "Процент отрицательных в pos %d\n"
    #   "Процент отрицательных в neg %d\n"
    #   "Процент положиетльных в neg %d\n" % (
    # (l_pos == 'pos').sum() * 10000 / (len(pos) - SCOPE),
    # (l_pos == 'neg').sum() * 10000 / (len(pos) - SCOPE),
    # (l_neg == 'neg').sum() * 10000 / (len(neg) - SCOPE),
    # (l_neg == 'pos').sum() * 10000 / (len(neg) - SCOPE)))



'''

def gen_list_for_test(file_name):
    list_dict_tweet = []
    with open(file_name) as src_file:
        for post in src_file:
            words = regexp_tokenize(post, "[\w']+")
            english_stops = set(stopwords.words('english'))
            list_dict_tweet.append({word.lower(): True for word in words if word not in english_stops})
    return list_dict_tweet

#def counting_frequency_words(tweet):
#    return dict([(word, True) for word in tweet])


def label_by_category(gen_dict_tweets, cat): # label_by_category
    return [(dict_tweets, cat) for dict_tweets in gen_dict_tweets]


pipeline = Pipeline([('tfidf', TfidfTransformer()),
                     ('chi2', SelectKBest(chi2, k=1000)),
                     ('nb', MultinomialNB())])

classifier = SklearnClassifier(pipeline)

SCOPE_FOR_LEARNING = 5000

pos = gen_list_for_test(path_pos)
neg = gen_list_for_test(path_neg)

features = label_by_category(pos[:SCOPE_FOR_LEARNING], 'pos') + \
           label_by_category(neg[:SCOPE_FOR_LEARNING], 'neg')

classifier.train(features)

l_pos = np.array(classifier.batch_classify(pos[SCOPE_FOR_LEARNING:]))
l_neg = np.array(classifier.batch_classify(neg[SCOPE_FOR_LEARNING:]))
'''