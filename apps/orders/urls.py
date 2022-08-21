from django.urls import path

from apps.orders.views import CartTemplateView, CartOperationView, OrderCreateView, PaymentView

urlpatterns = [
    path("cart/", CartTemplateView.as_view(), name="cart"),
    path("cart-operation/", CartOperationView.as_view(), name="cart-operation"),
    path("confirm/", OrderCreateView.as_view(), name="confirm"),
    path("pay/<str:uuid>/", PaymentView.as_view(), name="pay")
]
