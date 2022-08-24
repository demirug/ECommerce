from django.http import HttpResponse
from django.shortcuts import render

from apps.orders.constants import OrderStatus
from apps.orders.services.delivery.constants import DeliveryMethod
from apps.orders.services.payment.model import IPaymentType
from apps.orders.signals import payment_done


class CashOnDelivery(IPaymentType):

    def handle_get(self, obj, request) -> HttpResponse:
        return self.handle_post(obj, request)

    def handle_post(self, obj, request) -> HttpResponse:
        if obj.status == OrderStatus.NEW:
            obj.status = OrderStatus.PAYED
            obj.track = DeliveryMethod[obj.delivery_service].values[0].generate_document(obj, obj.track)
            obj.save()
            payment_done.send(obj)
        return render(request, "orders/payment/cash_on_delivery.jinja", {"track": obj.track})
