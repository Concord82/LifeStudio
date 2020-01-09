from tokenize import blank_re

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
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
    reg = re.compile('^\d{6}$|^[9]\d{9}$|^[7-8][9]\d{9}$|^\+[7][3,9]\d{9}$')
    if not reg.match(value):
        raise ValidationError(_(u'%s hashtag doesnot comply' % value))


class Offices(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name=_('Office Name'),
        help_text=_('Set office name')
    )
    short_code = models.CharField(
        max_length=5,
        verbose_name=_('Short Code'),
        help_text=_('Set Short code for current office')
    )
    address = models.TextField(
        verbose_name=_('Place Affress Ofice'),
        blank=True
    )
    twoGisCode = models.TextField(
        verbose_name=_('2gis site code'),
        help_text=_('Set 2gis code for curent place'),
        blank=True
    )
    phone = models.CharField(
        verbose_name=_('Phone Number'),
        max_length=12,
        unique=True,
        validators=[validate_phone],
        blank=True
    )
    work_time_start = models.TimeField(
        verbose_name=_('Work Time Start'),
        default=timezone.now
    )
    work_time_end = models.TimeField(
        verbose_name=_('Work Time End'),
        default=timezone.now
    )
    return_time_start = models.TimeField(
        verbose_name=_('Start Time Return'),
        default=timezone.now,
        blank=True
    )
    view_on_front = models.BooleanField(
        verbose_name=_('view on frontend'),
        default=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Ofice')
        verbose_name_plural = _(u'Ofices')


class WorkType(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name=_('Name Work Type')
    )
    description = models.CharField(
        max_length=256,
        verbose_name=_('Description for work type'),
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Work Type')
        verbose_name_plural = _(u'Works Type')

UnitList = (
    ('1', 'кв.м.'),
    ('2', 'шт.'),
)

class WorksList(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name=_('Work Name')
    )
    workType = models.ForeignKey(
        to=WorkType,
        on_delete=models.CASCADE,
    )
    unit = models.CharField(
        verbose_name=_('unit'),
        max_length=10,
        choices=UnitList
    )
    price = models.DecimalField(
        verbose_name=_('Price'),
        max_digits=10,
        decimal_places=2
    )
    master_percent = models.PositiveSmallIntegerField(
        verbose_name=_('master Percent'),
    )
    admin_percent = models.PositiveSmallIntegerField(
        verbose_name=_('Admin Percent'),
    )
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Work')
        verbose_name_plural = _(u'Works List')

class Clients(models.Model):
    last_name = models.CharField(
        verbose_name=_('Last Name User'),
        max_length=64,
    )
    first_name = models.CharField(
        verbose_name=_('First Name User'),
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
        blank=True
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
    lastAction = models.DateTimeField(
        verbose_name=_('Last Action Data'),
        blank=True,
        null=True
    )
    comment = models.TextField(
        verbose_name=_('Comment'),
        blank=True
    )

    def get_full_name(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name
    get_full_name.short_description = _('Full Name User')

    def get_short_name(self):
        return self.last_name + ' ' + self.first_name[0] + '.' + self.middle_name[0] + '.'
    get_short_name.short_description = _('Short Name User')

    def get_phone_number(self):
        if self.phone[0:6] == '+73822':
            return '+7 (3822) ' + self.phone[6:9] + '-' + self.phone[9:]
        else:
            return self.phone[0:2] + '-' + self.phone[2:5] + '-' + self.phone[5:8] + '-' + self.phone[8:]

    get_phone_number.short_description = _('Phone Number')

    def comment_preview(self):
        coment_list = self.comment.split(' ')
        if len(coment_list) > 5:
            return ' '.join(coment_list[:5])
        else:
            return self.comment

    def clean(self):
        if len(self.phone) == 6:
            self.phone = '+73822' + self.phone
        elif len(self.phone) == 10:
            self.phone = '+7' + self.phone
        elif len(self.phone) == 11:
            if self.phone[0] == '7' or self.phone[0] == '8':
                self.phone = '+7' + self.phone[1:]


    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.middle_name = self.middle_name.capitalize()
        super(Clients, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_short_name()

    class Meta:
        verbose_name = _(u'Client')
        verbose_name_plural = _(u'Clients')
