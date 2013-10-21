from django.conf.urls import patterns, include, url
from BuzzScore.views import hello
from BuzzScore.views import tweets

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^hello/$', hello),
    url(r'^tweets/(?P<s_str>\w*)/(?P<lang>\w*)/(?P<count>\d*)/$', tweets)
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
