from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from main_site.decorators import  check_priveleged
from main_site.forms import  MaintenanceEndForm
from main_site.models import Maintenance, Maintenance, Status


#create maintenance
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class MaintenanceCreateView(CreateView):
    model = Maintenance
    fields = ['vehicle','start_date','start_time']
    template_name = 'maintenance/new.html'
    success_url = reverse_lazy('list-maintenances')

#maintenance details
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class MaintenanceDetailView(DetailView):
    model = Maintenance
    template_name = 'maintenance/view.html'
    context_object_name = 'maintenance'

#update maintenance
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class MaintenanceEndView(UpdateView):
    model = Maintenance
    form_class = MaintenanceEndForm
    template_name = 'maintenance/update.html'
    def form_valid(self, form):
        temp=form.save(commit=False)
        temp.status=Status.objects.get(type='Maintenance Completed')
        temp.save()
        return super(MaintenanceEndView,self).form_valid(form)

    def get_success_url(self):
        return reverse('view-maintenance', kwargs={'pk': self.object.pk})

#list drivers
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class MaintenanceListView(ListView):
    model = Maintenance
    template_name = 'maintenance/list.html'
    context_object_name = 'maintenances'
