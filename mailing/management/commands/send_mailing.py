from django.core.management.base import BaseCommand
from mailing.models import Mailing


class Command(BaseCommand):
    help = 'Отправить рассылку по ID'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int)

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        try:
            mailing = Mailing.objects.get(pk=mailing_id)
            mailing.send_mailing()
            self.stdout.write(self.style.SUCCESS('Рассылка отправлена успешно.'))
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR('Рассылка не найдена.'))
