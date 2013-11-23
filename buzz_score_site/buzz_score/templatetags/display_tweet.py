from django.template import Library
register = Library()

@register.inclusion_tag('tweet.html', takes_context=True)
def display_tweet(context):
    tweet = context['tweet']
    tweet_class = 'tweet '
    if 'sentiment' in tweet.keys():
        tweet_class += tweet['sentiment']
    return {
        'user': tweet['user']['screen_name'],
        'text': tweet['text'],
        'tweet_class': tweet_class,
        'is_retweet': 'retweeted_status' in tweet.keys(),
        'favorited': tweet['favorited'],
        'retweet_count': tweet['retweet_count']
    }