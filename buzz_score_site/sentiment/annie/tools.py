# coding=utf-8
from __future__ import print_function
import os
import pickle
from json import load
from buzz_score_site.settings import DATASET_ROOT
from buzz_score_site.twitter.tweet_downloader import download_tweets_to_file

path_neg_en = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'en', 'rt-polaritydata', 'rt-polarity', 'neg_set')
path_pos_en = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'en', 'rt-polaritydata', 'rt-polarity', 'pos_set')


def file_divide_per_blocks(path_file_input):
    """
    Разбиение большого файла на несколько поменьше. Нужно для перевода в Google Translate
    """
    i = 0
    k = 1
    fout = 'pos_en_'
    ff = open(fout + str(k), 'w')
    with open(path_file_input) as f:
        for line in f:
            if i != 0 and i % 200 == 0:
                if k == 5: break
                ff.close()
                k += 1
                ff = open(fout + str(k), 'w')
            ff.write(line)
            i += 1
    ff.close()

def unicode_print(list_a_words):
    for word in list_a_words:
        print("%s" % word)
#
# stopwords = {'и', 'в', 'во', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'о', 'из', 'ему', 'теперь', 'когда', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'чего', 'раз', 'себе', 'под', 'будет', '', '', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'ним', 'здесь', 'этом', 'один', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'после', 'над', 'тот', 'через', 'эти', 'нас', 'про', 'них', 'какая', 'разве', 'три', 'эту', 'моя', 'впрочем', 'свою', 'этой', 'перед', 'иногда', 'том', 'нельзя', 'им', 'конечно', 'всю', 'между'}
# path_stop = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'stopwords.pkl')
# f = open(path_stop, 'wb')
# pickle.dump(stopwords, f)
# f.close()


path_tw = os.path.join(DATASET_ROOT, 'sentiment_analysis', 'ru', 'tweets')
#download_tweets_to_file('сталин', 'ru', 100, path_tw)
i = 0
with open(path_tw) as src_file:
    for tweet in load(src_file):
        if i == 30: break
        i += 1
        print(tweet['text'])
        print('\n')


''' trash
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