from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth import  REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, ListView, DeleteView, CreateView, DetailView

from main_site.decorators import is_not_priveleged, check_not_priveleged
from main_site.models import TransportRequest, Driver, RequestStatus, Vehicle, Trip, TripStatus
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import UpdateView

import logging
logger = logging.getLogger(__name__)


class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
            if is_not_priveleged(request.user):
                return redirect('user-home')
            else:
                return redirect('staff-home')

        else:
            return render(request,'login.html',{'error':'Invalid credentials'})

    def get(self,request):
        if request.user.is_authenticated:
            if is_not_priveleged(request.user):
                return redirect('user-home')
            else:
                return redirect('staff-home')

        return render(request,'login.html')

@method_decorator(login_required(login_url='login'),name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


def my_requests(request):
    requests=TransportRequest.objects.filter(user=request.user)
    return render(request, 'transport_request/my_requests.html', {'requests':requests})


####################driver##################


#create driver
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class DriverCreateView(CreateView):
    model=Driver
    fields=['name','picture','phone','license_no','license_validity','email','date_of_birth']
    template_name = 'driver/new_driver.html'
    success_url = reverse_lazy('list-drivers')

#driver details
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class DriverDetailView(DetailView):
    model=Driver
    template_name = 'driver/view_driver.html'
    context_object_name = 'driver'

#update driver
@method_decorator(check_not_priveleged,name='dispatch')
@method_decorator(login_required(login_url='login'),name='dispatch')
class DriverUpdateView(UpdateView):
    model=Driver
    fields=['name','picture','phone','license_no','license_validity','email','date_of_birth']
    template_name = 'driver/update_driver.html'
    def get_success_url(self):
        return reverse('view-driver',kwargs={'pk':self.object.pk})

#delete driver
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class DriverDeleteView(DeleteView):
    model=Driver
    template_name = 'driver/delete_driver.html'
    success_url = reverse_lazy('list-drivers')

#list drivers
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class DriverListView(ListView):
    model = Driver
    template_name = 'driver/list_drivers.html'
    context_object_name = 'drivers'

#################request####################

#create request
@method_decorator(login_required(login_url='login'),name='dispatch')
class RequestCreateView(CreateView):
    model=TransportRequest
    template_name = 'transport_request/new_request.html'
    fields = ['date_of_journey', 'time_of_journey', 'request_type', 'description',
              'source', 'destination','no_of_persons_travelling', 'is_return_journey']
    def form_valid(self, form):
        request=form.save(commit=False)
        request.user=self.request.user
        request.request_status=RequestStatus.objects.get(pk=1)
        request.last_updated_at=timezone.now()
        return super(RequestCreateView,self).form_valid(form)
    def get_success_url(self):
        return reverse('view-request',kwargs={'pk':self.object.pk})

#read request
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class RequestDetailView(DetailView):
    model=TransportRequest
    template_name = 'transport_request/view_request.html'
    context_object_name = 'request'

#update request
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class RequestUpdateView(UpdateView):
    model=TransportRequest
    fields = ['date_of_journey', 'time_of_journey', 'request_type', 'description',
              'source', 'destination','preferred_vehicle_type', 'is_return_journey']
    template_name = 'transport_request/update_request.html'
    def get_success_url(self):
        return reverse('view-request',kwargs={'pk':self.object.pk})

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class RequestListView(ListView):
    model = TransportRequest
    template_name = 'transport_request/list_requests.html'
    context_object_name = 'requests'
    def get_queryset(self):
        if is_not_priveleged(self.request.user):
            return TransportRequest.objects.filter(user=self.request.user)
        return TransportRequest.objects.all()

#####################################################

################vehicle##############3

#create vehicle
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class VehicleCreateView(CreateView):
    model=Vehicle
    fields=['registration_no','type','description','fuel_capacity']
    template_name = 'vehicle/new_vehicle.html'
    success_url = reverse_lazy('list-vehicles')

#vehicle details
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class VehicleDetailView(DetailView):
    model=Vehicle
    template_name = 'vehicle/view_vehicle.html'
    context_object_name = 'vehicle'

#update vehicle
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class VehicleUpdateView(UpdateView):
    model=Vehicle
    fields=['registration_no','type','description','fuel_capacity']
    template_name = 'vehicle/update_vehicle.html'
    def get_success_url(self):
        return reverse('view-vehicle',kwargs={'pk':self.object.pk})

#delete vehicle
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class VehicleDeleteView(DeleteView):
    model=Vehicle
    template_name = 'vehicle/delete_vehicle.html'
    success_url = reverse_lazy('list-vehicles')

#list vehicles
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicle/list_vehicles.html'
    context_object_name = 'vehicles'
    
####################trips########################

#new trip
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class TripCreateView(CreateView):
    model=Trip
    fields=['request','vehicles','drivers','start_time']
    template_name = 'trip/new_trip.html'
    success_url = reverse_lazy('list-trips')


#trip details
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class TripDetailView(DetailView):
    model=Trip
    template_name = 'trip/view_trip.html'
    context_object_name = 'trip'

#update trip
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class TripUpdateView(UpdateView):
    model=Trip
    template_name = 'trip/update_trip.html'
    fields = ['start_distance_reading','end_distance_reading','start_time','end_time',
              'vehicles','drivers']
    def get_success_url(self):
        return reverse('view-trip',kwargs={'pk':self.object.pk})

#list trips
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class TripListView(ListView):
    model = Trip
    template_name = 'trip/list_trips.html'
    context_object_name = 'trips'

@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class TripStartView(UpdateView):
    model = Trip
    template_name = 'trip/start_trip.html'
    fields = ['start_time','start_distance_reading','vehicles','drivers']
    context_object_name = 'trip'

@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class TripEndView(UpdateView):
    model = Trip
    fields = ['end_time','start_distance_reading','end_distance_reading']
    template_name = 'trip/end_trip.html'


    def get_context_data(self, **kwargs):
        context = super(TripEndView, self).get_context_data(**kwargs)
        if Trip.objects.get(id=self.kwargs['pk']).status==TripStatus.objects.get(type='Completed'):
            raise PermissionDenied
        request=Trip.objects.get(pk=self.object.pk).request
        context['request'] = request
        return context

    def get_object(self, queryset=None):
        obj=super(TripEndView,self).get_object()
        obj.status=TripStatus.objects.get(type='Completed')
        return obj

    def get_success_url(self):
        return reverse('view-trip', kwargs={'pk': self.object.pk})