from aenum import MultiValueEnum
from django.utils.translation import gettext_lazy as _

from apps.orders.services.payment.model import IPaymentType
from apps.orders.services.payment.nopayment import CashOnDelivery


class PaymentMethod(MultiValueEnum):
    NONE = IPaymentType(enabled=False), "NONE"
    CASH_ON_DELIVERY = CashOnDelivery(), _("Cash on delivery")

    @classmethod
    def choices(cls):
        return [(key, cls[key].values[1]) for key in cls.__members__.keys()
                if cls[key].values[0].enabled]