import factory

from django.contrib.auth.models import User


class UserFactory(factory.Factory):
  FACTORY_FOR = User
  
  username = factory.sequence(lambda n: 'alfred{0}'.format(n))
  first_name = factory.sequence(lambda n: 'Alfred{0}'.format(n))
  last_name = factory.sequence(lambda n: 'Bloomf{0}'.format(n))
  email = factory.sequence(lambda n: 'example{0}@example.org'.format(n))
  

class SuperUserFactory(factory.Factory):
  FACTORY_FOR = User
  
  username = factory.sequence(lambda n: 'rufus{0}'.format(n))
  first_name = factory.sequence(lambda n: 'Rufus{0}'.format(n))
  last_name = factory.sequence(lambda n: 'Wurtenberger{0}'.format(n))
  email = factory.sequence(lambda n: 'superexample{0}@example.org'.format(n))
  is_superuser = True