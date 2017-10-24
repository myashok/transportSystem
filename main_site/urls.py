from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.home,name='home'),
    url(r'^login$',views.login_view,name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^transport_request',views.transport_request,name='transport_request'),
    url(r'^transport_request/(?P<id>\d+)',views.view_request,name='view_request')
]
