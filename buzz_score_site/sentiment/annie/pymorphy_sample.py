# coding=utf-8
from __future__ import print_function
import os
import pickle
from random import shuffle, sample
import itertools
import re
from nltk import sent_tokenize, regexp_tokenize, word_tokenize,  FreqDist, NaiveBayesClassifier
from nltk.classify import accuracy, apply_features
from nltk.classify.scikitlearn import SklearnClassifier
from pymorphy2 import MorphAnalyzer
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.pipeline import Pipeline
from buzz_score_site.settings import DATASET_ROOT

PATH_POS = os.path.join(DATASET_ROOT, "sentiment_analysis", "ru", "pos")
PATH_NEG = os.path.join(DATASET_ROOT, "sentiment_analysis", "ru", "neg")
morph = MorphAnalyzer()
N_feature = 100
def uprint(list_a_words):
    # for word, l in list_a_words:
    #     print(l, '->', '%s' % word)
    # for word in list_a_words:
    #     print('%s' % word)
    for word, c in list_a_words.items():
        print('%s' % word, '->', c)



def get_marked_set(path, label=None):
    """
    Вернет размеченный список твитов, каждый твит - текст.
    """
    with open(path) as f:
        return zip(f.readlines(), itertools.repeat(label))


def get_tokens(text, stopwords=[]):
    """
    Возвращает список слов, получнных из текстаю
    """
    if not stopwords: # если не дан свой список исключений, инициализируем его
        stopwords = {u'перед', u'надо', u'зачем', u'там', u'так', u'два', u'разве', u'ему', u'тебя', u'потому', u'ли', u'вдруг', u'том', u'во', u'чего', u'у', u'нельзя', u'ведь', u'того', u'эту', u'них', u'нибудь', u'потом', u'как', u'в', u'есть', u'куда', u'можно', u'ее', u'вы', u'нас', u'здесь', u'на', u'нее', u'он', u'никогда', u'об', u'ней', u'тогда', u'себе', u'все', u'вот', u'для', u'с', u'чтоб', u'где', u'я', u'а', u'через', u'к', u'когда', u'о', u'мы', u'тем', u'один', u'тот', u'всю', u'конечно', u'себя', u'меня', u'иногда', u'уж', u'то', u'от', u'сейчас', u'над', u'быть', u'еще', u'раз', u'что', u'если', u'свою', u'при', u'про', u'мой', u'они', u'им', u'вам', u'мне', u'из', u'после', u'же', u'за', u'будет', u'него', u'вас', u'под', u'и', u'ты', u'их', u'тут', u'ей', u'ну', u'этого', u'моя', u'без', u'до', u'кто', u'со', u'его', u'три', u'между', u'какой', u'была', u'или', u'какая', u'было', u'были', u'этот', u'только', u'впрочем', u'ним', u'эти', u'она', u'но', u'чтобы', u'наконец', u'по', u'теперь', u'был', u'может', u'сам', u'этом', u'всех', u'этой', u'чем', u'бы', u'уже'}
    split_words= map(lambda w: unicode(w, encoding='utf-8', errors='replace').lower(),
                     word_tokenize(re.sub("['`.«<>-]|``", ' ', text)))
    return [w for w in split_words if w not in stopwords and len(w) > 1]


def get_ngrams(text, n=3):
    list_ngrams = []
    for word in get_tokens(text):
        poz = range(0, len(word)+1, n) if len(word) + 1 > n else [0, len(word)]
        for i in xrange(len(poz) - 1):
            list_ngrams.append(word[poz[i]:poz[i+1]])
    return list_ngrams


class Doc_feat_extractor:
    """
    Содержит метод, который извлекает признаки из документа. Сначала нужно создать экземпляр класса c полями:
        all_words, amount_of_words, func ('extract_normal_form' or 'extract_simple_word' or 'extract_ngram')
    Возвращает features.
    """
    def __init__(self, all_words, amount_of_words=N_feature, func='extract_simple_word', ngrams=3):
        self.all_feats = all_words
        self.amount_of_feats = amount_of_words
        self.func = func
        self.ngrams = ngrams

    def __call__(self, document):
        return getattr(self, self.func)(document)

    def extract_simple_word(self, document):
        return {'contains(%s)' % word: (word in get_tokens(document))
                for word in self.all_feats.keys()[:min(len(self.all_feats), self.amount_of_feats)]}

    def extract_normal_form(self, documnet):
        features = {}
        words_in_doc = get_tokens(documnet)
        for word in self.all_feats.keys()[:min(len(self.all_feats), self.amount_of_feats)]: # берем amount_of_feats наиболее встречаемых слов из all_feats
            try:
                word = morph.parse(word)[0].normal_form # получаем нормальную форму
            except (IndexError, UnicodeDecodeError):
                pass
            features['contains(%s)' % word] = (word in words_in_doc)
        return features

    def extract_ngram(self, document):
        """
        Разделяет на 3символьные граммы
        """
        # tokenize = HashingVectorizer(analyzer='char_wb', ngram_range=(2, 2)).build_tokenizer()

        return {'contains(%s)' % word: (word in get_ngrams(document, self.ngrams))
                for word in self.all_feats.keys()[:min(len(self.all_feats), self.amount_of_feats)]}


