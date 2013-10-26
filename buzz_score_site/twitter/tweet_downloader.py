__author__ = 'nikita_kartashov'

import TwitterSearch
import itertools
import urllib

CONSUMER_KEY = "qaxwA1MNvx2ilaBQaql4g"
CONSUMER_SECRET = "ok5l42lywxjEeh460xTy8EMUUQzMkVBhorITv82Yc"

TOKEN_KEY = "115023328-B3LMKWYXNS86M5YiS7BT8CSAvTFR8E9thUYIzGmd"
TOKEN_SECRET = "wgcM1iAZPvuSZBogjtEJ3B5VZRCb3vwCnBqqi9EGgA"


def preprocess_search_string(search_string):
    """Returns list containing preprocessed <search_string> for using in net queries"""

    search_string = urllib.quote_plus(search_string)
    return [search_string]


def download_tweets(search_string, language):
    """Returns list of <count> tweets containing <search_string>"""

    search_string = preprocess_search_string(search_string)

    try:
        tso = TwitterSearch.TwitterSearchOrder()
        tso.setKeywords(search_string)
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