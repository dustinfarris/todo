from django.contrib.auth.models import User
from django.db import models


PRIORITY_OPTIONS = [
  (1, 'Low'),
  (2, 'Medium'),
  (3, 'High'),
]


class Task(models.Model):
  user = models.ForeignKey(User, related_name='tasks')
  created_at = models.DateTimeField(auto_now_add=True)
  modified_on = models.DateTimeField(auto_now=True)
  description = models.CharField(max_length=255)
  priority = models.SmallIntegerField(choices=PRIORITY_OPTIONS)
  
  class Meta:
    ordering = ('-priority',)
  
  @models.permalink
  def get_absolute_url(self):
    return ('tasks:show', [], {'pk': str(self.id)})