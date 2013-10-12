from django.http import HttpResponse
from TwitterAPIWrapper.TweetDownloader import download_tweets

def hello(request):
    return HttpResponse("Hello world")

def tweets(request, s_str, lang, count):
    items = download_tweets([s_str], lang, int(count))
    html = "<html><body> Tweets with string %s in lang %s </br>" % (s_str, lang)

    counter = 0
    for tweet in items:
        html += "@%s tweeted %s </br>" % (tweet["user"]["screen_name"], tweet["text"])
        if counter > count:
            break

    html += "</body></html>"
    return HttpResponse(html)