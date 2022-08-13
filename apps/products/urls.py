from django.urls import path

from apps.products.views import ProductListView, ProductDetailView

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="detail")
]
