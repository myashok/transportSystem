from django.conf.urls import url
from django.views.generic import TemplateView
from main_site.views import edit_request
from . import views

urlpatterns=[
    url(r'^$',views.home,name='home'),
    url(r'^login',views.login_view,name='login'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^requests/new', views.new_request, name='new_request'),
    url(r'^requests/(?P<pk>\d+)$', views.view_request, name='view_request'),
    url(r'^requests$',views.my_requests,name='my_requests'),
    url(r'^requests/(?P<pk>\d+)/edit$',edit_request.as_view(),name='edit_request'),
    url(r'^staff$',views.staff_home,name='staff_home'),
    url(r'^staff/pending_requests$',views.pending_requests,name='pending_requests'),
    url(r'^accesss_denied$',TemplateView.as_view(template_name='access_denied.html'),name='access_denied')
]
