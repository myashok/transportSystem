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
        os.path.join(str(instance.id),filename))

class Driver(models.Model):
    name=models.CharField(max_length=200)
    phone=PhoneNumberField(unique=True)
    license_no=models.CharField(max_length=50,unique=True)
    license_validity=models.DateField()
    email=models.EmailField(unique=True)
    date_of_birth=models.DateField()
    picture=models.ImageField(upload_to=get_upload_path,default='default.png')

    def get_age(self):
        return timezone.now().year-self.date_of_birth.year

    class Meta():
        ordering=['license_validity']

    def __str__(self):
        return self.name

    def save(self, *args, ** kwargs):
        super(Driver, self).save(*args, **kwargs)
        image = Image.open(self.picture)
        (width, height) = image.size
        size = (100, 100)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.picture.path)


class VehicleType(models.Model):
    type=models.CharField(max_length=50,unique=True)
    capacity=models.IntegerField(default=4,validators=[MinValueValidator(1)])
    def __str__(self):
        return self.type

class VehicleStatus(models.Model):
    type=models.CharField(max_length=50)
    description=models.TextField(null=True)

class VehicleMaintenance(models.Model):
    vehicle=models.ForeignKey('Vehicle')
    start_date=models.DateField()
    end_date=models.DateField(null=True)
    expected_cost=models.FloatField(validators=[MinValueValidator(0)])
    actual_cost=models.FloatField(validators=[MinValueValidator(0)])

    class Meta:
        ordering=['start_date']

    @classmethod
    def make_available(cls,id,end_date,actual_cost):
        vm=cls.objects.get(pk=id)
        vm.end_date=end_date
        vm.actual_cost=actual_cost
        vm.save()
        vm.vehicle.status=VehicleStatus.objects.get(type='Available')
        vm.vehicle.save()


class Vehicle(models.Model):
    registration_no=models.CharField(max_length=15,null=False,unique=True)
    #picture=models.ImageField(upload_to=get_upload_path,default='default_bus.png')
    type=models.ForeignKey('VehicleType')
    description=models.TextField(null=True)
    fuel_capacity=models.FloatField(null=False,validators=[MinValueValidator(10)])
    status=models.ForeignKey('VehicleStatus',default=1)

    def __str__(self):

        return self.registration_no

    @classmethod
    def get_available_vehicles(cls):
        return cls.objects.filter(status=VehicleStatus.objects.get(type='Available'))
    @classmethod
    def get_vehicles_under_maintenance(cls):
        return cls.objects.get(status=VehicleStatus.objects.get(type='Under maintenance'))


class RequestType(models.Model):
    type=models.CharField(max_length=50,unique=True,null=False)
    rate=models.FloatField(validators=[MinValueValidator(0)])
    def __str__(self):
        return self.type


class RequestStatus(models.Model):
    type=models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.type


class TransportRequest(models.Model):
    user=models.ForeignKey('auth.User')
    last_updated_at=models.DateTimeField(default=timezone.now)
    date_of_journey=models.DateField(null=False)
    time_of_journey=models.TimeField(null=False)
    no_of_persons_travelling=models.IntegerField(default=1,validators=[MinValueValidator(1)])
    request_type=models.ForeignKey('RequestType')
    description=models.TextField(null=True)
    source=models.CharField(max_length=200,null=False)
    destination=models.CharField(max_length=200,null=False)
    is_return_journey=models.BooleanField(default=False)
    status=models.ForeignKey('RequestStatus',default=1)

    def save(self, *args, **kwargs):
        self.last_updated_at=timezone.now()
        super(TransportRequest, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering=['date_of_journey']


class TripStatus(models.Model):
    type=models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.type

class Trip(models.Model):
    start_distance_reading=models.FloatField(null=True,blank=True,validators=[MinValueValidator(0)])
    end_distance_reading=models.FloatField(null=True,blank=True,validators=[MinValueValidator(1)])
    request = models.OneToOneField(
        TransportRequest,
        on_delete=models.CASCADE,
    )
    status=models.ForeignKey('TripStatus',default=1)
    start_time=models.TimeField(null=False)
    end_time=models.TimeField(null=True,blank=True)
    vehicles=models.ManyToManyField(Vehicle)
    drivers=models.ManyToManyField(Driver)

    def is_valid_trip(self):
        return self.vehicles.all().count()==self.drivers.all().count()

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
        return self.id

