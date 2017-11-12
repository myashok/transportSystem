from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView

from main_site.decorators import check_not_priveleged
from main_site.models import Vehicle

# create vehicle
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_not_priveleged, name='dispatch')
class VehicleCreateView(CreateView):
    model = Vehicle
    fields = ['registration_no','nickname', 'description', 'seating_capacity'
              ,'is_owned','picture']
    template_name = 'vehicle/new_vehicle.html'
    success_url = reverse_lazy('list-vehicles')

# vehicle details
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_not_priveleged, name='dispatch')
class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicle/view_vehicle.html'
    context_object_name = 'vehicle'


# update vehicle
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_not_priveleged, name='dispatch')
class VehicleUpdateView(UpdateView):
    model = Vehicle
    fields = ['registration_no', 'nickname', 'description', 'seating_capacity'
            ,'is_owned', 'picture']
    template_name = 'vehicle/update_vehicle.html'

    def get_success_url(self):
        return reverse('view-vehicle', kwargs={'pk': self.object.pk})

# delete vehicle
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_not_priveleged, name='dispatch')
class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = 'vehicle/delete_vehicle.html'
    success_url = reverse_lazy('list-vehicles')

# list vehicles
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_not_priveleged, name='dispatch')
class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicle/list_vehicles.html'
    context_object_name = 'vehicles'