from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from shared.services.slugify import unique_slugify


class Product(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    description = models.TextField(_("Description"))
    image = models.ImageField(_("Image"), blank=True)
    slug = models.SlugField(unique=True, blank=True)

    price = models.DecimalField(_("Price"), max_digits=5, decimal_places=1)
    count = models.PositiveIntegerField(_("Count"))

    enable = models.BooleanField(_("Enabled"), default=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

    def save(self, **kwargs):
        """Creating unique slug for model if slug not set"""
        if not self.slug:
            unique_slugify(self, f"{self.name}")
        super().save(**kwargs)

    def get_image(self):
        if self.image:
            return self.image.url
        return static("products/images/default.png")


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    file = models.ImageField(_("Image"))

    class Meta:
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")

    def __str__(self):
        return f"ProductImage={self.product.name}-{self.pk}"
