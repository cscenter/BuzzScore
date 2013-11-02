from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'buzz_score.views.index'),
    url(r'^tweets/$', 'buzz_score.views.tweets'),
    url(r'^tweets_ajax/$', 'buzz_score.views.tweets_ajax'),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
