from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from apps.menu.models import Element


@admin.register(Element)
class MenuAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'url', 'position', 'enabled')
    list_filter = ('position', 'enabled',)
