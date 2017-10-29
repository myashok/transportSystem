from urllib.request import Request

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group
from django.forms import ModelForm, DateInput
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, ListView, DeleteView, CreateView, DetailView

from main_site.models import TransportRequest, Driver
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import UpdateView

import logging
logger = logging.getLogger(__name__)

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


class RequestForm(ModelForm):
    class Meta:
        model=TransportRequest
        fields=['date_of_journey','time_of_journey','request_type','description',
                'source','destination','is_return_journey']
        widgets = {
            'date_of_journey': DateInput(attrs={'type': 'date'}),
            'time_of_journey': DateInput(attrs={'type':'time'}),
        }


def check_not_staff(user):
    return True if not user.groups.filter(name='TransportStaff').exists() else False


def is_not_staff(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        check_not_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next', False):
                return redirect(request.GET.get('next'))
            else:
                if check_not_staff(request.user):
                    print(request.user.groups.all())
                    return redirect('staff_home')
                else:
                    return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    else:
        if request.user.is_authenticated:
            if has_group(request.user,'TransportStaff'):
                return redirect('staff_home')
            else:
                return redirect('home')
        else:
            return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


def my_requests(request):
    requests=TransportRequest.objects.filter(user=request.user)
    return render(request, 'transport_request/my_requests.html', {'requests':requests})

#####staff views#####
@login_required(login_url='login')
@is_not_staff(login_url='access_denied')
def staff_home(request):
    return render(request,'staff/home.html')


@login_required(login_url='login')
@is_not_staff(login_url='access_denied')
def view_requests(request):
    reqs=TransportRequest.objects.all().order_by('date_of_journey')
    return render(request,'staff/view_requests.html',{'requests':reqs})


def pending_requests(request):
    pending=TransportRequest.objects.filter(request_status='pending').order_by('date_of_journey')
    return render('pending.html',{'pending':pending})


def allot_vehicle(request,pk):
    req=TransportRequest.objects.get(pk=pk)
    return render(request,'staff/allot_vehicle.html',{'request':req})

def view_vehicles(request):
    pass

def view_conductors(request):
    pass


#create driver
@method_decorator(login_required(login_url='login'),name='dispatch')
class DriverCreateView(CreateView):
    model=Driver
    fields=['name','phone','license_no','license_validity','email','date_of_birth']
    template_name = 'driver/new_driver.html'
    success_url = reverse_lazy('list-drivers')

#read driver
@method_decorator(login_required(login_url='login'),name='dispatch')
class DriverDetailView(DetailView):
    model=Driver
    template_name = 'driver/view_driver.html'
    def get_context_data(self, **kwargs):
        context=super(DriverDetailView, self).get_context_data(**kwargs)
        context['now']=timezone.now()
        return context

#update driver
@method_decorator(login_required(login_url='login'),name='dispatch')
class DriverUpdateView(UpdateView):
    model=Driver
    fields=['name','phone','license_no','license_validity','email','date_of_birth']
    template_name = 'driver/update_driver.html'
    success_url = reverse_lazy('drivers')

#delete driver
@method_decorator(login_required(login_url='login'),name='dispatch')
class DriverDeleteView(DeleteView):
    model=Driver
    template_name = 'driver/delete_driver.html'
    success_url = reverse_lazy('list-drivers')

#list drivers
@method_decorator(login_required(login_url='login'),name='dispatch')
class DriverListView(ListView):
    model = Driver
    template_name = 'driver/list_drivers.html'
    context_object_name = 'drivers'

#create request
@method_decorator(login_required(login_url='login'),name='dispatch')
class RequestCreateView(CreateView):
    model=TransportRequest


class edit_request(UpdateView): #Note that we are using UpdateView and not FormView
    model = Request
    fields = ['date_of_journey', 'time_of_journey', 'request_type', 'description',
              'source', 'destination', 'is_return_journey']
    template_name = 'transport_request/new_request.html'
    success_url = reverse_lazy('list-requests')

#read request
@method_decorator(login_required(login_url='login'),name='dispatch')
class RequestDetailView(DetailView):
    model=TransportRequest
    template_name = 'transport_request/view_request.html'
    context_object_name = 'request'

#update request
@method_decorator(login_required(login_url='login'),name='dispatch')
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
