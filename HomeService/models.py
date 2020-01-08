from tokenize import blank_re

from django.db import models
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
    reg = re.compile('^\d{6}$|^[9]\d{9}$|^[7-8][9]\d{9}$|^\+[7][9]\d{9}$')
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