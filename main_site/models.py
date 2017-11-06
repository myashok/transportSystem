import os
from datetime import datetime

from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

def get_upload_path(instance, filename):
    return os.path.join(
       instance.__class__.__name__,
        os.path.join(str(instance.id), filename))

class Driver(models.Model):
    name=models.CharField(max_length=200)
    phone=PhoneNumberField(unique=True)
    blood_group=models.CharField(max_length=5,default='A+')
    license_no=models.CharField(max_length=50,unique=True)
    license_validity=models.DateField()
    email=models.EmailField(unique=True)
    picture=models.ImageField(upload_to=get_upload_path,default='default.png')

    class Meta():
        ordering=['license_validity']

    def __str__(self):
        return self.name

    def save(self, *args, ** kwargs):
        if os.path.exists(self.picture.url):
            image = Image.open(self.picture)
            os.remove(image)
        super(Driver, self).save(*args, **kwargs)
        image = Image.open(self.picture)
        (width, height) = image.size
        size = (200, 200)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.picture.path)

    def delete(self, using=None, keep_parents=False):
        super(Driver, self).delete()
        if not os.path.exists(self.picture):
            return
        image = Image.open(self.picture)
        os.remove(image)


class VehicleMaintenance(models.Model):
    vehicle=models.ForeignKey('Vehicle')
    start_date=models.DateField()
    end_date=models.DateField(null=True)
    expected_cost=models.FloatField(default=0,blank=True)
    actual_cost=models.FloatField(default=0,blank=True)

    class Meta:
        ordering=['start_date']

class Vehicle(models.Model):
    registration_no=models.CharField(max_length=15,unique=True)
    picture=models.ImageField(upload_to=get_upload_path,default='school-bus.png')
    description=models.TextField(null=True)
    seating_capacity=models.IntegerField(default=4)
    status=models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if self.vehiclemaintenance_set.filter(end_date=None).exists():
            self.status="Under Maintenance"
        else:
            self.status="Available"
        if os.path.exists(self.picture.url):
            image = Image.open(self.picture)
            os.remove(image)
        image = Image.open(self.picture)
        (width, height) = image.size
        size = (200, 200)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.picture.path)
        super(Vehicle,self).save(*args,**kwargs)

    def __str__(self):
        return self.registration_no

    @classmethod
    def get_available_vehicles(cls):
        return cls.objects.filter(status='Available')
    @classmethod
    def get_vehicles_under_maintenance(cls):
        return cls.objects.get(status='Under maintenance')


class RequestType(models.Model):
    type=models.CharField(max_length=50,unique=True,null=False)
    rate=models.FloatField(validators=[MinValueValidator(0)])
    def __str__(self):
        return self.type


class TransportRequest(models.Model):
    user=models.ForeignKey('auth.User')
    last_updated_at=models.DateTimeField(default=timezone.now)
    date_of_journey=models.DateField(null=False)
    time_of_journey=models.TimeField(default=timezone.now)
    no_of_persons_travelling=models.IntegerField(default=1,validators=[MinValueValidator(1)])
    request_type=models.ForeignKey('RequestType')
    description=models.TextField(null=True)
    source=models.CharField(max_length=200,null=False)
    destination=models.CharField(max_length=200,null=False)
    is_return_journey=models.BooleanField(default=False)
    status=models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.last_updated_at=timezone.now()
        if Trip.objects.filter(request=self).exists():
            self.status='Accepted'
        else:
            self.status='Pending'

        super(TransportRequest, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering=['date_of_journey']

class Trip(models.Model):
    start_distance_reading=models.FloatField(null=True,blank=False,validators=[MinValueValidator(0)])
    end_distance_reading=models.FloatField(null=True,blank=False,validators=[MinValueValidator(1)])
    request = models.OneToOneField(
        TransportRequest,
        on_delete=models.CASCADE,
    )
    status=models.CharField(max_length=50)
    start_time=models.TimeField()
    end_time=models.TimeField(null=True)
    vehicles=models.ManyToManyField(Vehicle)
    drivers=models.ManyToManyField(Driver)

    def save(self,*args,**kwargs):
        if Bill.objects.filter(trip=self):
            self.status='Completed'
        elif self.start_distance_reading:
            self.status='Active'
        else:
            self.status='Scheduled'
        super(Trip,self).save(*args,**kwargs)

    def __str__(self):
        return str(self.id)

class Bill(models.Model):
    datetime_of_generation=models.DateTimeField(default=timezone.now)
    trip = models.OneToOneField(
        Trip,
        on_delete=models.CASCADE,
    )
    total_distance=models.FloatField(validators=[MinValueValidator(1)])
    discount_percentage=models.FloatField(default=0,validators=[MinValueValidator(0)])
    total_fare=models.FloatField(validators=[MinValueValidator(0)])

    class Meta:
        ordering=['datetime_of_generation']

    def __str__(self):
        return str(self.id)

class Announcement(models.Model):
    created_by=models.ForeignKey('auth.User')
    created_at=models.DateTimeField()
    text=models.TextField(max_length=500)
    description=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.text

    class Meta:
        ordering=['created_at']