#create feedback
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView
from main_site.decorators import check_priveleged, is_not_priveleged
from main_site.models import Feedback


@method_decorator(login_required(login_url='login'), name='dispatch')
class FeedbackCreateView(CreateView):
    model = Feedback
    template_name = 'feedback/new.html'
    fields = ['text']

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.user=self.request.user
        return super(FeedbackCreateView, self).form_valid(form)
    def get_success_url(self):
        if is_not_priveleged(self.request.user):
            return reverse_lazy('user-home')
        return reverse_lazy('list-feedbacks')
        

#feedback details
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class FeedbackDetailView(DetailView):
    model = Feedback
    template_name = 'feedback/view.html'
    context_object_name = 'feedback'

#list Feedbacks
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(check_priveleged, name='dispatch')
class FeedbackListView(ListView):
    model = Feedback
    template_name = 'feedback/list.html'
    context_object_name = 'feedbacks'