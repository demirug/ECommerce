import uuid

from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.orders.constants import OrderStatus
from apps.orders.services.delivery.constants import DeliveryMethod
from apps.orders.services.payment.constants import PaymentMethod
from apps.products.models import Product


class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    status = models.CharField(_("Status"), max_length=15, choices=OrderStatus.choices, default=OrderStatus.NEW)
    cost = models.DecimalField(_("Cost"), max_digits=5, decimal_places=1)

    first_name = models.CharField(_("First name"), max_length=100)
    second_name = models.CharField(_("Second name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    phone_number = models.CharField(validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$',
                       message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed"))],
        max_length=17, blank=True)

    date = models.DateTimeField(default=timezone.now)

    note = models.TextField(blank=True, default="")

    payment_service = models.CharField(max_length=50, default=PaymentMethod.NONE.name)
    delivery_service = models.CharField(max_length=50, default=DeliveryMethod.NONE.name)
    track = models.CharField(max_length=999, default="")

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{self.first_name} {self.second_name} | {self.cost} {settings.CURRENCY}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    count = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"
