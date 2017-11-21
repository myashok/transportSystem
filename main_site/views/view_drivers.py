from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from main_site.decorators import  check_priveleged
from main_site.forms import DriverForm
from main_site.models import Driver, Trip


#create driver
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class DriverCreateView(CreateView):
    model = Driver
    form_class = DriverForm
    template_name = 'driver/new.html'
    success_url = reverse_lazy('list-drivers')

#driver details
@method_decorator(login_required(login_url='login'), name='dispatch')
# @method_decorator(check_priveleged, name='dispatch')
class DriverDetailView(DetailView):
    model = Driver
    template_name = 'driver/view.html'
    context_object_name = 'driver'

#update driver
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class DriverUpdateView(UpdateView):
    model = Driver
    form_class = DriverForm
    template_name = 'driver/update.html'
    def get_success_url(self):
        return reverse('view-driver', kwargs={'pk': self.object.pk})

#delete driver
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class DriverDeleteView(DeleteView):
    model = Driver
    template_name = 'driver/delete.html'
    success_url = reverse_lazy('list-drivers')

#list drivers
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class DriverListView(ListView):
    model = Driver
    template_name = 'driver/list.html'
    context_object_name = 'drivers'


