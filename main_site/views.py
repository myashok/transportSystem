from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, DateInput
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from main_site.models import Request

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
    return render(request,'home.html')

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
        return render(request,'registration/login.html')
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def transport_request(request):
    if request.method=='POST':
        form=RequestForm(request.POST)
        if form.is_valid():
            #add to database and redirectg
            return redirect('view_request',id=1)
        else:
            return render(request,'request_vehicle.html',{'form':form})
    else:
        form=RequestForm()
        return render(request,'request_vehicle.html',{'form':form})

def view_request(request,id):
    temp=Request.objects.get({'id':id})
    if temp.user is not request.user:
        return
    return render()
