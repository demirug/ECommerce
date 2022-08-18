from django import forms


class CartOperationForm(forms.Form):

    operation = forms.CharField()
    slug = forms.CharField()
    value = forms.IntegerField()

