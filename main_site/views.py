from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from main_site.decorators import is_not_priveleged, check_not_priveleged
from main_site.models import Announcement
from django.contrib.auth import authenticate, login, logout

class UserHomeView(TemplateView):
    def get(self, request, **kwargs):
        announcements = Announcement.objects.all()
        return render(request, 'home.html', {'announcements': announcements})


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_not_priveleged, name='dispatch')
class StaffHomeView(View):
    def get(self, request):
        announcements = Announcement.objects.all()
        return render(request, 'staff_home.html',  {'announcements': announcements})


class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if is_not_priveleged(request.user):
                return redirect('user-home')
            else:
                return redirect('staff-home')

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})

    def get(self, request):
        if request.user.is_authenticated:
            if is_not_priveleged(request.user):
                return redirect('user-home')
            else:
                return redirect('staff-home')

        return render(request, 'login.html')

@method_decorator(login_required(login_url='login'), name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