def get_all_words(doc_set):
    """
    На вход подается размеченное множество документов, каждый документ - nекст.
    Вернет FreqDist - наподобии словаря {признак: частота вхождения, ...}, каждый признак просто слово.
    """
    all_feature = []
    for doc, label in doc_set:
        all_feature.extend(get_tokens(doc))
    return FreqDist(all_feature)[:N_feature]

def get_all_normal_forms(doc_set):
    """
    На вход подается размеченное множество документов, каждый документ - nекст.
    Вернет FreqDist - наподобии словаря {признак: частота вхождения, ...}, каждый признак нормальная форма слова.
    """
    all_feature = []
    for doc, label in doc_set:
        for token in get_tokens(doc):
            try:
                token = morph.parse(token)[0].normal_form # получаем нормальную форму
            except (IndexError, UnicodeDecodeError):
                pass
            all_feature.append(token)
    return FreqDist(all_feature)[:N_feature]

def get_all_ngram(doc_set, n=3):
    """
    Вернет FreqDist - наподобии словаря {признак: частота вхождения, ...}, каждый признак просто символьная ngramma
    """
    all_feature = []
    for doc, label in doc_set:
        all_feature.extend(get_ngrams(doc, n))
    return FreqDist(all_feature)[:N_feature]


def cross_validate(a_classiffier, content_set, number_folds, all_feats, amount_feats, type_feats):
    with open('result.txt', 'a') as result_file:
        print('\n\n\nClassiffier {0}, features is {1}'.format(a_classiffier[1], type_feats[8:]), file=result_file) # запись в файл file=result_file
        document_extraction = Doc_feat_extractor(all_feats, amount_feats, type_feats)
        incr = len(content_set) // number_folds
        for i in xrange(number_folds):
            train_set = apply_features(document_extraction,
                                       content_set[:i * incr] + content_set[(i + 1) * incr:])
            test_set = apply_features(document_extraction,
                                      content_set[i * incr: min((i + 1) * incr, len(content_set))])
            classifier = a_classiffier[0].train(train_set)
            y_true = [l for (fs, l) in test_set]
            y_pred = classifier.batch_classify([fs for (fs, l) in test_set])
            print('\n{0} attempt\n'.format(i + 1), classification_report(y_true, y_pred,), file=result_file)
            result_file.flush()
        # print(classifier['nb'].show_most_informative_features())

def run_approaches(content_set):
    j=0
    common = {'content_set': content_set, 'number_folds': 2, 'amount_feats': N_feature, 'a_classiffier': None}
    args = [{'all_feats': get_all_words(content_set), 'type_feats': 'extract_simple_word'},
            {'all_feats': get_all_normal_forms(content_set), 'type_feats': 'extract_normal_form'},
            {'all_feats': get_all_ngram(content_set, 3), 'type_feats': 'extract_ngram'}]
    clssfr = [(NaiveBayesClassifier, 'NaiveBayesClassifier'),
              (SklearnClassifier(Pipeline([('nb', MultinomialNB())])), 'MultinomialNB without TfidfTransformer'),
              (SklearnClassifier(Pipeline([('tfidf', TfidfTransformer()), ('nb', MultinomialNB())])), 'MultinomialNB with TfidfTransformer'),
              (SklearnClassifier(Pipeline([('nb', BernoulliNB())])), 'BernoulliNB without TfidfTransformer'),
              (SklearnClassifier(Pipeline([('tfidf', TfidfTransformer()), ('nb', BernoulliNB())])), 'BernoulliNB with TfidfTransformer')]
    for arg in args:
        print(arg['type_feats'])
        for cl in clssfr:
            try:
                common['a_classiffier'] = cl
                arg.update(common)
                cross_validate(**arg)
            except ValueError:
                pass
            j+=1; print('\t', j, cl[1])


if __name__ == '__main__':
    # tweet_set = sample(get_marked_set(PATH_POS, 'pos'), 50) + sample(get_marked_set(PATH_NEG, 'neg'), 50)
    tweet_set = sample(get_marked_set(PATH_POS, 'pos'), 1000) + sample(get_marked_set(PATH_NEG, 'neg'), 1000)
    # tweet_set = get_marked_set(PATH_POS, 'pos') + get_marked_set(PATH_NEG, 'neg')
    shuffle(tweet_set)
    run_approaches(tweet_set)

