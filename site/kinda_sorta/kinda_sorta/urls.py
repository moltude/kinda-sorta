
"""
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from beast import views

urlpatterns = patterns('',

	url(r'^$', include('beast.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^results/$', views.results, name='results'),
    url(r'^error/$', views.error, name='error'),

)

# Taken from 
# http://stackoverflow.com/questions/9047054/heroku-handling-static-files-in-django-app
# to fix static resources issue
if not settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	)