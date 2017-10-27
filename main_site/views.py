from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.forms import ModelForm, DateInput
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import UpdateView

from main_site.models import Request
from django.http import Http404
import logging
logger = logging.getLogger(__name__)
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


class RequestForm(ModelForm):
    class Meta:
        model=Request
        fields=['date_of_journey','time_of_journey','request_type','description',
                'source','destination','is_return_journey']
        widgets = {
            'date_of_journey': DateInput(attrs={'type': 'date'}),
            'time_of_journey': DateInput(attrs={'type':'time'}),
        }

def home(request):
    return render(request, 'user_home.html')

def login_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next', False):
                return redirect(request.GET.get('next'))
            else:
                return redirect('home')
        else:
            return render(request,'registration/login.html',{'error':'Invalid login credentials'})
    else:
        if request.user.is_authenticated:
            logger.info(request.user.groups.all())
            if has_group(request.user,'Admin'):
                return redirect('staff_home')
            else:
                return redirect('home')
        else:
            return render(request,'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def new_request(request):
    if request.method=='POST':
        form=RequestForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.save()
            return redirect('my_requests')
        else:
            return render(request, 'new_request.html', {'form':form})
    else:
        form=RequestForm()
        return render(request, 'new_request.html', {'form':form})


def my_requests(request):
    requests=Request.objects.filter(user=request.user)
    return render(request,'my_requests.html',{'requests':requests})


def view_request(request,pk):
    try:
        req = Request.objects.get(pk=pk)
        if req.user!=request.user:
            print(request.user.groups.all())
            if request.user.groups.filter(name='Transport_Admin').exists():
                return render(request, 'view_request.html', {'req': req})
            else:
                return redirect('/access_denied')

        else:
            return render(request, 'view_request.html', {'req': req})

    except Request.DoesNotExist:
        raise Http404




def delete_request(request,ID):
    req=Request.objects.get({'id':ID})
    req.delete()
    return redirect('user_home')
#####staff views#####
def not_in_staff_group(user):
    if user:
        return user.groups.filter(name='Staff').count() ==0
    return True
#@login_required(login_url='login')
@permission_required('request.user.is_staff',login_url='access_denied')
def staff_home(request):
    return render(request,'staff/staff_home.html')

def pending_requests(request):
    pending=Request.objects.filter(request_status='pending').order_by('date_of_journey')
    return render('pending.html',{'pending':pending})

class edit_request(UpdateView): #Note that we are using UpdateView and not FormView
    model = Request
    fields = ['date_of_journey', 'time_of_journey', 'request_type', 'description',
              'source', 'destination', 'is_return_journey']
    template_name = "new_request.html"
    success_url = '/requests'

