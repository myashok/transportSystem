from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from main_site.decorators import check_priveleged
from main_site.models import Bill, Request, Trip, Status
from main_site.utils import get_bill_as_pdf


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class BillDetailView(View):
    def get(self, request, pk):
        bill = get_object_or_404(Bill, pk=pk)
        #return render(request,'bill/view_bill.html',{'bill':bill})
        return get_bill_as_pdf(request, bill)

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class BillCreateView(View):

    def get(self,request,pk):
        Tripset = modelformset_factory(Trip, fields=['start_distance', 'end_distance', 'rate'], extra=0)
        req=get_object_or_404(Request,pk=pk)
        if req.status==Status.objects.get(type='Request Cancelled'):
           raise PermissionDenied()
        tripformset=Tripset(queryset=req.trip_set.all())
        return render(request, 'bill/new_bill.html', {'forms':tripformset})
    def post(self,request,pk):
        req=get_object_or_404(Request,pk=pk)
        Tripset = modelformset_factory(Trip, fields=['start_distance', 'end_distance', 'rate'], extra=0)
        tripformset=Tripset(request.POST)
        if tripformset.is_valid():
            dist=0
            fare=0
            for form in tripformset:
                trip=form.save(commit=False)
                temp_dist=(trip.end_distance-trip.start_distance)
                trip.fare=trip.rate*temp_dist
                dist+=temp_dist
                fare+=trip.fare
                trip.save()
            try:
                bill=Bill.objects.get(request=req)
            except Bill.DoesNotExist:
                bill=Bill(request=req)
            bill.total_distance=dist
            bill.total_fare=fare
            bill.save()
            return redirect(reverse('view-bill', kwargs={'pk': bill.pk}))