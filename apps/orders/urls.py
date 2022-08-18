from django.urls import path

from apps.orders.views import CartTemplateView, CartOperationView

urlpatterns = [
    path("cart/", CartTemplateView.as_view(), name="cart"),
    path("cart-operation/", CartOperationView.as_view(), name="cart-operation")
]
