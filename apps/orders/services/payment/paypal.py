import json
import requests
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from requests.auth import HTTPBasicAuth

from apps.orders.constants import OrderStatus
from apps.orders.models import Order
from apps.orders.services.delivery.constants import DeliveryMethod
from apps.orders.services.payment.model import IPaymentType
from apps.orders.signals import payment_done

token = None


class GetTokenError(Exception):
    pass


def get_token():
    res = requests.post("https://api-m.sandbox.paypal.com/v1/oauth2/token", data={"grant_type": "client_credentials"},
                        auth=HTTPBasicAuth(settings.PAYPAL_CLIENT, settings.PAYPAY_PASSWORD)
                        )
    print(res.status_code)
    if res.status_code == 200:
        return json.loads(res.content)['token_type'] + " " + json.loads(res.content)['access_token']
    raise GetTokenError("Can't get token. Check your credentials and ethernet connection")


def api_request(path, data={}):
    global token
    if token is None:
        token = get_token()

    result = requests.post("https://api-m.sandbox.paypal.com" + path, json=data, headers={"Authorization": token})

    # On token expired
    if result.status_code == 401:
        token = None
        return api_request(path, data)

    return result.status_code, json.loads(result.content)


def create_order(value: float, currency="USD"):
    return api_request("/v2/checkout/orders", data={"intent": "CAPTURE", "purchase_units": [{"amount": {"currency_code": currency, "value": str(value)}}]})[1]["id"]


def capture_payment(order_id):
    code, data = api_request(f"/v2/checkout/orders/{order_id}/capture")
    return code == 201 and data["status"] == "COMPLETED"


class PayPalPayment(IPaymentType):

    def generate_order(self, obj: Order):
        if obj.payment_data is None:
            obj.payment_data = create_order(obj.cost, settings.CURRENCY)
            obj.save()

    def handle_get(self, obj: Order, request: WSGIRequest) -> HttpResponse:
        self.generate_order(obj)
        return render(request, "orders/payment/paypal.jinja", {"object": obj, "paypal_client": settings.PAYPAL_CLIENT})

    def handle_post(self, obj: Order, request: WSGIRequest) -> HttpResponse:
        self.generate_order(obj)

        if "capture" in request.GET:
            if capture_payment(obj.payment_data):
                obj.status = OrderStatus.PAYED
                obj.track = DeliveryMethod[obj.delivery_service].values[0].generate_document(obj, obj.track)
                obj.save()
                payment_done.send(obj)
                return JsonResponse({'status': "OK"})
            else:
                return JsonResponse({'status': "ERROR"})

        return JsonResponse({'id': obj.payment_data})
