from django.http import HttpResponse


class IPaymentType:

    def __init__(self, enabled=True, *args, **kwargs):
        self.enabled = enabled
        super().__init__(*args, **kwargs)

    def handle_get(self, obj, request) -> HttpResponse:
        return HttpResponse()

    def handle_post(self, obj, request) -> HttpResponse:
        return HttpResponse()
