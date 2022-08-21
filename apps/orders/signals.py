from django import dispatch
from django.dispatch import receiver

payment_done = dispatch.Signal()


@receiver(payment_done)
def onPaymentDone(sender, **kwargs):
    # TODO send payment done mail
    pass
