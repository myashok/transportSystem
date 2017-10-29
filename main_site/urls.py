from django.conf.urls import url
from django.views.generic import TemplateView
from main_site.views import DriverListView, DriverUpdateView, \
    DriverDeleteView, DriverCreateView, RequestListView, RequestUpdateView, RequestDetailView, DriverDetailView
from . import views

urlpatterns=[
    url(r'^$',TemplateView.as_view(template_name='home.html'),name='home'),
    url(r'^login',views.login_view,name='login'),
    url(r'^logout', views.logout_view, name='logout'),

    url(r'^staff$',views.staff_home,name='staff_home'),
    url(r'^staff/allot_vehicle/(?P<pk>\d+)$',views.allot_vehicle,name='allot_vehicle'),
    url(r'^staff/view_requests$',views.view_requests,name='view_requests'),
    url(r'^staff/view_vehicles',views.view_vehicles,name='view_vehicles'),
    url(r'^staff/view_',views.view_conductors,name='view_conductors'),

    url(r'^requests/new', views.RequestCreateView.as_view(), name='new-request'),
    url(r'^requests/(?P<pk>\d+)$', RequestDetailView.as_view(), name='view-request'),
    url(r'^requests/(?P<pk>\d+)/edit$', RequestUpdateView.as_view(), name='update-request'),
    url(r'^requests', RequestListView.as_view(), name='list-requests'),

    url(r'^drivers/new$', DriverCreateView.as_view(), name='new-driver'),
    url(r'^drivers/(?P<pk>\d+)$', DriverDetailView.as_view(), name='view-driver'),
    url(r'^drivers/(?P<pk>\d+)/edit$', DriverUpdateView.as_view(), name='update-driver'),
    url(r'^drivers/(?P<pk>\d+)/delete$', DriverDeleteView.as_view(), name='delete-driver'),
    url(r'^drivers', DriverListView.as_view(), name='list-drivers'),

    url(r'^access_denied$', TemplateView.as_view(template_name='access_denied.html'), name='access_denied'),

]
