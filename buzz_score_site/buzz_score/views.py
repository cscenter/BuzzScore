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
    try:
        downloaded_tweets = storage[session_id]

        items = downloaded_tweets.get_chunk()
        return render(request, 'tweets_page.html', {'tweets': items,
                                                    'ITEMS_PER_PAGE': ITEMS_PER_PAGE})
    except KeyError:
        form = EmotionalEvaluationForm()
        return render(request, 'index.html', {'form': form})


def tweets(request):
    form = EmotionalEvaluationForm(request.POST)
    if form.is_valid():
        post = form.cleaned_data
        downloaded_tweets = TweetDownloader.download_tweets(post['search_query'], post['search_language'])
        try:
            session_id = request.COOKIES['JSESSIONID']
            storage[session_id] = TweetChunkIterator(downloaded_tweets, ITEMS_PER_PAGE)
            items = storage[session_id].get_chunk()
            return render(request, 'tweets_index.html', {'tweets': items,
                                                         'ITEMS_PER_PAGE': ITEMS_PER_PAGE})
        except KeyError:
            return cookies_and_something_else_error(request)
        except Exception:
            return cookies_and_something_else_error(request, additional_stuff_to_turn_on='and javascript')
    else:
        return render(request, 'index.html', {'form': form})


def csrf_failure(request, reason):
    return cookies_and_something_else_error(request)


def cookies_and_something_else_error(request, additional_stuff_to_turn_on=''):
    return render(request, 'error.html',
                  {'error_text': 'You need cookies %s turned on to use our awesome site!' % additional_stuff_to_turn_on})