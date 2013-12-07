import functools
import os

import numpy as np
from sklearn import cross_validation, metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier, \
    PassiveAggressiveClassifier, Perceptron
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC, NuSVC


def prepare_dataset(base_dir):
    def prepare(path, label):
        X = list(open(path))
        y = np.empty(len(X), dtype=np.int8)
        y.fill(label)
        return X, y

    Xp, yp = prepare(os.path.join(base_dir, "rt-polarity.pos"), 1)  # positive
    Xn, yn = prepare(os.path.join(base_dir, "rt-polarity.neg"), -1)  # negative
    dv = CountVectorizer(analyzer="word", ngram_range=(1, 2), lowercase=False,
                         charset_error="ignore", binary=True, dtype=np.int32)
    X = dv.fit_transform(Xp + Xn)
    y = np.concatenate([yp, yn])
    return X, y

if __name__ == "__main__":
    X, y = prepare_dataset(
        os.path.join("..", "..", "datasets", "sentiment_analysis",
                     "en", "rt-polaritydata"))
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        X, y, test_size=.4)

    models = [MultinomialNB, BernoulliNB,
              functools.partial(SGDClassifier, loss="hinge", penalty="l2"),
              LogisticRegression,
              Perceptron,
              PassiveAggressiveClassifier,
              functools.partial(LinearSVC, C=0.01, penalty="l1", dual=False),
              NuSVC,
              KNeighborsClassifier,
              ]

              # Note (katya):
              # ValueError: No neighbors found for test samples [0, 1, 2, 3, 4,
              # 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ...]
              # you can try using larger radius, give a label for outliers,
              # or consider removing them from your dataset.
              # RadiusNeighborsClassifier

              # Note (katya):
              # UserWarning: The sum of true positives and false positives are
              # equal to zero for some labels. Precision is ill defined for
              # those labels [-1]. The precision and recall are equal to zero
              # for some labels. fbeta_score is ill defined for those
              # labels [-1].
              # SVC

              # Note (katya):
              # "TypeError: A sparse matrix was passed, but
              # dense data is required. Use X.toarray() to convert to a dense
              # numpy array."
              # functools.partial(RandomForestClassifier,
              #                  n_jobs=2, criterion="entropy"),
              # BayesianRidge
              # DecisionTreeClassifier,
              # GradientBoostingClassifier
              # ExtraTreesClassifier

    for model in models:
        clf = model()
        clf.fit(X_train, y_train)
        print(clf.__class__.__name__)
        print(metrics.classification_report(y_test, clf.predict(X_test),
                                        [1, -1], ["pos", "neg"]))
