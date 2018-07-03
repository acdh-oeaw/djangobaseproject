from django.contrib import admin
from .models import Book, Reference


class BookAdmin(admin.ModelAdmin):
    search_fields = [
        'zoterokey', 'item_type', 'author', 'title', 'publication_title',
        'publication_year', 'isbn', 'url'
    ]
    list_display = [
        'zoterokey', 'item_type', 'author', 'title', 'publication_title',
        'publication_year', 'isbn', 'url'
    ]


class ReferenceAdmin(admin.ModelAdmin):
    search_fields = ['id', 'zotero_item', 'page']
    list_display = ['id', 'zotero_item', 'page']


admin.site.register(Book, BookAdmin)
admin.site.register(Reference, ReferenceAdmin)

# Register your models here.
