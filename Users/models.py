from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, login_name, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not login_name:
            raise ValueError(_('Users must have an login'))

        user = self.model(
            login_name=login_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_name, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            login_name,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    login_name = models.CharField(
        verbose_name=_('user login'),
        max_length=32,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=_('First Name User'),
        max_length=64,
    )
    last_name= models.CharField(
        verbose_name=_('Last Name User'),
        max_length=64,
    )
    middle_name = models.CharField(
        verbose_name=_('Middle Name User'),
        max_length=64,
    )
    phone = models.CharField(
        verbose_name=_('Phone Number'),
        max_length=10,
        unique=True
    )
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=32,
        unique=True,
    )
    address = models.CharField(
        verbose_name=_('Address'),
        max_length=64,
        blank=True
    )
    birthDay = models.DateField(
        verbose_name=_('User BirthDay'),
        blank=True,
        null=True
    )
    creationData = models.DateTimeField(
        verbose_name=_('Registration Data'),
        auto_now_add=True
    )
    photo = models.ImageField(
        verbose_name=_('Photo'),
        upload_to='uploads/%Y/%m/%d/',


    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'login_name'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_short_name(self):
        # The user is identified by their email address
        if self.first_name != '' and self.middle_name != '' and self.last_name != '':
            return self.last_name + ' ' + self.first_name[0] + '.' + self.middle_name[0] + '.'
        else:
            return self.login_name

    def __str__(self):  # __unicode__ on Python 2
        return self.login_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin