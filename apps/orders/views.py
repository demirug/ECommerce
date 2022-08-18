import json

from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView

from apps.orders.cart import Cart
from apps.orders.forms import CartOperationForm
from apps.orders.payment.model import PAYMENT_METHODS
from apps.products.models import Product


class CartTemplateView(TemplateView):
    template_name = "orders/cart.jinja"

    def get_context_data(self, **kwargs):
        PAYMENT_METHODS[0].handle_post(None, None)
        data = super().get_context_data(**kwargs)
        cart: Cart = Cart(self.request)
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
