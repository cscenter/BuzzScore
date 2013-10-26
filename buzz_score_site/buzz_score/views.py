from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from forms import EmotionalEvaluationForm
from buzz_score_site.twitter.tweet_downloader import download_tweets

from os.path import abspath


def index(request):
    args = {'form': EmotionalEvaluationForm()}
    args.update(csrf(request))
    return render_to_response(abspath('buzz_score/templates/index.html'), args)


def tweets(request):
    if request.method == "POST":
        form = EmotionalEvaluationForm(request.POST)
        if form.is_valid():
            post = form.cleaned_data
            downloaded_tweets = download_tweets(post['search_query'],
                                                post['search_language'],
                                                int(post['number_of_results']))
            return render_to_response(abspath('buzz_score/templates/tweets.html'), {'tweets': downloaded_tweets})
        else:
            return render_to_response(abspath('buzz_score/templates/error.html'),
                                      {'error_text': "The form was filled incorrectly"})
    else:
        return render_to_response(abspath('buzz_score/templates/error.html'),
                                      {'error_text': "The form was filled"})
