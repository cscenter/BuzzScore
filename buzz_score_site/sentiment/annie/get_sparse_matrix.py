# coding=utf-8
import os
import pickle
import itertools
import numpy as np
from pprint import pprint
from nltk.tokenize import word_tokenize, sent_tokenize
from scipy.sparse import csc_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from buzz_score_site.settings import DATASET_ROOT


path_pos = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'pos')
path_neg = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'neg')
path_X = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'count_vector')
path_XTF = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'count_vectorTF')
path_XTFmax_f = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'count_vectorTF')
path_XTFNgram = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'count_vectorTFNgram')
path_vocabulary = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'vocabulary')
path_vocabularyTF = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'vocabularyTF')
path_vocabularyTFmax_f = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'vocabularyTFmax_F')
path_vocabularyTFNgram = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'vocabularyTFNgram')
path_trainedMB = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'trainedMB')


def dump_feature_extraction(input_file=None, output_path=None, vocabulary_path=None):
    """
    Загрузить матрицу частот извлеченных слова из документа, а также инвертированный словарь слов.
    """
    count_vector = TfidfVectorizer(input='content') # max_features - плохой показатель
    # count_vector = CountVectorizer(input=file_in)
    X = count_vector.fit_transform(input_file)
    with open(output_path, 'wb') as out_file:
        pickle.dump(X, out_file)
    voc = {}
    for w, i in count_vector.vocabulary_.items():
        voc[i] = w
    with open(vocabulary_path, 'wb') as vocabulary_file:
        pickle.dump(voc, vocabulary_file)


def get_matrix_X(input_file):
    """
    Получить разряженную матрицу частот слов в виде CSC, полученнцю после обработки feature_extraction.
    """
    with open(input_file, 'rb') as file_in:
        return pickle.load(file_in)


def get_vocabulary(input_file):
    """
    Получить инвертированный словарь слов.
    """
    with open(input_file, 'rb') as vocabulary_file:
        return pickle.load(vocabulary_file)


def count_mi(*frequency):
    """
    Посчитать вручую оценку показательности классификационных признаков методом взаимной информации (Mutual Information).
    см. http://bazhenov.me/blog/2012/12/10/feature-selection.html
    Можно еще посмотреть from sklearn.metrics.cluster import adjusted_mutual_info_score
    http://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_mutual_info_score.html#sklearn.metrics.adjusted_mutual_info_score
    Пример: print(count_mi(65342, 143, 9, 897567))
    Возвращает: -inf
    """
    n = sum(frequency)
    n11, n10, n01, n00 = frequency
    a = np.array(frequency).reshape(2, 2)
    n1_r, n0_r = a.sum(axis=0)
    n1_c, n0_c = a.sum(axis=1)
    mi = (n11 * np.log2(n * n11 / (n1_r * n1_c)) + n01 * np.log2(n * n01 / (n0_r * n1_c)) +
          n10 * np.log2(n * n10 / (n1_r * n0_c)) + n00 * np.log2(n * n00 / (n0_r * n0_c))) / n
    return mi


def get_trained_classifier(classifier_name=MultinomialNB, X=None, num_pos=0, num_neg=0):
    """
    Получиь обученный классификатор.
    """
    y = [1] * num_pos + [0] * num_neg
    classifier = classifier_name()
    classifier.fit(X, y)
    return classifier


def dump_trained_classifier(classifier, output_path):
    """
    Записать на диск обученнный классификатор.
    """
    with open(output_path, 'wb') as MB_file:
        pickle.dump(classifier, MB_file)


def load_trained_classifier(input_path):
    """
    Загрузить обученный классификатор.
    """
    with open(input_path) as classifier_file:
        return pickle.load(classifier_file)


def out_high_frequency_words(path_matrix, path_vocabulary, number=10, file_output=None):
    """
    Вывести самые высокочастотные слова в коллекции документов. Частота определяется по весам, полученным в feature_extraction.
    """
    vocabulary = get_vocabulary(path_vocabulary)
    X = get_matrix_X(path_matrix)
    normalized_X = X.sum(axis=0) / ((X != 0).sum(axis=0) + 0.00001)
    sorted_args_X = normalized_X.argsort()

    if file_output != None:
        with open(file_output, 'w') as file_out:
            for i in xrange(1, min(number+1, len(sorted_args_X))):
                file_out.write(vocabulary[sorted_args_X[0, -i]])
    else:
        for i in xrange(1, min(number+1, len(sorted_args_X))):
            print(vocabulary[sorted_args_X[0, -i]])


def out_low_frequency_words(path_matrix, path_vocabulary, number=10, file_output=None):
    """
    Вывести самые низкочастотны слова в коллекции документов. Частота определяется по весам, полученным в feature_extraction.
    """
    vocabulary = get_vocabulary(path_vocabulary)
    X = get_matrix_X(path_matrix)
    normalized_X = X.sum(axis=0) / ((X != 0).sum(axis=0) + 0.00001)
    sorted_args_X = normalized_X.argsort()

    if file_output != None:
        with open(file_output, 'w') as file_out:
            for i in xrange(min(number, len(sorted_args_X))):
                file_out.write(vocabulary[sorted_args_X[0, i]])
    else:
        for i in xrange(min(number, len(sorted_args_X))):
            print(vocabulary[sorted_args_X[0, i]])


if __name__ == '__main__':
    # dump_feature_extraction(itertools.chain(open(path_pos), open(path_pos)), path_XTF, path_vocabularyTF)
    trainedMB = load_trained_classifier(path_trainedMB)
    # print 'fit_prior', trainedMB.fit_prior
    # print 'class_prior', trainedMB.class_prior
    # print '_get_coef', trainedMB.coef_.max()
    # print 'class_count_', trainedMB.class_count_ # [ 2200.  2200.]
    # print 'feature_count_', trainedMB.feature_count_ # shape (2, 11161) max 54.9053226334 - то что нужно
    # print '_get_intercept', trainedMB._get_intercept()
    # sorted_trainedMB = trainedMB.feature_log_prob_.argsort()
    # sorted_trainedMB = trainedMB.feature_count_.argsort()
    v = get_vocabulary(path_vocabularyTF)
    for i in xrange(1, 3110, 100):
        print v[i], trainedMB.feature_count_[0, i], trainedMB.feature_count_[1, i]