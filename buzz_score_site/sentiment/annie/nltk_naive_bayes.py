import os
import numpy as np
from nltk.tokenize import regexp_tokenize
from nltk.corpus import stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from buzz_score_site.settings import DATASET_ROOT

path_pos = os.path.sep(DATASET_ROOT, 'sentiment_analysis', 'ru', 'pos')
path_neg = os.path.sep(DATASET_ROOT, 'sentiment_analysis', 'ru', 'neg')


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

if __name__ == '__main__':
    print(len(pos))
    print("Confusion matrix:\n%d\t%d\n%d\t%d" % (
        (l_pos == 'pos').sum(), (l_pos == 'neg').sum(),
        (l_neg == 'pos').sum(), (l_neg == 'neg').sum()))

