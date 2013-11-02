import numpy as np
from nltk.probability import FreqDist
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from nltk.corpus import movie_reviews

pipeline = Pipeline([('tfidf', TfidfTransformer()),
                     ('chi2', SelectKBest(chi2, k=1000)),
                     ('nb', MultinomialNB())])
classifier = SklearnClassifier(pipeline)

pos = [FreqDist(movie_reviews.words(i)) for i in movie_reviews.fileids('pos')]
neg = [FreqDist(movie_reviews.words(i)) for i in movie_reviews.fileids('neg')]
add_label = lambda lst, lab: [(x, lab) for x in lst]
classifier.train(add_label(pos[:100], 'pos') + add_label(neg[:100], 'neg'))

l_pos = np.array(classifier.batch_classify(pos[100:]))
l_neg = np.array(classifier.batch_classify(neg[100:]))
print "Confusion matrix:\n%d\t%d\n%d\t%d" % (
    (l_pos == 'pos').sum(), (l_pos == 'neg').sum(),
    (l_neg == 'pos').sum(), (l_neg == 'neg').sum())
