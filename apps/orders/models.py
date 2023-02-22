import uuid

from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

from apps.orders.constants import OrderStatus
from apps.products.models import Product


class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    status = models.CharField(_("Status"), max_length=15, choices=OrderStatus.choices, default=OrderStatus.NEW)
    cost = models.DecimalField(_("Cost"), max_digits=5, decimal_places=1)

    first_name = models.CharField(_("First name"), max_length=100)
    second_name = models.CharField(_("Second name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    email = models.EmailField(_("Email"), default="")
    phone_number = models.CharField(validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$',
                       message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed"))],
        max_length=17, blank=True)

    date = models.DateTimeField(default=timezone.now)

    note = models.TextField(blank=True, default="")

    payment_service = models.CharField(max_length=50, default="NONE")
    payment_data = models.CharField(max_length=999, null=True)
    delivery_service = models.CharField(max_length=50, default="NONE")
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


class OrderSettings(SingletonModel):
    item_format = models.TextField(_("Item mail format"),
                                   default="<a href='{url}'>{name}</a>" +
                                           "<img src='{image}'/>" +
                                           "<p>{count} x {price} {totalPrice}</p>" +
                                           "<hr>")

    new_order_mail_title = models.CharField(_("Title for new order email"),
                                            max_length=100, default="New order #{number}")

    new_order_mail = models.TextField(_("New order email"), default="<h1>New order #{number}</h1>" +
                                                                    "<p>Thanks for order</p>" +
                                                                    "{items}" +
                                                                    "<p>Price: {total_price}</p>" +
                                                                    "<p>With love your-site-name</p>")

    order_payed_mail_title = models.CharField(_("Title for payed order email"),
                                              max_length=100, default="Order #{number} payed")

    order_payed_mail = models.TextField(_("Order payed email"), default="<h1>Order #{number} payed</h1>" +
                                                                        "<p>Your order payed</p>" +
                                                                        "{items}" +
                                                                        "<p>Price: {total_price}</p>" +
                                                                        "{track}" +
                                                                        "<p>With love your-site-name</p>")

    novaposhta_weight = models.PositiveIntegerField(_("Parsel weight"), default=1)
    novaposhta_description = models.CharField(_("Description"), max_length=36, default="Order {number}")

    class Meta:
        verbose_name = "Order settings"

    def __str__(self):
        return ""
