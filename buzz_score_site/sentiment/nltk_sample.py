import os
import itertools
from nltk import word_tokenize, sent_tokenize
import numpy as np
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

DATA_PATH = '../../datasets/sentiment_analysis/en/rt-polaritydata'


def word_feats(words):
    return dict([(word, True) for word in sent_tokenize(words)])


add_label = lambda lst, lab: [(x, lab) for x in lst]

pipeline = Pipeline([('tfidf', TfidfTransformer()),
                     ('chi2', SelectKBest(chi2, k=1000)),
                     ('nb', MultinomialNB())])
classifier = SklearnClassifier(pipeline)

pos = map(word_feats,
          open(os.path.join(DATA_PATH, 'rt-polarity.pos')).readlines())
neg = map(word_feats,
          open(os.path.join(DATA_PATH, 'rt-polarity.neg')).readlines())

features = zip(pos[:len(pos) / 2], itertools.repeat("pos")) + \
           zip(neg[:len(neg) / 2], itertools.repeat("neg"))
classifier.train(features)

l_pos = np.array(classifier.batch_classify(pos[len(pos) / 2:]))
l_neg = np.array(classifier.batch_classify(neg[len(neg) / 2:]))
print "Confusion matrix:\n%d\t%d\n%d\t%d" % (
    (l_pos == 'pos').sum(), (l_pos == 'neg').sum(),
    (l_neg == 'pos').sum(), (l_neg == 'neg').sum())
