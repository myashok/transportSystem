from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView

from main_site.decorators import check_priveleged
from main_site.models import Bill, Request, Status


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class BillCreateView(View):
   def get(self,request,pk):
       req=get_object_or_404(Request,pk=pk)
       trips=req.trip_set.all()
       return render(request, 'bill/new_bill.html', {'trips':trips})

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class BillDetailView(View):
    def get(self, request, pk):
        bill = get_object_or_404(Bill, pk=pk)
        return HttpResponse('hello world')
        #return get_bill_as_pdf(request, bill)