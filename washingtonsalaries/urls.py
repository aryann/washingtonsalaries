from django.conf.urls import patterns
from django.conf.urls import  url

import views

urlpatterns = patterns('',
    url(r'^search$', views.search, name='search'),
)
