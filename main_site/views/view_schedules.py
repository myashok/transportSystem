import os

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from main_site.decorators import  check_priveleged
from main_site.models import Schedule

#create schedule
from main_site.utils import render_schedule
from transport.settings import BASE_DIR


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class ScheduleCreateView(CreateView):
    model = Schedule
    fields = ['file']
    template_name = 'schedule/new.html'
    success_url = reverse_lazy('view-schedule')

#schedule details


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class ScheduleDetailView(View):
    def get(self,request):
        return render_schedule()

#update schedule
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class ScheduleUpdateView(UpdateView):
    model = Schedule
    fields = ['file']
    template_name = 'schedule/update.html'
    def get_success_url(self):
        return reverse('view-schedule', kwargs={'pk': self.object.pk})
