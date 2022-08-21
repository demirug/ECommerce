from aenum import MultiValueEnum
from django.utils.translation import gettext_lazy as _

from apps.orders.services.delivery.model import IDeliveryType
from apps.orders.services.delivery.nodelivery import Pickup
from apps.orders.services.delivery.novaposhta import Novaposhta


class DeliveryMethod(MultiValueEnum):
    NONE = IDeliveryType(enabled=False), "NONE",
    PICK_UP = Pickup(), _("Pick up"),
    NOVA_POSHTA = Novaposhta(), _("NovaPoshta")

    @classmethod
    def choices(cls):
        return [(key, cls[key].values[1]) for key in cls.__members__.keys()
                if DeliveryMethod[key].values[0].enabled]
