from django.contrib import admin

# Register your models here.

from .models import Offices, WorkType, WorksList

class OfficesAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_code', 'address','phone','view_on_front',)


admin.site.register(Offices, OfficesAdmin)


@admin.register(WorkType)
class AdminWorkType(admin.ModelAdmin):
    list_display = ('name', 'description',)

@admin.register(WorksList)
class AdminWorksList(admin.ModelAdmin):
    list_display = ('name', 'workType','unit', 'price')
    list_filter = ('workType',)
    search_fields = ('name',)