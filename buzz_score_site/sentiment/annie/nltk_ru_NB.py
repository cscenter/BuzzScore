# coding=utf-8
from pip.vendor.html5lib import tokenizer

__author__ = 'annie'
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import os
from buzz_score_site.settings import DATASET_ROOT

path_stopwords = os.path.join(DATASET_ROOT, 'ru/stopwords')
path_pos = os.path.join(DATASET_ROOT, 'sentiment_analysis/ru/pos')
path_neg = os.path.join(DATASET_ROOT, 'sentiment_analysis/ru/neg')

#para ='рок суждено стать новым 21-го века "Конан". и что он собирается сделать всплеск даже больше,'
para = open(path_pos)
para1 = para.readline()
print(para)
print(list(s for s in sent_tokenize(para))[0])

#stopwords = [s.decode('utf-8') for s in word_tokenize(open(path_stopwords).read())]
#if u'и' in stopwords: # требуются преобразования u'и' (или 'и'.decode('utf-8')) == '\xd0\xb8'.decode('utf-8')
#    print('yes')