from django.conf.urls import patterns, url
from buzz_score.views import tweets
from buzz_score.views import index
from buzz_score.views import more_tweets

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^tweets/(?P<page>\d+)/$', more_tweets),
    url(r'^tweets', tweets),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
