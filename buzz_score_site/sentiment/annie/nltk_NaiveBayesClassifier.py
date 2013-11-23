__author__ = 'annie'

import os
import numpy as np
from nltk.tokenize import regexp_tokenize
from nltk.corpus import stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from buzz_score_site.settings import APPLICATION_ROOT

path_pos = os.path.join(APPLICATION_ROOT, '../data_set/sentiment_analysis/ru/pos')
path_neg = os.path.join(APPLICATION_ROOT, '../data_set/sentiment_analysis/ru/neg')

def gen_list_for_test(name_file):
    list_dict_tweet = []
    for post in open(name_file):
        words = regexp_tokenize(post, "[\w']+")
        english_stops = set(stopwords.words('english'))
        list_dict_tweet.append({word.lower(): True for word in words if word not in english_stops})
    return list_dict_tweet

#def counting_frequency_words(tweet):
#    return dict([(word, True) for word in tweet])


def labeled_by_category(gen_dict_tweets, cat):
    return [(dict_tweets, cat) for dict_tweets in gen_dict_tweets]


pipeline = Pipeline([('tfidf', TfidfTransformer()),
                     ('chi2', SelectKBest(chi2, k=1000)),
                     ('nb', MultinomialNB())])

classifier = SklearnClassifier(pipeline)

scope_for_learning = 5000

pos = gen_list_for_test(path_pos)
neg = gen_list_for_test(path_neg)

features = labeled_by_category(pos[:scope_for_learning], 'pos') + \
           labeled_by_category(neg[:scope_for_learning], 'neg')

classifier.train(features)

l_pos = np.array(classifier.batch_classify(pos[scope_for_learning:]))
l_neg = np.array(classifier.batch_classify(neg[scope_for_learning:]))

#print(''.format())

print(len(pos))
print("Confusion matrix:\n%d\t%d\n%d\t%d" % (
    (l_pos == 'pos').sum(), (l_pos == 'neg').sum(),
    (l_neg == 'pos').sum(), (l_neg == 'neg').sum()))

