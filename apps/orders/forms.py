from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.orders.models import Order
from apps.orders.services.delivery.constants import DeliveryMethod
from apps.orders.services.payment.constants import PaymentMethod
from shared.mixins.forms import FormControlMixin


class CartOperationForm(forms.Form):

    operation = forms.CharField()
    slug = forms.CharField()
    value = forms.IntegerField()


class ConfirmModelForm(FormControlMixin, forms.ModelForm):

    payment_service = forms.CharField(widget=forms.Select(choices=PaymentMethod.choices()))
    delivery_service = forms.CharField(widget=forms.Select(choices=DeliveryMethod.choices()))
    delivery_data = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        data = self.cleaned_data

        if data['delivery_data'] == "" and DeliveryMethod[data['delivery_service']].values[0].required_data():
            raise ValidationError(_("Delivery params not filled"))

        return data

    class Meta:
        model = Order
        exclude = ('cost', 'date', 'track', 'status')

