from django.contrib import admin
from solo.admin import SingletonModelAdmin

from apps.orders.models import Order, OrderSettings

admin.site.register(Order)
admin.site.register(OrderSettings, SingletonModelAdmin)
