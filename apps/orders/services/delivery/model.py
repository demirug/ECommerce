class IDeliveryType:

    def __init__(self, enabled=True, *args, **kwargs):
        self.enabled = enabled
        super().__init__(*args, **kwargs)

    def get_script(self) -> str:
        return ""

    def required_data(self) -> bool:
        return False

    def generate_document(self, order, data: str) -> str:
        return ""
