from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from main_site.views import DriverListView, DriverUpdateView, \
    DriverDeleteView, DriverCreateView, RequestListView, RequestUpdateView, RequestDetailView, DriverDetailView, \
    LoginView, LogoutView, VehicleCreateView, VehicleDetailView, VehicleUpdateView, VehicleDeleteView, VehicleListView, \
    TripDetailView, TripUpdateView, TripListView, TripEndView, TripStartView, BillDetailView, AnnouncementCreateView, \
    AnnouncementUpdateView, AnnouncementDeleteView, AnnouncementListView, HomeView
from . import views

urlpatterns=[
    url(r'^$', HomeView.as_view(), name='user-home'),
    url(r'^login',LoginView.as_view(),name='login'),
    url(r'^logout', LogoutView.as_view(), name='logout'),

    url(r'^staff$',TemplateView.as_view(template_name='staff_home.html'),name='staff-home'),

    url(r'^requests/new', views.RequestCreateView.as_view(), name='new-request'),
    url(r'^requests/(?P<pk>\d+)$', RequestDetailView.as_view(), name='view-request'),
    url(r'^requests/(?P<pk>\d+)/edit$', RequestUpdateView.as_view(), name='update-request'),
    url(r'^requests$', RequestListView.as_view(), name='list-requests'),

    url(r'^drivers/new$', DriverCreateView.as_view(), name='new-driver'),
    url(r'^drivers/(?P<pk>\d+)$', DriverDetailView.as_view(), name='view-driver'),
    url(r'^drivers/(?P<pk>\d+)/edit$', DriverUpdateView.as_view(), name='update-driver'),
    url(r'^drivers/(?P<pk>\d+)/delete$', DriverDeleteView.as_view(), name='delete-driver'),
    url(r'^drivers', DriverListView.as_view(), name='list-drivers'),

    url(r'^vehicles/new$', VehicleCreateView.as_view(), name='new-vehicle'),
    url(r'^vehicles/(?P<pk>\d+)$', VehicleDetailView.as_view(), name='view-vehicle'),
    url(r'^vehicles/(?P<pk>\d+)/edit$', VehicleUpdateView.as_view(), name='update-vehicle'),
    url(r'^vehicles/(?P<pk>\d+)/delete$', VehicleDeleteView.as_view(), name='delete-vehicle'),
    url(r'^vehicles', VehicleListView.as_view(), name='list-vehicles'),

    url(r'^requests/(?P<pk>\d+)/trips/new', views.TripCreateView.as_view(), name='new-trip'),
    url(r'^trips/(?P<pk>\d+)$', TripDetailView.as_view(), name='view-trip'),
    url(r'^trips/(?P<pk>\d+)/edit$', TripUpdateView.as_view(), name='update-trip'),
    url(r'^trips/(?P<pk>\d+)/start$', TripStartView.as_view(), name='start-trip'),
    url(r'^trips/(?P<pk>\d+)/end$', TripEndView.as_view(), name='end-trip'),
    url(r'^trips', TripListView.as_view(), name='list-trips'),

    # url(r'^bills/(?P<pk>\d+)$', BillDetailView.as_view(), name='view-bill'),

    url(r'^announcements/new$', AnnouncementCreateView.as_view(), name='new-announcement'),
    url(r'^announcements/(?P<pk>\d+)/edit$', AnnouncementUpdateView.as_view(), name='update-announcement'),
    url(r'^announcements/$', AnnouncementListView.as_view(), name='list-announcements'),
    url(r'^announcements/(?P<pk>\d+)/delete$', AnnouncementDeleteView.as_view(), name='delete-announcement'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
