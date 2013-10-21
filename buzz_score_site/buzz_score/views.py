from django.http import HttpResponse
from twitter.tweet_downloader import download_tweets


def hello(request):
    return HttpResponse("Hello world")


def tweets(request, s_str, lang, count):
    downloaded_tweets = download_tweets(s_str, lang, int(count))
    html = "<html><body> Tweets with string %s in lang %s <br><p>" % (s_str, lang)

    html += "</p><p>".join(["@%s tweeted %s " % (tweet["user"]['screen_name'], tweet["text"])
                            for tweet in downloaded_tweets])

    #html += "@%s tweeted %s </br>" % (tweet["user"]["screen_name"], tweet["text"])

    html += "</p></body></html>"
    return HttpResponse(html)
