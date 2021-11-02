from django.http import HttpResponse
# decorators
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
# CBV
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.views.generic.detail import SingleObjectMixin
# from django.urls import reverse_lazy, reverse
# Client model import
from .models import Client
from .forms import ClientAddForm
# import slugify function to transliterate slug
from .apps import slugify

# if many decorators
# decorators = [permission_required, login_required]


@method_decorator(login_required, name='dispatch')
class ClientTableView(ListView):
    template_name = "client/clients.html"
    # name for client list in HTML template
    context_object_name = 'client_list'

    def get_queryset(self):
        return Client.objects.filter(created_by=
                                     self.request.user.userprofile)


@method_decorator(login_required, name='dispatch')
class ClientDetailView(DetailView):
    template_name = "client/clientdetail.html"
    model = Client
    context_object_name = 'unit'

    def get_object(self, queryset=None):
        object = super(ClientDetailView, self).get_object()
        # more methods in template ?
        # object.last_accessed = timezone.now()
        return object


@method_decorator(login_required, name='dispatch')
class ClientCreate(CreateView):
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


@method_decorator(login_required, name='dispatch')
class ClientUpdate(UpdateView):
    model = Client
    template_name = "client/addclient.html"
    fields = ('name', 'type', 'phone_number', 'origin', 'email')
    success_url = '/client'


@method_decorator(login_required, name='dispatch')
class ClientDelete(DeleteView):
    model = Client
    context_object_name = 'unit'
    # success_url = reverse_lazy('client')

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # no need for redirect, thanks to jQuery
        return HttpResponse(status=200)
