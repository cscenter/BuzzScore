import os

import numpy as np
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
import buzz_score_site.settings as settings

BASE_DIR_EN = os.path.join(settings.DATASET_ROOT, "sentiment_analysis",
                           "en", "rt-polaritydata")
BASE_DIR_RU = os.path.join(settings.DATASET_ROOT, "sentiment_analysis",
                           "ru", "rt-polaritydata")
MODEL_PATH_EN = os.path.join(settings.CLASSIFIER_ROOT,
                             "sentiment_classifier_en.pkl")
MODEL_PATH_RU = os.path.join(settings.CLASSIFIER_ROOT,
                             "sentiment_classifier_ru.pkl")
VECTORIZER_PATH_EN = os.path.join(settings.CLASSIFIER_ROOT,
                                  "vectorizer_en.pkl")
VECTORIZER_PATH_RU = os.path.join(settings.CLASSIFIER_ROOT,
                                  "vectorizer_ru.pkl")


def go(sentences, language="en"):
    """ Give sentences, sentences is list
        Return labels [ints]
    """
    if language == "en":
        classifier = joblib.load(MODEL_PATH_EN)
        dv = joblib.load(VECTORIZER_PATH_EN)  # load dictionary
    elif language == "ru":
        classifier = joblib.load(MODEL_PATH_RU)
        dv = joblib.load(VECTORIZER_PATH_RU)
    else:
        raise Exception("Undefined language")
    X = dv.transform(sentences)  # matrix of features
    labels = list(classifier.predict(X))
    return map(int, labels)


def save_trained(base_dir_path, vectorizer_path, model_path):
    def set_label(label, n):
        y = np.empty(n, dtype=np.int8)  # array of labels
        y.fill(label)
        return y

    Xp = list(open(os.path.join(base_dir_path, "rt-polarity.pos")))
    yp = set_label(1, len(Xp))

    Xn = list(open(os.path.join(base_dir_path, "rt-polarity.neg")))
    yn = set_label(-1, len(Xn))

    dv = CountVectorizer(analyzer="word", ngram_range=(1, 2), lowercase=False,
                         charset_error="ignore", binary=True, dtype=np.int32)

    X_train = dv.fit_transform(Xp + Xn)
    joblib.dump(dv, vectorizer_path)
    y_train = np.concatenate([yp, yn])
    clf = BernoulliNB()
    clf.fit(X_train, y_train)
    joblib.dump(clf, model_path)


if __name__ == "__main__":
    with open(os.path.join(BASE_DIR_EN, "rt-polarity.pos")) as sentences_file:
        sentences = list(sentences_file)
        res = go(sentences, "en")
        print(res[:10])
