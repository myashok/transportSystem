from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from main_site.decorators import check_priveleged
from main_site.models import Announcement


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class AnnouncementCreateView(CreateView):
    model = Announcement
    fields = ['text', 'description']
    template_name = 'announcement/new_announcement.html'
    success_url = reverse_lazy('list-announcements')

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.created_by = self.request.user
        announcement.created_at = datetime.now()
        announcement.save()
        return super(AnnouncementCreateView, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class AnnouncementUpdateView(UpdateView):
    model = Announcement
    fields = ['text', 'description']
    template_name = 'announcement/update_announcement.html'
    success_url = reverse_lazy('list-announcements')


class AnnouncementDeleteView(DeleteView):
    model = Announcement
    template_name = 'announcement/delete_announcement.html'
    success_url = reverse_lazy('list-announcements')

# list drivers
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcement/list_announcement.html'
    context_object_name = 'announcements'

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'announcement/view_announcement.html'
    context_object_name = 'announcement'