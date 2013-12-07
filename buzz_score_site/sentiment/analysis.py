import os

import numpy as np
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from django.conf import settings

BASE_DIR = os.path.join(settings.DATASET_ROOT, "sentiment_analysis",
                        "en", "rt-polaritydata")
MODEL_PATH = os.path.join(settings.CLASSIFIER_ROOT, "sentiment_classifier.pkl")
VECTORIZER_PATH = os.path.join(settings.CLASSIFIER_ROOT, "vectorizer.pkl")


def go(sentences):
    """ Give sentences, sentences is list
        Return labels [ints]
    """
    classifier = joblib.load(MODEL_PATH)
    dv = joblib.load(VECTORIZER_PATH)  # load dictionary
    X = dv.transform(sentences)  # matrix of features
    labels = list(classifier.predict(X))
    return map(int, labels)


def save_trained():
    def set_label(label, n):
        y = np.empty(n, dtype=np.int8)  # array of labels
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
