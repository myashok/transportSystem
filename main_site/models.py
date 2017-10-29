from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.timezone import utc
from phonenumber_field.modelfields import PhoneNumberField

DEFAULT_REQUEST_STATUS=0

class Driver(models.Model):
    name=models.CharField(max_length=200,null=False)
    phone=PhoneNumberField(null=False)
    license_no=models.CharField(max_length=50,unique=True,null=True)
    license_validity=models.DateField(default=timezone.now)
    email=models.EmailField(null=True)
    date_of_birth=models.DateField(null=True)
    def __str__(self):
        return self.name

class Vehicle(models.Model):
    registration_no=models.CharField(max_length=15,null=False)
    description=models.TextField(null=True)
    def __str__(self):
        return self.registration_no

class RequestType(models.Model):
    type=models.CharField(max_length=50,unique=True,null=False)
    def __str__(self):
        return self.type

class RequestStatus(models.Model):
    type=models.CharField(max_length=50,unique=True,null=False)
    def __str__(self):
        return self.type

class TransportRequest(models.Model):
    user=models.ForeignKey('auth.User')
    last_updated_at=models.DateTimeField()
    date_of_journey=models.DateField(null=False)
    time_of_journey=models.TimeField(null=False)
    request_type=models.ForeignKey('RequestType')
    description=models.TextField(null=True)
    request_status=models.ForeignKey('RequestStatus',null=False)
    source=models.CharField(max_length=200,null=False)
    destination=models.CharField(max_length=200,null=False)
    is_return_journey=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.last_updated_at=timezone.now()
        super(TransportRequest, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering=['date_of_journey']
