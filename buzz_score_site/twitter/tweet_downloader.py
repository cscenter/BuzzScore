__author__ = 'nikita_kartashov'
# -*- encoding: utf-8 -*-

import itertools
import codecs
import logging
import traceback
import json

import TwitterSearch

from sentiment.analysis import go


CONSUMER_KEY = "qaxwA1MNvx2ilaBQaql4g"
CONSUMER_SECRET = "ok5l42lywxjEeh460xTy8EMUUQzMkVBhorITv82Yc"

TOKEN_KEY = "115023328-B3LMKWYXNS86M5YiS7BT8CSAvTFR8E9thUYIzGmd"
TOKEN_SECRET = "wgcM1iAZPvuSZBogjtEJ3B5VZRCb3vwCnBqqi9EGgA"


def download_tweets(search_string, language):
    """Returns list of tweets containing <search_string>, <language> should be like 'en' or 'ru' """

    tso = TwitterSearch.TwitterSearchOrder()
    tso.addKeyword(search_string)
    tso.setLanguage(language)
    #removed setCount, because default value is 100 and max value is also 100 (the bigger the better)
    tso.setIncludeEntities(False)

    # create a TwitterSearch object with our secret tokens
    ts = TwitterSearch.TwitterSearch(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=TOKEN_KEY,
        access_token_secret=TOKEN_SECRET
    )
    try:
        return ts.searchTweetsIterable(tso)

    except TwitterSearch.TwitterSearchException as e:
        logging.exception("%s: %s", e.code, e.message)
        logging.exception("Stack trace: %s", traceback.format_exc())
        raise e


def add_sentiment_to_list(items, language):
    sentiment = go([tweet['text'] for tweet in items], language)
    for i in range(len(sentiment)):
        items[i]['sentiment'] = 'positive' if sentiment[i] > 0 else 'negative'
    return items


def download_tweets_to_file(search_string, language, count, filename):
    """Downloads <count> tweets and dumps them to <filename> file"""
    downloaded_tweets = download_tweets(search_string, language)
    tweets_to_dump = itertools.islice(downloaded_tweets, count)
    with codecs.open(filename, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(list(tweets_to_dump), sort_keys=True,
                               indent=4, separators=(',', ': ')))



class TweetChunkIterator(object):
    _start = 0
    _chunk_size = 0
    _iterable = None

    def __init__(self, tweets_iterable, chunk_size):
        self._iterable = iter(tweets_iterable)
        self._chunk_size = chunk_size
        self._start = 0

    def __iter__(self):
        return self._iterable

    def next(self):
        return next(self._iterable)

    def get_chunk(self):
        """Returns a list of <self.chunk_size> sized chunks of tweets extracted from <self.iterable>"""
        result = list(itertools.islice(self._iterable, self._start, self._start + self._chunk_size))
        self._start += self._chunk_size
        return result