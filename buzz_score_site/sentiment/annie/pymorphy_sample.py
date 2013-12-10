# coding=utf-8
import os
from nltk import sent_tokenize, regexp_tokenize, word_tokenize
from pymorphy2 import MorphAnalyzer
from buzz_score_site.settings import DATASET_ROOT

path_pos = os.path.join(DATASET_ROOT, "sentiment_analysis", "ru", "pos")



def uprint(list_a_words):
    for word in list_a_words:
        print('%s' % word)


def get_sentence(text):

    yield sent_tokenize(file_name.readline())

sentence = get_sentence(path_pos)
print(type(sentence.next()))
sentence.next()
print(sentence.next())


'''
for i in xrange(3):
    print('------------\n')
    s = list(sentence.next())
    print(len(s))
    print(s)
    #for j in s:
    #    pprint(word_tokenize(j))
    #    pprint(regexp_tokenize(j, u"[\w']+"))


#list_a_words = regexp_tokenize(list_a_tweet[0], u"[\w']+")
#list_a_words = word_tokenize(list_a_tweet[0])



morph = MorphAnalyzer()

s = u'разрядка'
# часть речи
j = morph.parse(s)[0].tag.POS
#j = morph.parse(s)

if j == 'ADVB': pass # наречие
if j == 'PRCL': pass # частица
if j == 'COMP': pass # компоратив
if j == 'ADJF': pass # прил полное
if j == 'ADJS': pass # прил краткое
if j == 'INTJ': pass # междометие
if j == 'PRED': pass # предикатив пр. некогда
if j == 'GRND': pass # деепричастие пр. красив


# нормальная форма
k = morph.parse(s)[0].inflect({'sing', 'nomn'}).word
print(j)
print(k)'''