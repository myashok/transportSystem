from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, ListView, DeleteView, CreateView, DetailView
from main_site.decorators import is_not_priveleged, check_not_priveleged, check_owner_of_request
from main_site.models import TransportRequest, Driver, RequestStatus, Vehicle, Trip, TripStatus, Bill, Announcement
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import UpdateView
# from main_site.utils import  get_bill_as_pdf

class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if is_not_priveleged(request.user):
                return redirect('user-home')
            else:
                return redirect('staff-home')

        else:
            return render(request,'login.html',{'error':'Invalid credentials. \nPlease contact admin if facing issues.'})

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
        return redirect('user-home')


####################driver##################


#create driver
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class DriverCreateView(CreateView):
    model=Driver
    fields=['name','picture','phone','license_no','license_validity','email','blood_group']
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
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class DriverUpdateView(UpdateView):
    model=Driver
    fields=['name','picture','phone','license_no','license_validity','email','blood_group']
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
@method_decorator(check_owner_of_request,name='dispatch')
class RequestDetailView(DetailView):
    model=TransportRequest
    template_name = 'transport_request/view_request.html'
    context_object_name = 'request'

#update request
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_owner_of_request,name='dispatch')
class RequestUpdateView(UpdateView):
    model=TransportRequest
    fields = ['date_of_journey', 'time_of_journey', 'request_type', 'description',
              'source', 'destination', 'is_return_journey']
    template_name = 'transport_request/update_request.html'
    def get_success_url(self):
        return reverse('view-request',kwargs={'pk':self.object.pk})

@method_decorator(login_required(login_url='login'), name='dispatch')
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
    fields=['vehicles','drivers','start_time']
    template_name = 'trip/new_trip.html'
    success_url = reverse_lazy('list-trips')
    def get_context_data(self, **kwargs):
        context=super(TripCreateView,self).get_context_data(**kwargs)
        req=get_object_or_404(TransportRequest,pk=self.kwargs['pk'])
        context['req']=req
        context['start_time']=req.time_of_journey
        return context
    def form_valid(self, form):
        trip=form.save(commit=False)
        trip.request.status = RequestStatus.objects.get(type='Accepted')
        trip.request.save()
        trip.request=self.get_context_data()['req']
        return super(TripCreateView,self).form_valid(form)

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

#trip start view
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class TripStartView(UpdateView):
    model = Trip
    template_name = 'trip/start_trip.html'
    fields = ['start_time','start_distance_reading','vehicles','drivers']
    context_object_name = 'trip'
    success_url = reverse_lazy('list-trips')
    def form_valid(self, form):
        trip=form.save(commit=False)
        trip.status=TripStatus.objects.get(type='Active')
        return super(TripStartView,self).form_valid(form)

@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class TripEndView(UpdateView):
    model = Trip
    fields = ['start_time','end_time','start_distance_reading','end_distance_reading']
    template_name = 'trip/end_trip.html'
    success_url = reverse_lazy('list-trips')
    def get_context_data(self, **kwargs):
        context=super(TripEndView,self).get_context_data(**kwargs)
        trip=get_object_or_404(Trip,pk=self.kwargs['pk'])
        if trip.status==TripStatus.objects.get(type='Active'):
            return context
        else:
            raise PermissionDenied()
    def form_valid(self, form):
        total_distance=self.object.end_distance_reading-self.object.start_distance_reading
        rate=self.object.request.request_type.rate
        fare=rate*total_distance
        bill=Bill(datetime_of_generation=datetime.now(),trip=self.object,total_distance=total_distance, \
            total_fare=fare)
        bill.save()
        return super(TripEndView,self).form_valid(form)

    def get_success_url(self):
        return reverse('view-bill', kwargs={'pk': self.object.bill.pk})

####################bill#################

@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class BillDetailView(View):
    def get(self,request,pk):
        bill=get_object_or_404(Bill,pk=pk)
        return get_bill_as_pdf(request,bill)

#############announcements###############


@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class AnnouncementCreateView(CreateView):
    model = Announcement
    fields = ['text','description']
    template_name = 'announcement/new_announcement.html'
    success_url = reverse_lazy('list-announcements')


#announcments details
@method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(check_not_priveleged,name='dispatch')
class AnnouncementDetailView(DetailView):
    model=Announcement
    template_name = 'announcement/list_announcement.html'
    context_object_name = 'announcements'


class AnnouncementUpdateView(UpdateView):
    model = Announcement
    fields = ['text', 'description']
    template_name = 'announcement/update_announcement.html'
    success_url = reverse_lazy('list-announcements')


class AnnouncementDeleteView(DeleteView):
    model = Announcement
    template_name = "announcement/delete_announcement.html"
