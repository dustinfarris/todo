from django.conf.urls import patterns, url
from django.contrib.auth.models import User

from views import do, edit, new


urlpatterns = patterns('',
  url(r'^s/$', do, name='index'),
  url(r'^s\.json$', do, {'as_json': True}, name='index-as-json'),
  url(r'^s/$', do, name='create'),
  url(r'^s/new/$', new, name='new'),
  url(r'^/(?P<pk>\d+)/$', do, name='show'),
  url(r'^/(?P<pk>\d+)\.json$', do, {'as_json': True}, name='show-as-json'),
  url(r'^/(?P<pk>\d+)/$', do, name='update'),
  url(r'^/(?P<pk>\d+)/$', do, name='destroy'),
  url(r'^/(?P<pk>\d+)/edit/$', edit, name='edit'),
)