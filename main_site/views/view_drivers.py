from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from main_site.decorators import  check_priveleged
from main_site.models import Driver

#create driver
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class DriverCreateView(CreateView):
    model = Driver
    fields = ['name','phone','emergency_contact','address','blood_group',
              'license_no', 'license_validity', 'email','picture']
    template_name = 'driver/new_driver.html'
    success_url = reverse_lazy('list-drivers')

#driver details
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class DriverDetailView(DetailView):
    model = Driver
    template_name = 'driver/view_driver.html'
    context_object_name = 'driver'

#update driver
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class DriverUpdateView(UpdateView):
    model = Driver
    fields = ['name', 'phone', 'emergency_contact', 'address', 'blood_group',
              'license_no', 'license_validity', 'email', 'picture']
    template_name = 'driver/update_driver.html'
    def get_success_url(self):
        return reverse('view-driver', kwargs={'pk': self.object.pk})

#delete driver
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class DriverDeleteView(DeleteView):
    model = Driver
    template_name = 'driver/delete_driver.html'
    success_url = reverse_lazy('list-drivers')

#list drivers
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class DriverListView(ListView):
    model = Driver
    template_name = 'driver/list_drivers.html'
    context_object_name = 'drivers'
