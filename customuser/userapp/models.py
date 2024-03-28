from django.db import models
from django.contrib.auth.models import AbstractUser,Permission,Group
from django.utils.translation import gettext_lazy as _

class NewUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    about = models.TextField(_('about'), max_length=500, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Dealer(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, related_name='dealers')
    user_permissions = models.ManyToManyField(Permission, related_name='dealers')

    def __str__(self):
        return self.name
