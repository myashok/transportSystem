from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from main_site.decorators import is_not_priveleged, check_priveleged
from main_site.models import Announcement
from django.contrib.auth import authenticate, login, logout

class UserHomeView(TemplateView):
    def get(self, request, **kwargs):
        announcements = Announcement.objects.all()
        return render(request, 'home.html', {'announcements': announcements})

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class StaffHomeView(View):
    def get(self, request):
        announcements = Announcement.objects.all()
        return render(request, 'staff_home.html', {'announcements': announcements})


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


# # trip start view
# @method_decorator(login_required(login_url='login'), name='dispatch')
# @method_decorator(check_priveleged, name='dispatch')
# class TripStartView(UpdateView):
#     model = Trip
#     template_name = 'trip/start_trip.html'
#     fields = ['start_time', 'start_distance_reading', 'vehicles', 'drivers']
#     context_object_name = 'trip'
#     success_url = reverse_lazy('list-trips')
#
#     def get_context_data(self, **kwargs):
#         if self.object.status == 'Trip Completed' or self.object.status == 'Trip Active':
#             raise PermissionDenied()
#         return super(TripStartView, self).get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         trip = form.save(commit=False)
#         trip.status='Trip Active'
#         trip.save()
#         return super(TripStartView, self).form_valid(form)
#
#
# @method_decorator(login_required(login_url='login'), name='dispatch')
# @method_decorator(check_priveleged, name='dispatch')
# class TripEndView(UpdateView):
#     model = Trip
#     fields = ['start_time', 'end_time', 'start_distance_reading', 'end_distance_reading']
#     template_name = 'trip/end_trip.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(TripEndView, self).get_context_data(**kwargs)
#         if self.object.status == 'Trip Active':
#             return context
#         else:
#             raise PermissionDenied()
#
#     def form_valid(self, form):
#         total_distance = self.object.end_distance_reading - self.object.start_distance_reading
#         rate = self.object.request.request_type.rate
#         fare = rate * total_distance
#         if Bill.objects.filter(trip=self.object).exists():
#             bill=Bill.objects.get(trip=self.object)
#             bill.datetime_of_generation=datetime.now()
#             bill.total_fare=fare
#             bill.total_distance=total_distance
#             bill.save()
#         else:
#             bill = Bill(datetime_of_generation=datetime.now(), trip=self.object, total_distance=total_distance, \
#                     total_fare=fare)
#             bill.save()
#         return super(TripEndView, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse('view-bill', kwargs={'pk': self.object.bill.pk})
#

