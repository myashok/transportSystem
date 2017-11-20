from datetime import datetime

from django.core.validators import MinValueValidator
from django.forms import models, forms
from main_site.models import Trip, Driver, Maintenance, Request
from django import  forms

class DriverForm(models.ModelForm):
    class Meta:
        model=Driver
        fields = ['name', 'phone', 'emergency_contact', 'address', 'blood_group',
                  'license_no', 'license_validity', 'email', 'picture']
    def clean(self):
        license_validity=self.cleaned_data.get('license_validity')
        if license_validity is None:
            return
        if license_validity<datetime.today().date():
            self.add_error('license_validity',['Not a valid expiration date'])


class MaintenanceEndForm(models.ModelForm):
    class Meta:
        model=Maintenance
        fields=['end_date','end_time','repairing_cost']
    def clean(self):
        end_date=self.cleaned_data.get('end_date')
        end_time=self.cleaned_data.get('end_time')
        if end_date<self.instance.start_date:
            self.add_error('end_date','End date cannot be before start date')
        elif end_date==self.instance.start_date and end_time<self.instance.start_time:
            self.add_error('end_time','End time cannot be before start time on same date')

class MaintenanceUpdateForm(models.ModelForm):
    class Meta:
        model=Maintenance
        fields=['start_date','end_date','start_time','end_time','repairing_cost']
    def clean(self):
        start_date=self.cleaned_data.get('start_date')
        end_date=self.cleaned_data.get('end_date')
        start_time=self.cleaned_data.get('start_time')
        end_time=self.cleaned_data.get('end_time')
        if end_date<start_date:
            self.add_error('end_date','End date cannot be before start date')
        elif end_date==start_date and end_time<start_time:
            self.add_error('end_time','End time cannot be before start time on same date')

class RequestForm(models.ModelForm):
    class Meta:
        model=Request
        fields = ['start_date', 'start_time', 'end_date', 'expected_end_time',
                  'no_of_persons_travelling', 'request_type', 'description',
                  'source', 'destination', 'is_round_trip']
    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        start_time = self.cleaned_data.get('start_time')
        expected_end_time = self.cleaned_data.get('expected_end_time')

        if start_date<datetime.today().date():
            self.add_error('start_date','You cannot make a trip in the past')
        elif end_date is not None and end_date<start_date:
            self.add_error('end_date','Make sure end date>=start date')
        elif start_date==end_date and start_time>expected_end_time:
            self.add_error('expected_end_time','End time cannot be smaller than start time on same day')

class TripCreateForm(models.ModelForm):
    class Meta:
        model=Trip
        fields=['driver','vehicle','rate']
    def __init__(self,*args,**kwargs):
        super(TripCreateForm,self).__init__(*args,**kwargs)
        self.pk=kwargs.pop('pk',None)
        #self.fields['vehicle']=Vehicle.get_available_vehicles()
        # trips=Trip.objects.filter(request_id=self.pk)
        # for i in trips:
        #     if i.status==Status.objects.get(type='Request Scheduled') and (i.vehicle==vehicle):
        #         self.add_error('vehicle','Same vehicle is in a different active journey for this trip')
        #     elif i.status == Status.objects.get(type='Request Scheduled') and (i.driver == driver):
        #         self.add_error('vehicle','Same driver is in a different active journey for this trip')
        #
class FareCalculatorForm(forms.Form):
    start_date=forms.DateField(required=True)
    end_date=forms.DateField(required=True)
    start_time=forms.TimeField(required=True)
    end_time=forms.TimeField(required=True)
    distance=forms.FloatField(required=True,
                              validators=[MinValueValidator(1)],
                              label='Expected Distance')

