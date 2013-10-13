__author__ = 'nikita_kartashov'

import TwitterSearch

CONSUMER_KEY = "qaxwA1MNvx2ilaBQaql4g"
CONSUMER_SECRET = "ok5l42lywxjEeh460xTy8EMUUQzMkVBhorITv82Yc"

TOKEN_KEY = "115023328-B3LMKWYXNS86M5YiS7BT8CSAvTFR8E9thUYIzGmd"
TOKEN_SECRET = "wgcM1iAZPvuSZBogjtEJ3B5VZRCb3vwCnBqqi9EGgA"


def download_tweets(search_string, language, count=100):
    try:
        tso = TwitterSearch.TwitterSearchOrder()
        tso.setKeywords(search_string)
        tso.setLanguage(language)
        tso.setCount(100)
        tso.setIncludeEntities(False)

        # create a TwitterSearch object with our secret tokens
        ts = TwitterSearch.TwitterSearch(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=TOKEN_KEY,
            access_token_secret=TOKEN_SECRET
        )

        result = []
        for i, tweet in enumerate(ts.searchTweetsIterable(tso)):
            if i == count:
                break
            result.append(tweet)

        return result
    except TwitterSearch.TwitterSearchException as e:
        print e