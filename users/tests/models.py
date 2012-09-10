import logging

from django.contrib.auth.models import User
from django.test import TestCase


logger = logging.getLogger(__name__)


class UserModel(TestCase):
  def setUp(self):
    self.fields = [f.__dict__['name'] for f in User._meta.fields]
  
  def test_fields(self):
    self.assertIn('username', self.fields)
    self.assertIn('first_name', self.fields)
    self.assertIn('last_name', self.fields)
    self.assertIn('email', self.fields)
    self.assertIn('password', self.fields)