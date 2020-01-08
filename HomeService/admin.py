from django.contrib import admin

# Register your models here.

from .models import Offices, WorkType

class OfficesAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_code', 'address','phone','view_on_front',)


admin.site.register(Offices, OfficesAdmin)


@admin.register(WorkType)
class AdminWorkType(admin.ModelAdmin):
    list_display = ('name', 'description',)