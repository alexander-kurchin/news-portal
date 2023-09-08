from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.views.generic import TemplateView


class BecomeAnAuthorView(LoginRequiredMixin, TemplateView):
    template_name = 'news/become-an-author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        authors_group = Group.objects.get(name='authors')
        authors_group.user_set.add(user)
        return redirect('become-an-author')
