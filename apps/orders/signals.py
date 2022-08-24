from django import dispatch
from django.contrib.sites.models import Site
from django.dispatch import receiver

from apps.orders.models import OrderSettings, Order
from shared.services.email import send_email

payment_done = dispatch.Signal()


@receiver(payment_done)
def onPaymentDone(sender: Order, **kwargs):
    settings: OrderSettings = OrderSettings.get_solo()
    items: str = ""
    for item in sender.items.all():
        items += settings.item_format.format(
            url="{site}{path}".format(site=Site.objects.get_current().domain, path=item.product.get_absolute_url()),
            name=item.product.name,
            image="{site}{path}".format(site=Site.objects.get_current().domain, path=item.product.get_image()),
            price=item.product.price,
            count=item.count,
            totalPrice=item.count * item.product.price
        )

    title: str = settings.order_payed_mail_title.format(number=sender.pk)
    message: str = settings.order_payed_mail.format(number=sender.pk, total_price=sender.cost, items=items, track=sender.track)

    send_email(sender.email, title, message)
