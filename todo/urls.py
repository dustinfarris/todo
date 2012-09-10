from django.conf import settings
from django.conf.urls import patterns, include, url, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import direct_to_template


handler404 = 'todo.views.page_not_found'
handler500 = 'todo.views.server_error'
admin.autodiscover()


urlpatterns = patterns('',
  url(
    r'^$',
    direct_to_template,
    {'template': 'home.jade'},
    name='home'
  ),
  url(r'^login/$', csrf_exempt(login), {'template_name': 'login.jade'}, name='login'),
  url(r'^logout/$', csrf_exempt(logout), {'template_name': 'logout.jade'}, name='logout'),
  url(r'^task', include('tasks.urls', namespace='tasks')),
  url(r'^user', include('users.urls', namespace='users')),
  
  # Admin
  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
  url(r'^admin/', include(admin.site.urls)),
)

# Serve media files locally in DEBUG mode
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug error pages
if settings.DEBUG:
  urlpatterns += patterns('', url(r'^404/$', direct_to_template, {'template': '404.jade'}))
  urlpatterns += patterns('', url(r'^500/$', direct_to_template, {'template': '500.jade'}))
  