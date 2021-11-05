from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# CBV
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Client
from .forms import ClientAddForm
# import slugify function to transliterate slug
from .apps import slugify


class ClientTableView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'client.view_client'
    template_name = "client/clients.html"
    paginate_by = 10
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.all()


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'client.view_client'
    template_name = "client/clientdetail.html"
    model = Client
    context_object_name = 'client'

    def get_object(self, queryset=None):
        object = super(ClientDetailView, self).get_object()
        # more methods in template ?
        # object.last_accessed = timezone.now()
        return object


class ClientCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'client.add_client'
    template_name = "client/addclient.html"
    form_class = ClientAddForm
    success_url = '/client'

    def form_valid(self, form):
        form.instance.created_by = self.request.user.userprofile
        form.instance.slug = slugify(form.instance.name)
        return super(ClientCreate, self).form_valid(form)

    def form_invalid(self, form):
        response = super(ClientCreate, self).form_invalid(form)
        return response


class ClientUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    context_object_name = 'client'
    permission_required = 'client.change_client'
    template_name = "client/addclient.html"
    fields = ('name', 'type', 'phone_number', 'origin', 'email')
    success_url = '/client'


class ClientDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = 'client.delete_client'
    context_object_name = 'client'
    # success_url = reverse_lazy('client')

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # no need for redirect, thanks to jQuery
        return HttpResponse(status=200)
