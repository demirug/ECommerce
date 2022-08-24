from django.conf import settings

from apps.orders.models import OrderSettings, Order
from apps.orders.services.delivery.model import IDeliveryType
from novaposhta_api.models import NP_WareHouse
from novaposhta_api.novaposhta import Novaposhta as NovaposhtaAPI, Recipient


class Novaposhta(IDeliveryType):

    def get_script(self) -> str:
        return "orders/js/nova_poshta.js"

    def required_data(self) -> bool:
        return True

    def generate_document(self, order: Order, data: str) -> str:

        order_settings: OrderSettings = OrderSettings.get_solo()

        from_WH: NP_WareHouse = NP_WareHouse.objects.filter(Ref=settings.NOVAPOSHTA_DEFAULT).first()
        to_WH: NP_WareHouse = NP_WareHouse.objects.filter(id=data).first()

        recipient: Recipient = Recipient(order.first_name, order.second_name, order.last_name, order.phone_number)
        ref, track = NovaposhtaAPI().create_document(from_WH,
                                                     to_WH,
                                                     order_settings.novaposhta_weight,
                                                     1,
                                                     int(order.cost),
                                                     order_settings.novaposhta_description.format(number=order.pk),
                                                     recipient)
        return track
