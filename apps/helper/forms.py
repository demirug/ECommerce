from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from apps.helper.models import Feedback, FAQ, HelperSettings


class HelperSettingsForm(forms.ModelForm):
    feedback_email = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = HelperSettings
        fields = "__all__"


class FAQForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = FAQ
        fields = "__all__"


class FeedbackAdminForm(forms.ModelForm):
    """Feedback for admin panel"""
    question = forms.CharField()

    email = forms.EmailField()

    answer = forms.CharField(label=_("Answer"), widget=CKEditorUploadingWidget(config_name='no-elements'))

    class Meta:
        model = Feedback
        fields = ['question', 'email', 'answer']


class FeedbackForm(forms.ModelForm):
    """Feedback form for authorized users"""
    email = forms.EmailField(label="",
                             widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Email")}))
    question = forms.CharField(label="", widget=CKEditorUploadingWidget(config_name='no-elements'))

    def clean_question(self):
        question = self.cleaned_data['question']
        settings = HelperSettings.get_solo()

        if len(strip_tags(question)) < settings.min_feedback_len:
            raise ValidationError(_("Minimum length of question %s chars") % settings.min_feedback_len)

        if len(strip_tags(question)) > settings.max_feedback_len:
            raise ValidationError(_("Maximum length of question %s chars") % settings.max_feedback_len)
        return question

    class Meta:
        model = Feedback
        fields = ['email', 'question']
