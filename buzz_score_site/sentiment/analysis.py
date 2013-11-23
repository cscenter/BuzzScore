import os
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.naive_bayes import BernoulliNB

MODEL_PATH = "sentiment_classifier.pkl"
VECTORIZER_PATH = "vectorizer.pkl"
BASE_DIR = "../../data_set/sentiment_analysis/en/rt-polaritydata"


def go(sentences):
    """ Give sentences, sentences is list
        Return list of pairs: (sentence, label)
    """
    classifier = joblib.load(MODEL_PATH)
    dv = joblib.load(VECTORIZER_PATH)
    X = dv.transform(sentences)
    labels = list(classifier.predict(X))
    return [(sentences, int(label)) for label in labels]


def save_trained():

    def set_label(label, N):
        y = np.empty(N, dtype=np.int8)
        y.fill(label)
        return y

    Xp = list(open(os.path.join(BASE_DIR, "rt-polarity.pos")))
    yp = set_label(1, len(Xp))

    Xn = list(open(os.path.join(BASE_DIR, "rt-polarity.neg")))
    yn = set_label(-1, len(Xn))

    dv = CountVectorizer(analyzer="word", ngram_range=(1, 2), lowercase=False,
                         charset_error="ignore", binary=True, dtype=np.int32)

    X_train = dv.fit_transform(Xp + Xn)
    joblib.dump(dv, VECTORIZER_PATH)
    y_train = np.concatenate([yp, yn])
    clf = BernoulliNB()
    clf.fit(X_train, y_train)
    joblib.dump(clf, MODEL_PATH)

if __name__ == "__main__":

    with open(os.path.join(BASE_DIR, "rt-polarity.pos")) as sentences_file:
        sentences = list(sentences_file)
        res = go(sentences)
        print(res[:10])
