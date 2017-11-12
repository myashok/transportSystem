
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from main_site.decorators import check_not_priveleged, check_owner_of_request
from main_site.models import Request

#create request
@method_decorator(login_required(login_url='login'), name='dispatch')
class RequestCreateView(CreateView):
    model = Request
    template_name = 'request/new_request.html'
    fields = ['start_date', 'start_time','end_date','expected_end_time' ,
              'no_of_persons_travelling','request_type', 'description',
              'source', 'destination',  'is_round_trip']

    def form_valid(self, form):
        request = form.save(commit=False)
        request.user = self.request.user
        try:
            print('test')
            #send_email('Transport request received','Hi, we have received your request',['nik211012@gmail.com'])
        except OSError as e:
            print(e.strerror)
        return super(RequestCreateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('view-request', kwargs={'pk': self.object.pk})

#read request
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_owner_of_request, name='dispatch')
class RequestDetailView(DetailView):
    model = Request
    template_name = 'request/view_request.html'
    context_object_name = 'request'


#update request
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_not_priveleged, name='dispatch')
class RequestUpdateView(UpdateView):
    model = Request
    fields = ['start_date', 'start_time', 'end_date', 'expected_end_time',
              'no_of_persons_travelling', 'request_type', 'description',
              'source', 'destination', 'is_round_trip']
    template_name = 'request/update_request.html'

    def get_object(self, *args, **kwargs):
        obj = super(RequestUpdateView, self).get_object(*args, **kwargs)
        if obj.trip_set.exists():
            raise PermissionDenied()
        return obj
    def get_success_url(self):
        return reverse('view-request', kwargs={'pk': self.object.pk})

#list requests
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_not_priveleged, name='dispatch')
class RequestListView(ListView):
    model = Request
    template_name = 'request/list_requests.html'
    context_object_name = 'requests'

#my requests
@method_decorator(login_required(login_url='login'), name='dispatch')
class MyRequestsView(ListView):
    model = Request
    template_name = 'request/my_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)
