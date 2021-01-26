from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader

from .models import Client
from .forms import ClientAddForm
# import slugify function to transliterate slug
from .apps import slugify


# Clients Table
def index(request):
    title = 'Клиенты'
    header = 'Клиенты'
    template = loader.get_template('client/clients.html')
    сlientsall = Client.objects.order_by('name')
    context = {'сlientsall': сlientsall, 'page_title': title, 'header_page': header}
    return HttpResponse(template.render(context, request))

# Client Details
def clientdetail(request, id):
    title = 'Информация о клиенте'
    #header = client.name
    client = get_object_or_404(Client, id=id)
    template = loader.get_template('client/clientdetail.html')
    context = {'client': client, 'page_title': title}
    return HttpResponse(template.render(context, request))


# Add Client
def addclient(request):
    title = 'Добавить клиента'
    header = 'Добавить клиента'
    if request.method == "POST":
        form = ClientAddForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.slug = slugify(s=request.POST.get("name"))
            # Cannot assign "<SimpleLazyObject: <User: Bulat>>": "Client.created_by" must be a "UserProfile" instance.
            client.created_by = request.user
            client.save()
            return redirect('detail', id=client.id)
    else:
        form = ClientAddForm()
        template = loader.get_template('client/addclient.html')
        context = {'form': form, 'page_title': title, 'header_page': header}
        return HttpResponse(template.render(context, request))

# Edit Client
def editclient(request, id):
    title = 'Изменить клиента'
    header = 'Изменить клиента'
    client = get_object_or_404(Client, id=id)
    if request.method == "POST":
        form = ClientAddForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.slug = slugify(s=request.POST.get("name"))
            #post.author = request.user
            #post.published_date = timezone.now()
            client.save()
            return redirect('detail', id=client.id)
    else:
        form = ClientAddForm(instance=client)
    template = loader.get_template('client/addclient.html')
    context = {'form': form, 'page_title': title, 'header_page': header}
    return HttpResponse(template.render(context, request))

# DeleteClient
def deletecl(request, id):
    try:
        client = Client.objects.get(id=id)
        client.delete()
        return redirect('index')
    except Client.DoesNotExist:
        return HttpResponseNotFound("<h2>Клиент с таким ID не существует!</h2>")
