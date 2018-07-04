from django.contrib import admin
from .models import ZotItem


class ZotItemAdmin(admin.ModelAdmin):
    search_fields = [
        'zot_key',
        'zot_creator',
        'zot_date',
        'zot_version'
    ]
    list_display = [
        'zot_key',
        'zot_creator',
        'zot_date',
        'zot_version'
    ]


admin.site.register(ZotItem, ZotItemAdmin)
