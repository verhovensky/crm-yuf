from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Client
from .forms import ClientAddForm
from .apps import slugify


class ClientTableView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      ListView):
    permission_required = 'client.view_client'
    login_url = '/account/login/'
    paginate_by = 10
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.all()


class ClientDetailView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       DetailView):
    permission_required = 'client.view_client'
    login_url = '/account/login/'
    model = Client
    context_object_name = 'client'

    def get_object(self, queryset=None):
        object = super(ClientDetailView, self).get_object()
        # more methods in template ?
        # object.last_accessed = timezone.now()
        return object


class ClientCreate(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   CreateView):
    model = Client
    login_url = '/account/login/'
    permission_required = 'client.add_client'
    form_class = ClientAddForm
    success_url = reverse_lazy('client:client_main')

    def form_valid(self, form):
        form.instance.created_by = self.request.user.userprofile
        form.instance.slug = slugify(form.instance.name)
        return super(ClientCreate, self).form_valid(form)

    def form_invalid(self, form):
        response = super(ClientCreate, self).form_invalid(form)
        return response

# TODO: on permission denied add message and redirect to the same page


class ClientUpdate(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   UpdateView):
    model = Client
    login_url = '/account/login/'
    context_object_name = 'client'
    permission_required = 'client.change_client'
    fields = ('name', 'type', 'phone_number', 'origin', 'email')
    success_url = reverse_lazy('client:client_main')


class ClientDelete(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   DeleteView):
    model = Client
    login_url = '/account/login/'
    permission_required = 'client.delete_client'
    context_object_name = 'client'

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # no need for redirect, thanks to jQuery
        return HttpResponse(status=200)
