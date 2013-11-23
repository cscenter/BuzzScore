# coding=utf-8

from pymorphy2 import MorphAnalyzer

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
print(k)