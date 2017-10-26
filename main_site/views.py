from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.forms import ModelForm, DateInput
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from main_site.models import Request
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

def access_denied(request):
    return render(request,'access_denied.html')

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
def transport_request(request):
    if request.method=='POST':
        form=RequestForm(request.POST)
        if form.is_valid():
            req=Request(form)
            req.save()
        else:
            return render(request,'request_vehicle.html',{'form':form})
    else:
        form=RequestForm()
        return render(request,'request_vehicle.html',{'form':form})

def my_requests(request):
    requests=Request.objects.filter(user=request.user)
    return render(request,'my_requests.html',{'requests':requests})

def view_request(request,id):

    temp=Request.objects.get({'id':id})
    if temp.user is not request.user:
        return
    return render()

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

