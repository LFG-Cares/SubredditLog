from constance import config
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView

from entries.forms import EntryForm
from entries.models import Entry, Rule


class LogView(UserPassesTestMixin, ListView):
    template_name = 'entries/log.html'
    model = Entry
    context_object_name = 'entries'
    queryset = Entry.objects.all()
    paginate_by = 25

    def test_func(self):
        if config.PUBLIC_MODLOG:
            return True
        elif self.request.user.is_authenticated:
            return True
        return False


class RulesView(ListView):
    template_name = 'entries/rules.html'
    model = Rule
    context_object_name = 'rules'
    queryset = Rule.objects.all()


class Search(ListView):
    template_name = 'entries/search.html'
    model = Entry
    context_object_name = 'entries'
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            return Entry.objects.none()
        return Entry.objects.filter(
            Q(user__icontains=query) | Q(notes__icontains=query)
        )


class AddEntryView(LoginRequiredMixin, CreateView):
    template_name = 'entries/add_entry.html'
    model = Entry
    form_class = EntryForm

    def form_valid(self, form):
        form.instance.moderator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('log-view')


@login_required
@require_http_methods(['POST'])
def ban_check(request):
    user = request.POST['user']
    if len(user) == 0:
        count = 0
    else:
        count = Entry.objects.filter(user__iexact=user).count()
    return render(request, 'entries/_found.html', {'user': user, 'count': count})
