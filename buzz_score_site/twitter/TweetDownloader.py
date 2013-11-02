__author__ = 'nikita_kartashov'
# -*- encoding: utf-8 -*-

import TwitterSearch
import itertools
import codecs
import requests
from requests_oauthlib import OAuth1
import urllib

CONSUMER_KEY = "qaxwA1MNvx2ilaBQaql4g"
CONSUMER_SECRET = "ok5l42lywxjEeh460xTy8EMUUQzMkVBhorITv82Yc"

TOKEN_KEY = "115023328-B3LMKWYXNS86M5YiS7BT8CSAvTFR8E9thUYIzGmd"
TOKEN_SECRET = "wgcM1iAZPvuSZBogjtEJ3B5VZRCb3vwCnBqqi9EGgA"


class TweetDownloader:
    def __init__(self):
        pass

    @staticmethod
    def preprocess_search_string(search_string):
        """Returns list containing preprocessed <search_string> for using in net queries"""
        #search_string = urllib.quote_plus(search_string.encode('utf-8'))
        return search_string

    @staticmethod
    def download_tweets(search_string, language):
        """Returns list of <count> tweets containing <search_string>"""

        search_string = TweetDownloader.preprocess_search_string(search_string)
        try:
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

            return ts.searchTweetsIterable(tso)

        except TwitterSearch.TwitterSearchException as e:
            print e

    @staticmethod
    def download_tweets_and_dump_to_file(search_string, language, count, filename):
        """Downloads <count> tweets and dumps them to <filename> file"""
        downloaded_tweets = TweetDownloader.download_tweets(search_string, language)
        tweets_to_dump = itertools.islice(downloaded_tweets, count)
        with codecs.open(filename, mode='w', encoding='utf-8') as f:
            f.write('[\n')
            for tweet in tweets_to_dump:
                f.write('\t{\n')
                f.write("\t\tuser: '%s'," % tweet['user']['screen_name'])
                f.write('\n')
                f.write("\t\ttext: '%s'," % tweet['text'])
                f.write('\n')
                f.write('\t}\n')
            f.write(']')


class TweetChunkIterator:
    def __init__(self, tweets_iterable, chunk_size):
        self.iterable = iter(tweets_iterable)
        self.chunk_size = chunk_size
        self.start = 0

    def __iter__(self):
        return self.iterable

    def next(self):
        return next(self.iterable)

    def get_chunk(self):
        """Returns a list of <self.chunk_size> sized chunks of tweets extracted from <self.iterable>"""
        result = list(itertools.islice(self.iterable, self.start, self.start + self.chunk_size))
        self.start += self.chunk_size
        return result