import logging

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from factories import UserFactory, SuperUserFactory


logger = logging.getLogger(__name__)


class UserPages(TestCase):
  def setUp(self):
    self.user = UserFactory()
    self.user.set_password('asdf')
    self.user.save()
    self.superuser = SuperUserFactory()
    self.superuser.set_password('asdf')
    self.superuser.save()
    
  def test_new_page(self):
    response = self.client.get(reverse('users:new'))
    
    self.assertContains(response, '<h1>New User</h1>', html=True)
  
  def test_edit_page(self):
    self.assertTrue(self.client.login(username=self.user.username, password='asdf'))
    response = self.client.get(reverse('users:edit', kwargs={'pk': self.user.pk}), follow=True)

    self.assertContains(response, '<h1>Edit %s</h1>' % self.user.username, html=True)
  
  def test_if_superuser(self):  
    self.client.login(username=self.superuser.username, password='asdf')
    response = self.client.get(reverse('users:index'))
    
    self.assertContains(response, self.user.username)
    self.assertContains(response, reverse('users:show', kwargs={'pk': self.user.pk}))
  
  def test_create_a_user(self):
    total_users = User.objects.count()
    data = {
      'username': 'testonly',
      'first_name': 'Test',
      'last_name': 'User',
      'email': 'test@example.org',
      'password1': 'asdf',
      'password2': 'asdf',
    }
    response = self.client.post(reverse('users:create'), data)
    
    self.assertEqual(User.objects.count(), total_users + 1)

  def test_detail_if_correct_user(self):
    response = self.client.get(reverse('users:show', kwargs={'pk': self.user.pk}))
    
    self.assertContains(response, self.user.first_name)
  
  def test_update_if_correct_user(self):
    data = {
      'first_name': 'Attempted change',
      'last_name': self.user.last_name,
      'email': self.user.email,
      '_method': 'put',
    }
    self.client.login(username=self.user.username, password='asdf')
    response = self.client.post(reverse('users:update', kwargs={'pk': self.user.pk}), data)
    
    self.assertRedirects(response, reverse('users:show', kwargs={'pk': self.user.pk}))
    self.assertEqual(self.user.first_name, 'Attempted change')
    
  def test_delete_if_correct_user(self):
    new_user = UserFactory()
    new_user.set_password('asdf')
    new_user.save()
    total_users = User.objects.count()
    self.client.login(username=new_user.username, password='asdf')
    response = self.client.post(reverse('users:destroy', kwargs={'pk': new_user.pk}), {'_method': 'delete'})
    
    self.assertRedirects(response, reverse('home'))
    self.assertEqual(User.objects.count(), total_users - 1)
  
  def test_if_not_logged_in(self):
    response = self.client.get(reverse('users:index'))
    
    self.assertRedirects(response, '%s?next=/users/' % reverse('login'))
  
  def test_if_not_superuser(self):
    self.client.login(username=self.user.username, password='asdf')
    index_response = self.client.get(reverse('users:index'))
    
    self.assertEqual(index_response.status_code, 403)
  
  def test_if_not_correct_user(self):
    wrong_user = UserFactory()
    wrong_user.set_password('asdf')
    wrong_user.save()
    self.client.login(username=wrong_user.username, password='asdf')
    detail_response = self.client.get(reverse('users:show', kwargs={'pk': self.user.pk}))
    data = {
      'first_name': 'Attempted change',
      'last_name': ':):)',
      'email': 'new@email.org',
      '_method': 'put',
    }
    update_response = self.client.post(reverse('users:update', kwargs={'pk': self.user.pk}), data)
    delete_response = self.client.post(reverse('users:destroy', kwargs={'pk': self.user.pk}), {'_method': 'delete'})
    
    self.assertEqual(update_response.status_code, 403)
    self.assertEqual(delete_response.status_code, 403)