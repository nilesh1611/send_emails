from django.shortcuts import render
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from .models import Employee, Event, EmailTemplate, EmailLog

def send_event_emails():
    current_date = timezone.now().date()
    events = Event.objects.filter(event_date=current_date)

    if not events.exists():
        # Log that no events are scheduled for the current period
        log_no_events_scheduled()
        return

    for event in events:
        try:
            # Fetch email template based on the event type
            email_template = EmailTemplate.objects.get(event_type=event.event_type)
            # Populate the email template with event-specific content
            email_content = populate_email_template(email_template, event)
            # Send the email to the employee
            send_email_to_employee(event.employee, email_template.subject, email_content)
            # Log the email sending status as successful
            log_email_status(event, True, None)
        except Exception as e:
            # Log the error and continue with the next scheduled email
            log_email_status(event, False, str(e))

def populate_email_template(email_template, event):
    # For simplicity, let's assume the content is already populated.
    return email_template.content

def send_email_to_employee(employee, subject, content):
    # Use Django's send_mail function to send the email
    send_mail(subject, content, 'nrply@example.com', [employee.email])

def log_no_events_scheduled():
    # Your implementation to log this information.

def log_email_status(event, success, error_message):
    # Log the email sending status and any errors encountered in Django db
    email_log = EmailLog.objects.create(
        employee=event.employee,
        event=event,
        email_status=success,
        error_message=error_message
    )
