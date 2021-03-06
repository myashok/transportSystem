from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf.urls import url

# from main_site.views.view_feedback import FeedbackCreateView, FeedbackListView, FeedbackDetailView
from main_site.views.view_feedback import FeedbackCreateView, FeedbackListView, FeedbackDetailView
from main_site.views.view_maintenences import MaintenanceCreateView, MaintenanceDetailView, MaintenanceEndView, \
    MaintenanceListView, MaintenanceUpdateView
from main_site.views.view_schedules import ScheduleDetailView, ScheduleUpdateView
from main_site.views.views import UserHomeView, LoginView, LogoutView, StaffHomeView, FareCalculatorView, PlayTripView, \
    PlayView
from main_site.views.view_announcements import AnnouncementCreateView, AnnouncementUpdateView, AnnouncementListView, \
    AnnouncementDeleteView, AnnouncementDetailView
from main_site.views.view_bills import BillDetailView, BillCreateView
from main_site.views.view_drivers import DriverCreateView, DriverDetailView, DriverUpdateView, DriverDeleteView, \
    DriverListView
from main_site.views.view_requests import RequestDetailView, RequestListView, MyRequestsView, RequestCreateView, RequestCancelView
from main_site.views.view_trips import TripCreateView, TripDetailView, TripCancelView, TripListView, UserTripListView
from main_site.views.view_vehicles import VehicleCreateView, VehicleDetailView, VehicleUpdateView, VehicleDeleteView, \
    VehicleListView

urlpatterns=[
    url(r'^$', UserHomeView.as_view(), name='user-home'),
    url(r'^login',LoginView.as_view(),name='login'),
    url(r'^logout', LogoutView.as_view(), name='logout'),

    url(r'^staff$', StaffHomeView.as_view(),name='staff-home'),

    url(r'^requests/new', RequestCreateView.as_view(), name='new-request'),
    url(r'^requests/(?P<pk>\d+)$', RequestDetailView.as_view(), name='view-request'),
    url(r'^requests/(?P<pk>\d+)/cancel$', RequestCancelView.as_view(), name='cancel-request'),
    url(r'^requests[/]$', RequestListView.as_view(), name='list-requests'),
    url(r'^myrequests[/]$',MyRequestsView.as_view(),name='my-requests'),

    url(r'^drivers/new[/]$', DriverCreateView.as_view(), name='new-driver'),
    url(r'^drivers/(?P<pk>\d+)$', DriverDetailView.as_view(), name='view-driver'),
    url(r'^drivers/(?P<pk>\d+)/edit[/]$', DriverUpdateView.as_view(), name='update-driver'),
    url(r'^drivers/(?P<pk>\d+)/delete[/]$', DriverDeleteView.as_view(), name='delete-driver'),
    url(r'^drivers[/]$', DriverListView.as_view(), name='list-drivers'),

    url(r'^vehicles/new$', VehicleCreateView.as_view(), name='new-vehicle'),
    url(r'^vehicles/(?P<pk>\d+)$', VehicleDetailView.as_view(), name='view-vehicle'),
    url(r'^vehicles/(?P<pk>\d+)/edit$', VehicleUpdateView.as_view(), name='update-vehicle'),
    url(r'^vehicles/(?P<pk>\d+)/delete$', VehicleDeleteView.as_view(), name='delete-vehicle'),
    url(r'^vehicles', VehicleListView.as_view(), name='list-vehicles'),

    url(r'^requests/(?P<pk>\d+)/trips/new', TripCreateView.as_view(), name='new-trip'),
    url(r'^trips/(?P<pk>\d+)$', TripDetailView.as_view(), name='view-trip'),
    url(r'^trips/(?P<pk>\d+)/cancel$', TripCancelView.as_view(), name='cancel-trip'),
    url(r'^requests/(?P<pk>\d+)/trips', TripListView.as_view(), name='list-trips'),
    url(r'^myrequests/(?P<pk>\d+)/trips', UserTripListView.as_view(), name='list-user-trips'),

    url(r'^requests/(?P<pk>\d+)/billing$', BillCreateView.as_view(), name='new-bill'),
    url(r'^requests/(?P<pk>\d+)/bill$', BillDetailView.as_view(), name='view-bill'),

    url(r'^announcements/new$', AnnouncementCreateView.as_view(), name='new-announcement'),
    url(r'^announcements/(?P<pk>\d+)$', AnnouncementDetailView.as_view(), name='view-announcement'),
    url(r'^announcements/(?P<pk>\d+)/edit$', AnnouncementUpdateView.as_view(), name='update-announcement'),
    url(r'^announcements/(?P<pk>\d+)/delete$', AnnouncementDeleteView.as_view(), name='delete-announcement'),
    url(r'^announcements/$', AnnouncementListView.as_view(), name='list-announcements'),

    url(r'^maintenances/new$', MaintenanceCreateView.as_view(), name='new-maintenance'),
    url(r'^maintenances[/]$', MaintenanceListView.as_view(), name='list-maintenances'),
    url(r'^maintenances/(?P<pk>\d+)$', MaintenanceDetailView.as_view(), name='view-maintenance'),
    url(r'^maintenances/(?P<pk>\d+)/end$', MaintenanceEndView.as_view(), name='end-maintenance'),
    url(r'^maintenances/(?P<pk>\d+)/update$', MaintenanceUpdateView.as_view(), name='update-maintenance'),

    url(r'^schedule[/]$', ScheduleDetailView.as_view(), name='view-schedule'),
    url(r'^schedule/update[/]$', ScheduleUpdateView.as_view(), name='update-schedule'),

    url(r'^fare_calculator[/]$', FareCalculatorView.as_view(), name='fare-calculator'),


    url(r'^feedbacks/new$', FeedbackCreateView.as_view(), name='new-feedback'),
    url(r'^feedbacks[/]$', FeedbackListView.as_view(), name='list-feedbacks'),
    url(r'^feedbacks/(?P<pk>\d+)$', FeedbackDetailView.as_view(), name='view-feedback'),

    #playing trips
    url(r'^play_trips$', PlayTripView.as_view(), name='play-trips'),
    url(r'^play/(?P<name>\w+).mp3$', PlayView.as_view(), name='play'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
