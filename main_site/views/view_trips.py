from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from main_site.decorators import check_priveleged
from main_site.models import Trip, Request, Status

# new trip
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class TripCreateView(CreateView):
    model = Trip
    fields = ['vehicle', 'driver', 'rate']
    template_name = 'trip/new.html'

    def get_context_data(self, **kwargs):
        context = super(TripCreateView, self).get_context_data(**kwargs)
        req = get_object_or_404(Request, pk=self.kwargs['pk'])
        context['req'] = req
        return context

    def form_valid(self, form):
        trip = form.save(commit=False)
        trip.request = self.get_context_data()['req']
        trip.save()
        return super(TripCreateView, self).form_valid(form)
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
        trip.status=Status.objects.get(type='Trip Cancelled')
        trip.save()
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
