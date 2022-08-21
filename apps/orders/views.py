import json

from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView
from django_jinja.views.generic import CreateView

from apps.orders.cart import Cart
from apps.orders.forms import CartOperationForm, ConfirmModelForm
from apps.orders.models import Order, OrderItem
from apps.orders.services.delivery.constants import DeliveryMethod
from apps.orders.services.payment.constants import PaymentMethod
from apps.orders.services.payment.model import IPaymentType
from apps.products.models import Product


class CartTemplateView(TemplateView):
    template_name = "orders/cart.jinja"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        cart: Cart = Cart(self.request)
        cart.updateQuantity()
        products = Product.objects.filter(pk__in=cart.cart_items.keys())
        data['cart'] = {product: cart.cart_items[str(product.pk)] for product in products}
        data['totalPrice'] = sum([product.price * cart.cart_items[str(product.pk)] for product in products])
        return data


class CartOperationView(BaseFormView):
    form_class = CartOperationForm

    def get(self, *args, **kwargs):
        return redirect("orders:cart")

    def form_invalid(self, form):
        return HttpResponseBadRequest()

    def form_valid(self, form):
        product: Product = get_object_or_404(Product, slug=self.request.POST['slug'])
        cart: Cart = Cart(self.request)
        function = getattr(cart, self.request.POST['operation'], None)
        if function:
            # Check if its function and has @cart_option decorator
            if callable(function) and function.__dict__.get('cart', False):
                function(product, int(self.request.POST['value']))
                count = cart.cart_items.get(str(product.pk), 0)
                return HttpResponse(json.dumps({'count': count, 'price': count * product.price}, default=str))


class OrderCreateView(CreateView):
    template_name = "orders/confirm.jinja"
    model = Order
    form_class = ConfirmModelForm

    def dispatch(self, request, *args, **kwargs):
        self.cart = Cart(request)
        # If cart empty or cart items unavailable do redirect
        if len(self.cart.cart_items) == 0 or not self.cart.check_available():
            return redirect("orders:cart")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        products = Product.objects.filter(pk__in=self.cart.cart_items.keys())
        data['cart'] = {product: self.cart.cart_items[str(product.pk)] for product in products}
        data['totalPrice'] = sum([product.price * self.cart.cart_items[str(product.pk)] for product in products])

        data['delivery_js'] = [DeliveryMethod[key].values[0].get_script() for key in DeliveryMethod.__members__.keys()
                               if DeliveryMethod[key].values[0].get_script() != ""]

        return data

    def form_valid(self, form):
        order: Order = form.save(commit=False)
        products = Product.objects.filter(pk__in=self.cart.cart_items.keys())

        for product in products:
            product.count -= self.cart.cart_items[str(product.pk)]
            product.save()

        order.cost = sum([product.price * self.cart.cart_items[str(product.pk)] for product in products])
        # saving delivery_data to track field. After will be processed to document track number
        order.track = form.cleaned_data['delivery_data']

        order.save()

        OrderItem.objects.bulk_create([
             OrderItem(order=order, product=products.get(id=key), count=value)
             for key, value in self.cart.cart_items.items()])

        self.cart.clear()

        return redirect("orders:pay", uuid=order.uuid)


class PaymentView(View):

    def dispatch(self, request, *args, **kwargs):
        self.order: Order = get_object_or_404(Order, uuid=self.kwargs['uuid'])
        self.payment: IPaymentType = PaymentMethod[self.order.payment_service].values[0]
        return super().dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.payment.handle_get(self.order, self.request)

    def post(self, *args, **kwargs):
        return self.payment.handle_post(self.order, self.request)
