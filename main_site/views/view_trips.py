from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from main_site.decorators import check_priveleged
from main_site.forms import TripCreateForm
from main_site.models import Trip, Request, Status, Bill
from main_site.utils import send_html_mail, generate_mp3


#new trip
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class TripCreateView(CreateView):
    model = Trip
    form_class = TripCreateForm
    template_name = 'trip/new.html'

    def get_context_data(self, **kwargs):
        context = super(TripCreateView, self).get_context_data(**kwargs)
        req = get_object_or_404(Request, pk=self.kwargs['pk'])
        if req.status==Status.objects.get(type='Request Cancelled'):
            raise PermissionDenied('Cannnot make trips for a cancelled request')
        elif Bill.objects.filter(request=req).exists():
            raise PermissionDenied('Trip cannot be created after billing')
        context['req'] = req
        return context

    def form_valid(self, form):
        trip = form.save(commit=False)
        trip.request = self.get_context_data()['req']
        trip.request.status=Status.objects.get(type='Request Approved')
        trip.request.save()
        response=super(TripCreateView, self).form_valid(form)
        html_content=render_to_string('custom_templates/trip_created.html',{'trip':trip})
        to=[]
        if trip.request.user.email is not None:
            to.append(trip.request.user.email)
        if trip.driver.email is not None:
            to.append(trip.driver.email)
        send_html_mail('Trip for request #'+str(trip.request_id)+'created',
                           html_content,to)

        generate_mp3(trip)
        return response
    def get_success_url(self):
        return reverse('list-trips',kwargs={'pk':self.kwargs['pk']})

# trip details
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class TripDetailView(DetailView):
    model = Trip
    template_name = 'trip/view.html'
    context_object_name = 'trip'


# update trip
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class TripCancelView(View):
    def get(self,request,*args,**kwargs):
        trip=get_object_or_404(Trip,pk=kwargs['pk'])
        if trip.status==Status.objects.get(type="Trip Cancelled"):
            raise PermissionDenied('This trip has already been cancelled')
        elif Bill.objects.filter(request=trip.request).exists():
            raise PermissionDenied('Trip cannot be cancelled after billing')
        trip.status=Status.objects.get(type='Trip Cancelled')
        trip.save()
        if not trip.request.trip_set.filter(status=Status.objects.get(type='Trip Scheduled')).exists():
            trip.request.status=Status.objects.get(type='Request Pending')
            trip.request.save()
        to=[]
        if trip.driver.email is not None:
            to.append(trip.driver.email)
        if trip.request.user.email is not None:
            to.append(trip.request.user.email)
        html_content=render_to_string('custom_templates/trip_cancelled.html',{'trip':trip})
        send_html_mail('Trip # '+str(trip.id)+' cancelled',
                       html_content,
                       to)
        return redirect('view-trip',pk=trip.pk)

# list trips
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class TripListView(ListView):
    model = Trip
    template_name = 'trip/list.html'
    context_object_name = 'trips'
    def get_queryset(self):
        req=get_object_or_404(Request,pk=self.kwargs['pk'])
        return Trip.objects.filter(request=req)

@method_decorator(login_required(login_url='login'), name='dispatch')
class UserTripListView(ListView):
    model = Trip
    template_name = 'user-trip/list.html'
    context_object_name = 'trips'
    def get_queryset(self):
        req=get_object_or_404(Request,pk=self.kwargs['pk'])
        return Trip.objects.filter(request=req)
