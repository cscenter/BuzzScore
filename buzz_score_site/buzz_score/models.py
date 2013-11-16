# Create your models here.


class Tweet:
    _tweet_dict = {}

    @staticmethod
    def construct_tweet_collection(l):
        return [Tweet(item) for item in l]

    def __init__(self, tweet_dict):
        self._tweet_dict = tweet_dict

    def as_html(self):
        tweet_class = 'tweet '
        if 'sentiment' in self._tweet_dict.keys():
            tweet_class += self._tweet_dict['sentiment']
        output = '<div class="%s"' \
                 'favorited="%s" retweet_count="%s" is_retweet="%r">' \
                 '<p> @%s tweeted %s </p>' \
                 '</div>' % (tweet_class,
                             self._tweet_dict['favorited'],
                             self._tweet_dict['retweet_count'],
                             'retweeted_status' in self._tweet_dict.keys(),
                             self._tweet_dict['user']['screen_name'],
                             self._tweet_dict['text'])
        return output