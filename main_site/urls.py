from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns=[
    url(r'^$',views.home,name='home'),
    url(r'^login$',views.login_view,name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^transport_request',views.transport_request,name='transport_request'),
    url(r'^transport_request/(?P<id>\d+)',views.view_request,name='view_request'),
    url(r'^my_requests$',views.my_requests,name='my_requests'),
    url(r'^staff$',views.staff_home,name='staff_home'),
    url(r'^staff/pending_requests$',views.pending_requests,name='pending_requests'),
    url(r'^access_denied$',TemplateView.as_view(template_name='access_denied.html'),name='access_denied')
]
