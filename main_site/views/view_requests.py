from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from main_site.decorators import check_priveleged, check_owner_of_request, is_not_priveleged
from main_site.forms import RequestForm
from main_site.models import Request, Status, Bill
from main_site.utils import send_html_mail


@method_decorator(login_required(login_url='login'), name='dispatch')
class RequestCreateView(CreateView):
    model = Request
    template_name = 'request/new.html'
    form_class = RequestForm

    def form_valid(self, form):
        request = form.save(commit=False)
        request.user = self.request.user
        self.status = Status.objects.get(type='Request Pending')
        response=super(RequestCreateView, self).form_valid(form)
        msg_html = render_to_string('custom_templates/request_created.html', {'request': request})
        if request.user.email is not None:
            send_html_mail('Booking Request Received', msg_html, [request.user.email])
        return response

    def get_success_url(self):
        return reverse('view-request', kwargs={'pk': self.object.pk})

@method_decorator(login_required(login_url='login'), name='dispatch')
class RequestDetailView(DetailView):
    model = Request
    template_name = 'request/view.html'
    context_object_name = 'request'
    def get_object(self, queryset=None):
        obj=super(RequestDetailView,self).get_object()
        if is_not_priveleged(self.request.user) and obj.user!=self.request.user:
            raise PermissionDenied('You are not priveleged to see this page')
        return obj


# not allowing updation of request for now
# @method_decorator(login_required(login_url='login'), name='dispatch')
# @method_decorator(check_not_priveleged, name='dispatch')
# class RequestUpdateView(UpdateView):
#     model = Request
#     fields = ['start_date', 'start_time', 'end_date', 'expected_end_time',
#               'no_of_persons_travelling', 'request_type', 'description',
#               'source', 'destination', 'is_round_trip']
#     template_name = 'request/end.html'
#
#     def get_object(self, *args, **kwargs):
#         obj = super(RequestUpdateView, self).get_object(*args, **kwargs)
#         if obj.trip_set.exists() or obj.status==Status.objects.get('Request Cancelled'):
#             raise PermissionDenied()
#         return obj
#     def get_success_url(self):
#         return reverse('view-request', kwargs={'pk': self.object.pk})

#list requests
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class RequestListView(ListView):
    model = Request
    template_name = 'request/list.html'
    context_object_name = 'requests'

#my requests
@method_decorator(login_required(login_url='login'), name='dispatch')
class MyRequestsView(ListView):
    model = Request
    template_name = 'request/my_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_owner_of_request, name='dispatch')
class RequestCancelView(View):
    def get(self,request,pk):
        req=get_object_or_404(Request,pk=pk)
        if req.status==Status.objects.get(type='Request Cancelled'):
            raise PermissionDenied('Trying to cancel already cancelled request?')
        elif Bill.objects.filter(request=req).exists():
            raise PermissionDenied('Trip cannot be cancelled after billing')
        elif req.trip_set.filter(status=Status.objects.get(type='Trip Scheduled')).exists():
            raise  PermissionDenied('Request cannot be cancelled as trip has already been scheduled')
        elif datetime.now() >= datetime.combine(req.start_date,req.start_time):
            raise PermissionDenied('Request cannot be cancelled after the scheduled time. Please contact admin for help.')


        req.status=Status.objects.get(type='Request Cancelled')
        req.save()
        trips=req.trip_set.all()
        if trips.exists():
            for t in trips:
                t.status=Status.objects.get(type='Trip Cancelled')
                t.save()
        if req.user.email is not None:
            html_content=render_to_string('custom_templates/request_cancelled.html',{'request':req})
            send_html_mail('Request #'+str(req.id)+' cancelled',
                           html_content,[req.user.email])
        return redirect('view-request',pk=pk)
