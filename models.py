from django.db import models

event_type_choices = [
    ('birthday', 'Birthday'),
    ('foundation day', 'Foundation Day'),
]

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()

class Event(models.Model):
    objects = None
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event_type = models.CharField(choices=event_type_choices, max_length=50)
    event_date = models.DateField()

class EmailTemplate(models.Model):
    objects = None
    event_type = models.CharField(choices=event_type_choices, max_length=50)
    subject = models.CharField(max_length=255)
    content = models.TextField()

class EmailLog(models.Model):
    objects = None
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email_status = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)
    sent_date = models.DateTimeField(auto_now_add=True)
