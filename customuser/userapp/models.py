from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Permission, Group
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    """
    A custom manager for handling user creation.
    """

    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        """
        Creates and saves a superuser with the given email, username, first name, and password.
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):
        """
        Creates and saves a user with the given email, username, first name, and password.
        """
        if not email:
            raise ValueError(_('You must provide an email address.'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model with email-based authentication.
    """
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_name

class Dealer(models.Model):
    """
    A model representing a dealer.
    """
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, related_name='dealers')
    user_permissions = models.ManyToManyField(Permission, related_name='dealers')

    def __str__(self):
        return self.name
