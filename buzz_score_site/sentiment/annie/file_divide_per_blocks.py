__author__ = 'annie'

path_neg = '/Users/annie/PycharmProjects/BuzzScore/data_set/sentiment_analysis/en/rt-polaritydata/rt-polarity.neg'
path_pos = '/Users/annie/PycharmProjects/BuzzScore/data_set/sentiment_analysis/en/rt-polaritydata/rt-polarity.pos'
f = open(path_pos)


i = 0
k = 1
fout = 'pos_en_'
ff = open(fout + str(k), 'w')
# разбиение большого файла на несколько поменьше. Нужно для перевода в Google Translate
for line in f:
    if i != 0 and i % 200 == 0:
        if k == 5: break
        ff.close()
        k += 1
        ff = open(fout + str(k), 'w')
    ff.write(line)
    i += 1
ff.close()