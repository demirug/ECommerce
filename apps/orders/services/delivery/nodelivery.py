from apps.orders.services.delivery.model import IDeliveryType


class Pickup(IDeliveryType):

    def required_data(self) -> bool:
        return False
