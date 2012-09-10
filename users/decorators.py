import logging
import base64

from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden


logger = logging.getLogger(__name__)


def http_basic_auth(func):
  def wrapper(request, *args, **kwargs):
    if request.META.get('HTTP_AUTHORIZATION', False):
      authtype, auth = request.META['HTTP_AUTHORIZATION'].split()
      auth = base64.b64decode(auth)
      username, password = auth.split(':')
      user = authenticate(username=username, password=password)
      if user is not None and user.is_active:
        login(request, user)
        request.user = user
      else:
        return HttpResponseForbidden()
    return func(request, *args, **kwargs)
  return wrapper
