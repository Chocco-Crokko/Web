from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from fl_askapp.models import Profile
from random import randint
from faker import Factory
import urllib.request
from django.core.files import File

class Command(BaseCommand):
    help = 'Creates users'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                action='store',
                dest='number',
                default=10,
                help='Number of users to add'
        )

    def handle(self, *args, **options):
        fake = Factory.create()

        number = int(options['number'])
        
        for i in range(0, number):
            profile = fake.simple_profile()

            u = User()
            u.username = profile['username']
            u.first_name = fake.first_name()
            u.last_name = fake.last_name()
            u.email = profile['mail']
            u.password = make_password('qwerty123')
            u.is_active = True
            u.is_superuser = False 
            u.save()

            up = Profile()
            up.user = u
            up.information = '%s [%s]' % (fake.company(), fake.catch_phrase())
            up.rating = randint(-100, 400)

            #image_url = 'http://api.adorable.io/avatars/100/%s.png' % u.username
            #content = urllib.request.urlretrieve(image_url)
            #up.avatar.save('%s.png' % u.username, File(open(content[0])), save=True)
            up.save()

            self.stdout.write('[%d] added user %s' % (u.id, u.username))
