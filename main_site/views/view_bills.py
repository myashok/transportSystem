from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from main_site.decorators import check_not_priveleged
from main_site.models import Bill


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_not_priveleged, name='dispatch')
class BillDetailView(View):
    def get(self, request, pk):
        bill = get_object_or_404(Bill, pk=pk)
        return HttpResponse('hello world')
        #return get_bill_as_pdf(request, bill)