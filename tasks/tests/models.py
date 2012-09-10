import logging

from django.test import TestCase

from tasks.models import Task


logger = logging.getLogger(__name__)


class TaskModel(TestCase):
  def setUp(self):
    self.fields = [f.__dict__['name'] for f in Task._meta.fields]
  
  def test_fields(self):
    self.assertIn('description', self.fields)
    self.assertIn('priority', self.fields)
    self.assertIn('user', self.fields)
    self.assertIn('created_at', self.fields)
    self.assertIn('modified_on', self.fields)