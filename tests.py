from django.test import TestCase

from django.test import TestCase
from django.core import mail
from django.utils import timezone
from send_email.models import Employee, Event, EmailTemplate, EmailLog
from send_email.views import send_event_emails

class EventEmailTestCase(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(name='John Doe', email='john@example.com')
        self.birthday_template = EmailTemplate.objects.create(
            event_type='birthday',
            subject='Happy Birthday!',
            content='Dear {name}, Happy Birthday to you!'
        )
        self.work_anniversary_template = EmailTemplate.objects.create(
            event_type='work_anniversary',
            subject='Work Anniversary Greetings!',
            content='Congratulations {name} on completing {years} years with us!'
        )

    def test_send_birthday_email(self):
        event = Event.objects.create(
            employee=self.employee,
            event_type='birthday',
            event_date=timezone.now().date()
        )

        send_event_emails()

        # Check if the email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.employee.email])
        self.assertIn('Happy Birthday to you!', mail.outbox[0].subject)
        self.assertIn('Dear John', mail.outbox[0].body)

        # Check if the email log is created
        self.assertTrue(EmailLog.objects.filter(event=event, email_status=True).exists())

    def test_send_work_anniversary_email(self):
        event = Event.objects.create(
            employee=self.employee,
            event_type='work_anniversary',
            event_date=timezone.now().date()
        )

        send_event_emails()

        # Check if the email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.employee.email])
        self.assertIn('Work Anniversary Greetings!', mail.outbox[0].subject)
        self.assertIn('Congratulations John on completing', mail.outbox[0].body)

        # Check if the email log is created
        self.assertTrue(EmailLog.objects.filter(event=event, email_status=True).exists())

    def test_no_events_scheduled(self):
        send_event_emails()

        # Check if no email is sent
        self.assertEqual(len(mail.outbox), 0)

        # Check if the email log is created with the no events message
        self.assertTrue(EmailLog.objects.filter(email_status=False, error_message='No events scheduled').exists())
