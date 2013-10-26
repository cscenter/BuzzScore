from django.shortcuts import render
from itertools import islice

from forms import EmotionalEvaluationForm
from twitter.tweet_downloader import download_tweets

# Later will be replaced with calls to memcache
storage = {}

ITEMS_PER_PAGE = 20


def index(request):
    form = EmotionalEvaluationForm()
    return render(request, 'index.html', {'form': form})


def tweets(request):
    if request.is_ajax():
        session_id = request.COOKIES['JSESSIONID']
        downloaded_tweets = storage[session_id]
        items = []
        for i in range(ITEMS_PER_PAGE):
            items.append(downloaded_tweets.next())
        storage[session_id] = downloaded_tweets
        return render(request, 'tweets_page.html', {'tweets': items,
                                                    'ITEMS_PER_PAGE': ITEMS_PER_PAGE})
    form = EmotionalEvaluationForm(request.POST)
    if form.is_valid():
        post = form.cleaned_data
        downloaded_tweets = download_tweets(post['search_query'],
                                            post['search_language'])
        session_id = request.COOKIES['JSESSIONID']
        items = list(islice(downloaded_tweets, ITEMS_PER_PAGE))
        storage[session_id] = downloaded_tweets
        return render(request, 'tweets_index.html', {'tweets': items,
                                                     'ITEMS_PER_PAGE': ITEMS_PER_PAGE})
    else:
        return render(request, 'index.html', {'form': form})