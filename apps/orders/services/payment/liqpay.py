from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.orders.constants import OrderStatus
from apps.orders.models import Order
from apps.orders.services.delivery.constants import DeliveryMethod
from apps.orders.services.payment.model import IPaymentType
from apps.orders.signals import payment_done
from liqpay import LiqPay


class LiqPayDelivery(IPaymentType):

    def handle_get(self, obj: Order, request) -> HttpResponse:
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': float(obj.cost),
            'currency': settings.CURRENCY,
            'description': _('Payment for order #%s') % obj.pk,
            'order_id': int(obj.pk),
            'version': '3',
            'sandbox': int(settings.LIQPAY_SANDBOX),
            'server_url': '{domain}{path}'.format(
                domain=Site.objects.get_current().domain,
                path=reverse("orders:pay", kwargs={"uuid": obj.uuid})
            ),
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)

        return render(request, "orders/payment/liqpay.jinja", {'signature': signature, 'data': data})

    def handle_post(self, obj, request) -> HttpResponse:
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        if sign == signature:  # If signature correct
            response = liqpay.decode_data_from_str(data)
            if response['order_id'] == str(obj.id):  # If order id correct
                obj.status = OrderStatus.PAYED
                obj.track = DeliveryMethod[obj.delivery_service].values[0].generate_document(obj, obj.track)
                obj.save()
                payment_done.send(obj)
        return HttpResponse()
