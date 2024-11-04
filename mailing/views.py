from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


from mailing.models import Recipient, Message, Mailing, MailingAttempt


class MailingHomeView(ListView):
    model = Mailing
    template_name = "base.html"
    context_object_name = "mailings"


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"
    context_object_name = "mailings"

#
# class RecipientCreateView(CreateView):
#     model = Recipient
#     form_class = RecipientForm
#     template_name = "catalog/product_create.html"
#     success_url = reverse_lazy("catalog:home")