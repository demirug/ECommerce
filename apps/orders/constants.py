from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class OrderStatus(TextChoices):
    NEW = "NEW", _("NEW")
    PAYED = "PAYED", _("PAYED")
    DONE = "DONE", _("DONE"),
    CANCELED = "CANCELED", _("CANCELED")
