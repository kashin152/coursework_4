from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingHomeView, MailingListView

app_name = MailingConfig.name

urlpatterns = [
    path("home/", MailingHomeView.as_view(), name="home"),
    path("mailing_list/", MailingListView.as_view(), name="mailing_list")

]
