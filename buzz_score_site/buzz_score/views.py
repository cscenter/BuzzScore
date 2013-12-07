from django.shortcuts import render
import logging
import traceback

from forms import EmotionalEvaluationForm
from twitter.tweet_downloader import TweetChunkIterator
from twitter.tweet_downloader import download_tweets
from twitter.tweet_downloader import add_sentiment_to_list

from functools import partial
from itertools import ifilterfalse
from spam.spam_classifier import is_spam

from sentiment.analysis import go

# Later will be replaced with calls to memcached
STORAGE = {}

ITEMS_PER_PAGE = 20
#Sessions expire in 5 minutes
SESSION_EXPIRY_TIME = 300


def index(request):
    request.session.set_expiry(SESSION_EXPIRY_TIME)
    form = EmotionalEvaluationForm()
    return render(request, 'index.html', {'form': form})


def tweets_ajax(request):
    if not request.is_ajax():
        form = EmotionalEvaluationForm()
        return render(request, 'index.html', {'form': form})
    session_id = request.session.session_key
    try:
        user_package = STORAGE[session_id]
        downloaded_tweets = user_package['it']
        language = user_package['it']
        items = downloaded_tweets.get_chunk()
        items = add_sentiment_to_list(items, language)
        return render(request, 'tweets_page.html', {'tweets': items})
    except KeyError:
        form = EmotionalEvaluationForm()
        return render(request, 'index.html', {'form': form})


def tweets(request):
    form = EmotionalEvaluationForm(request.POST)
    if form.is_valid():
        post = form.cleaned_data
        query = post['search_query']
        language = post['search_language']
        downloaded_tweets = download_tweets(query, language)
        downloaded_tweets = ifilterfalse(partial(is_spam, lang=language), downloaded_tweets)
        try:
            session_id = request.session.session_key
            try:
                STORAGE[session_id] = {'it': TweetChunkIterator(downloaded_tweets, ITEMS_PER_PAGE),
                                       'lang': language}
            except KeyError:
                logging.error('User with session_id %s has no stored tweets', session_id)
                return user_environment_error(request)

            items = STORAGE[session_id]['it'].get_chunk()
            items = add_sentiment_to_list(items, language)
            return render(request, 'tweets_index.html', {'tweets': items})

        except Exception as e:
            logging.exception("Unknown exception %s", e.message)
            logging.exception("Stack trace: %s", traceback.format_exc())
            return unknown_error(request)
    else:
        return render(request, 'index.html', {'form': form})


def csrf_failure(request, reason):
    return user_environment_error(request)


def user_environment_error(request):
    return render(request, 'error.html',
                  {'error_text': 'You need cookies and javascript turned on to use our awesome site!'})


def unknown_error(request):
    return render(request, 'error.html',
                  {'error_text': "We have no idea what is wrong, "
                                 "but it has probably been fixed by the time you have read this pointless message,"
                                 " why don't you try and start from the beginning?"})