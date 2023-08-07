from django.core.management.base import BaseCommand
from send_email.views import send_event_emails


class Command(BaseCommand):
    help = 'Send event emails to employees.'

    def handle(self, *args, **options):
        send_event_emails()
