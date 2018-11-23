from django.db import models
from django.conf import global_settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(global_settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='ref_from_set')
    user_to = models.ForeignKey(User, related_name='ref_to_set')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


User.add_to_class('following', models.ManyToManyField('self',
                                                      through=Contact,
                                                      related_name='followers',
                                                      symmetrical=False))
