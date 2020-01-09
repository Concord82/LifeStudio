from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
# Create your models here.

def validate_phone(value):
    import re
    '''
    Номер телефона должен быть:
    ^\d{6}$ - только цифры 6 знаков для городских номеров
    ^[9]\d{9}$ - 10 цифр начинается на девятку
    ^[7-8][9]\d{9}$ - 11 цифр начинается на 7 или 8 потом 9 и еще 9 знаков
    ^\+[7][9]\d{9}$ - 12 знаков в федеральном формате на +7 
    '''
    reg = re.compile('^\d{6}$|^[9]\d{9}$|^[7-8][9]\d{9}$|^\+[7][9]\d{9}$')
    if not reg.match(value):
        raise ValidationError(_(u'%s hashtag doesnot comply' % value))


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
        max_length=12,
        unique=True,
        validators=[validate_phone]
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

    def save(self, *args, **kwargs):
        if len(self.phone) == 6:
            self.phone = '+73822' + self.phone
        elif len(self.phone) == 10:
            self.phone = '+7' + self.phone
        elif len(self.phone) == 11:
            if self.phone[0] == '7' or self.phone[0] == '8':
               self.phone = '+7' + self.phone[1:]
        '''    else:
                raise ValueError(_('Phone number should start 7 or 8'))
        elif len(self.phone) == 12:
            if self.phone[0:2] != '+7':
                raise ValueError(_('Phone number should start +7 or +8'))
        else:
            raise ValueError(_('Phone number format is not valid')) '''
        super(MyUser, self).save(*args, **kwargs)



    class Meta:
        verbose_name = _(u'User')
        verbose_name_plural = _(u'Users')