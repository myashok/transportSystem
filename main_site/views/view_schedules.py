import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView
from main_site.decorators import  check_priveleged
from main_site.models import Schedule

#schedule details
from transport.settings import STATIC_URL, MEDIA_ROOT


@method_decorator(login_required(login_url='login'), name='dispatch')
class ScheduleDetailView(View):
    def get(self,request):
        schedule=Schedule.load()
        data = open(os.path.join(MEDIA_ROOT,schedule.file.name),'rb')
        response = HttpResponse(content=data)
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'inline; filename="%s.pdf"' \
                                          % 'schedule'
        return response

#update schedule
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class ScheduleUpdateView(UpdateView):
    model = Schedule
    fields = ['file']
    template_name = 'schedule/update.html'
    def get_object(self, queryset=None):
        return Schedule.load()
    def get_success_url(self):
        return reverse('view-schedule')
