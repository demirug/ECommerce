from django.urls import reverse
from django_jinja.views.generic import ListView, DetailView

from apps.products.models import Product
from shared.mixins.breadcrumbs import BreadCrumbsMixin
from shared.mixins.paginator import RemovePageMixin


class ProductListView(RemovePageMixin, ListView):
    model = Product
    template_name = "products/list.jinja"
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(enable=True)


class ProductDetailView(BreadCrumbsMixin, DetailView):
    model = Product
    template_name = "products/detail.jinja"

    def get_queryset(self):
        return Product.objects.filter(enable=True)

    def get_breadcrumbs(self):
        return [('Home', reverse("products:list")), (self.object.name,)]
