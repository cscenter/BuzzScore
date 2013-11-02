from django.shortcuts import render

from forms import EmotionalEvaluationForm
from twitter.TweetDownloader import TweetDownloader, TweetChunkIterator

# Later will be replaced with calls to memcache
storage = {}

ITEMS_PER_PAGE = 20


def index(request):
    form = EmotionalEvaluationForm()
    return render(request, 'index.html', {'form': form})


def tweets_ajax(request):
    if not request.is_ajax():
        form = EmotionalEvaluationForm()
        return render(request, 'index.html', {'form': form})
    session_id = request.COOKIES['JSESSIONID']
    downloaded_tweets = storage[session_id]
    if not downloaded_tweets:
        form = EmotionalEvaluationForm()
        return render(request, 'index.html', {'form': form})
    items = downloaded_tweets.get_chunk()
    return render(request, 'tweets_page.html', {'tweets': items,
                                                'ITEMS_PER_PAGE': ITEMS_PER_PAGE})


def tweets(request):
    form = EmotionalEvaluationForm(request.POST)
    if form.is_valid():
        post = form.cleaned_data
        downloaded_tweets = TweetDownloader.download_tweets(post['search_query'], post['search_language'])
        session_id = request.COOKIES['JSESSIONID']
        storage[session_id] = TweetChunkIterator(downloaded_tweets, ITEMS_PER_PAGE)
        items = storage[session_id].get_chunk()
        return render(request, 'tweets_index.html', {'tweets': items,
                                                     'ITEMS_PER_PAGE': ITEMS_PER_PAGE})
    else:
        return render(request, 'index.html', {'form': form})