import factory

from tasks.models import Task


class TaskFactory(factory.Factory):
  FACTORY_FOR = Task
  
  description = factory.sequence(lambda n: 'This is a description...{0}'.format(n))
  priority = 1