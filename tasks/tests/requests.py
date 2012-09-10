import logging

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from factories import TaskFactory
from tasks.models import Task


logger = logging.getLogger(__name__)


class TaskPages(TestCase):
  def setUp(self):
    self.paul = User.objects.create_user('paul', 'paul@example.org', 'paulpassword')
    self.tom = User.objects.create_user('tom', 'tom@example.org', 'tompassword')
    for _ in range(20):
      TaskFactory(user=self.paul)
      TaskFactory(user=self.tom)
  
  def test_index(self):
    self.client.login(username='paul', password='paulpassword')
    response = self.client.get(reverse('tasks:index'))
    
    for task in self.paul.tasks.all():
      self.assertContains(response, task.description)
    
    for task in self.tom.tasks.all():
      self.assertNotContains(response, task.description)
  
  def test_create(self):
    total_tasks = Task.objects.count()
    data = {
      'description': 'Sample task',
      'priority': 2,
    }
    self.client.login(username='paul', password='paulpassword')
    response = self.client.post(reverse('tasks:create'), data)
    
    self.assertEqual(Task.objects.count(), total_tasks + 1)
  
  def test_delete(self):
    total_tasks = Task.objects.count()
    data = {'_method': 'delete'}
    task = self.paul.tasks.all()[0]
    self.client.login(username='paul', password='paulpassword')
    response = self.client.post(reverse('tasks:destroy', kwargs={'pk': str(task.pk)}), data)
    
    self.assertRedirects(response, reverse('tasks:index'))
    self.assertEqual(Task.objects.count(), total_tasks - 1)
  
  def test_update(self):
    data = {'description': 'BIG CHANGE', 'priority': 2, '_method': 'put'}
    task = self.paul.tasks.all()[0]
    self.client.login(username='paul', password='paulpassword')
    response = self.client.post(reverse('tasks:update', kwargs={'pk': str(task.pk)}), data)
    task = Task.objects.get(id=task.id)
    
    self.assertEqual(task.description, 'BIG CHANGE')
    self.assertRedirects(response, reverse('tasks:show', kwargs={'pk': str(task.pk)}))