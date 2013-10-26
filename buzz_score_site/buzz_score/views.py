from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, render

from forms import EmotionalEvaluationForm
from twitter.tweet_downloader import download_tweets


def index(request):
    form = EmotionalEvaluationForm()
    return render(request, 'index.html', {'form': form})


def tweets(request):
    form = EmotionalEvaluationForm(request.POST)
    if form.is_valid():
        post = form.cleaned_data
        downloaded_tweets = download_tweets(post['search_query'],
                                            post['search_language'],
                                            int(post['number_of_results']))
        return render(request, 'tweets.html', {'tweets': downloaded_tweets})
    else:
        return render(request, 'index.html', {'form': form})
