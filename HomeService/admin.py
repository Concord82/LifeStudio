from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
# Register your models here.

from .models import Offices, WorkType, WorksList, Clients

class OfficesAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_code', 'address','phone','view_on_front',)


admin.site.register(Offices, OfficesAdmin)

@admin.register(Clients)
class AdminClients(admin.ModelAdmin):
    list_display = ('get_short_name','get_phone_number',)
    fieldsets = (
                    (_('Personal info'),{'fields':(
                        ('last_name',
                        'first_name',
                        'middle_name'),
                        'phone',
                    )}),
                    (_('Other info'), {'fields':(
                        ('email',
                        'address'),
                        'birthDay',
                        'comment',
                        ('creationData',
                        'lastAction')
                    )})
    )
    readonly_fields = ['creationData','lastAction',]
    search_fields = ('last_name','phone')
    list_filter = ('lastAction',)


@admin.register(WorkType)
class AdminWorkType(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)


@admin.register(WorksList)
class AdminWorksList(admin.ModelAdmin):
    list_display = ('name', 'workType','unit', 'price')
    list_filter = ('workType',)
    search_fields = ('name',)
    autocomplete_fields = ('workType',)