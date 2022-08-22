from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, get_language
from django.views.generic.edit import CreateView

from apps.helper.forms import FeedbackForm
from apps.helper.models import FAQ, Feedback
from shared.mixins.breadcrumbs import BreadCrumbsMixin


class FeedbackFAQView(BreadCrumbsMixin, CreateView):
    """ListView for FAQ with creating Feedback objects"""
    model = Feedback
    template_name = "helper/home.jinja"
    form_class = FeedbackForm

    def get_breadcrumbs(self):
        return [(_("Home"), reverse("products:list")), (_("Questions"),)]

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Your question has been sent. Check your email for a reply"))
        return redirect("helper")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = FAQ.objects.all()
        return context
