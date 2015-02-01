
"""
URL mappings
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from beast import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)

