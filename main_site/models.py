import os
import uuid
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

#todo Try removing the respective image from directory after deleting a driver
#todo Add last_updated_at field to every model, editalble=False and change on every save
def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(
       instance.__class__.__name__, filename)


class Driver(models.Model):
    created_at=models.DateTimeField(default=timezone.now,editable=False)
    name=models.CharField(max_length=200)
    phone=PhoneNumberField(unique=True,
                           verbose_name='Phone Number',
                           help_text='Format: +91-9912345678')
    emergency_contact = PhoneNumberField(null=True,
                                         blank=True,
                                         verbose_name='Emergency Contact',
                                         help_text='Format: +91-9912345678')
    address=models.TextField(null=True,
                             blank=True)
    blood_group=models.CharField(max_length=2,
                                 verbose_name='Blood Group',
                                 choices=[('O-','O-'),('O+','O+'),('A-','A-'),('A+','A+'),
                                          ('B-','B-'),('B+','B+'),('AB-','AB-'),('AB+','AB+'),
                                          ('NA','NA')])
    license_no=models.CharField(max_length=50,
                                null=True,blank=True,
                                verbose_name='License number')
    license_validity=models.DateField(verbose_name='Valid till',null=True,blank=True)
    email=models.EmailField(null=True,
                            blank=True,
                            verbose_name='Email Address')
    picture=models.ImageField(upload_to=get_upload_path,
                              default='default.png',
                              help_text='If not provided, default will be used')

    class Meta():
        ordering=['license_validity']

    def __str__(self):
        return self.name




class Maintenance(models.Model):
    created_at=models.DateTimeField(default=timezone.now,editable=False)
    vehicle=models.ForeignKey('Vehicle',
                              verbose_name='Vehicle to repair')
    start_date=models.DateField(default=timezone.now)
    end_date=models.DateField(null=True)
    start_time=models.TimeField()
    end_time=models.TimeField(null=True)
    repairing_cost=models.FloatField(null=True,blank=True,validators=[MinValueValidator(0)])
    status=models.ForeignKey('Status', null=True, editable=False)
    class Meta:
        ordering=['-start_date']
    def save(self,*args,**kwargs):
        if self.pk is None:
            self.status=Status.objects.get(type='Maintenance Started')
        super(Maintenance, self).save(*args, **kwargs)

    def __str__(self):
        return self.vehicle.__str__()+' | '+str(self.start_date)

class Vehicle(models.Model):
    created_at=models.DateTimeField(default=timezone.now,editable=False)
    registration_no=models.CharField(max_length=15,
                                     unique=True,
                                     help_text='e.g - UP 15 D 1234')
    nickname=models.CharField(max_length=50,
                              blank=True,
                              help_text='e.g.- B3')

    description=models.TextField(null=True,blank=True)
    seating_capacity=models.IntegerField(default=4,validators=[MinValueValidator(1)])
    is_owned=models.BooleanField(default=True,
                                 verbose_name='Owned by institute?',
                                 help_text='Whether owned by IIITA or hired')
    picture = models.ImageField(upload_to=get_upload_path,
                                default='school-bus.png',
                                help_text='If not provided, default will be taken')

    @classmethod
    def get_available_vehicles(cls):
        excluded_vehicles = []
        m = Maintenance.objects.filter(status=Status.objects.get('Maintenance Started'))
        for i in m:
            excluded_vehicles.append(i.vehicle)
        return Vehicle.objects.filter(~Q(excluded_vehicles))

    def __str__(self):
        if self.nickname is not None:
            return self.registration_no+" | "+self.nickname
        else:
            return self.registration_no

class Status(models.Model):
    type=models.CharField(max_length=50,unique=True)
    description=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.type

class Request(models.Model):
    user=models.ForeignKey('auth.User',
                           verbose_name='Requested by')
    created_at=models.DateTimeField(default=timezone.now,editable=False)
    #last_updated_at=models.DateTimeField(default=timezone.now)
    start_date=models.DateField()
    start_time=models.TimeField()
    end_date=models.DateField(null=True,blank=True)
    expected_end_time=models.TimeField(null=True,
                                       blank=True,
                                       help_text='To ensure fair services to '
                                                 'everyone, please provide expected end time')
    no_of_persons_travelling=models.IntegerField(default=1,validators=[MinValueValidator(1)])
    request_type=models.CharField(max_length=50,
                          default='Personal',
                          choices=[('Official','Official'),('Personal','Personal')],
                          verbose_name='Type of request(Official/Personal)')
    description=models.TextField(null=True,
                                 blank=True,
                                 verbose_name='Brief Summary,with preferences(if any)')
    remarks=models.TextField(null=True,
                             blank=True,
                             verbose_name='Remarks from transport cell')
    source=models.CharField(max_length=200)
    destination=models.CharField(max_length=200)
    is_round_trip=models.BooleanField(default=False,
                                          verbose_name='Round Trip?')
    status=models.ForeignKey('Status',editable=False,
                             verbose_name='Status of Request')


    def save(self, *args, **kwargs):
        #self.last_updated_at=timezone.now()
        if self.pk is None:
            self.status=Status.objects.get(type='Request Pending')
        super(Request, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering=['-start_date']



class Trip(models.Model):
    created_at=models.DateTimeField(default=timezone.now,editable=False)
    request = models.ForeignKey('Request', on_delete=models.CASCADE,editable=False)
    status=models.ForeignKey('Status',editable=False,verbose_name='Status of trip')
    vehicle=models.ForeignKey('Vehicle')
    driver=models.ForeignKey('Driver')
    start_distance = models.FloatField(null=True,
                                       validators=[MinValueValidator(0)])
    end_distance = models.FloatField(null=True,
                                     validators=[MinValueValidator(1)])
    rate = models.FloatField(default=0,
                             verbose_name='Rate/km', validators=[MinValueValidator(0)])
    fare = models.FloatField(validators=[MinValueValidator(0)],null=True)
    def save(self,*args,**kwargs):
        if self.pk is None:
            self.status = Status.objects.get(type='Trip Scheduled')
        super(Trip, self).save(*args,**kwargs)
    def __str__(self):
        return str(self.id)

class Bill(models.Model):
    created_at=models.DateTimeField(default=timezone.now,editable=False)
    request=models.OneToOneField(
        Request,on_delete=models.CASCADE)
    total_distance=models.FloatField(default=0.0,validators=[MinValueValidator(0)])
    total_fare=models.FloatField(default=0.0,validators=[MinValueValidator(0)])

    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return str(self.id)

class Announcement(models.Model):
    created_by=models.ForeignKey('auth.User')
    created_at=models.DateTimeField(default=timezone.now,editable=False)
    text=models.TextField(max_length=500)
    description=models.TextField(null=True,
                                 blank=True,
                                 verbose_name='Brief description')
    def __str__(self):
        return str(self.id)

    class Meta:
        ordering=['-created_at']
    def save(self, *args,**kwargs):
        super(Announcement, self).save(*args,**kwargs)

class Schedule(models.Model):
    file=models.FileField(upload_to=get_upload_path)
    created_at=models.DateTimeField(default=timezone.now)
    def save(self, *args,**kwargs):
        message='Transport schedule has been updated.Please visit'\
                +self.file.url+'to see changes'
        #mail_to_admins(message=message)
        super(Schedule,self).save(*args,**kwargs)