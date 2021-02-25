from django.shortcuts import get_object_or_404, HttpResponse, redirect
from .models import Category, Product
from .forms import ProductAddForm
# CBV
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
# slugify func
from client.apps import slugify

class ProductListView(ListView):
    paginate_by = 3
    extra_context = {'page_title': 'Товары', 'page_header': 'Все товары'}
    template_name = 'product/products.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(available=True).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CategoryListView(ListView):
    paginate_by = 3
    extra_context = {'page_title': 'Товары', 'page_header': 'Все товары'}
    template_name = 'product/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        # https://docs.djangoproject.com/en/2.2/topics/db/queries/#lookups-that-span-relationships
        return Product.objects.filter(category__slug=self.kwargs['slug'], available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductCreateView(CreateView):
    template_name = 'product/addproduct.html'
    extra_context = {'page_title': 'Добавить товар', 'header_page': 'Добавить товар'}
    form_class = ProductAddForm
    success_url = 'query'


class ProductDeleteView(DeleteView):
    model = Product
    #success_url = reverse_lazy('product')
    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # no need for redirect, thanks to jQuery
        return HttpResponse(status=200)

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product/addproduct.html'
    fields = ('name', 'image', 'price', 'stock', 'available')
    success_url = 'query'
    # calc_total_product would be nice to make permanent field
    # displayed somewhere in corner


# queryset = Product.objects.filter(available=True).order_by('-created')

# Product list
# def product_list(request, category_slug=None):
#     title = 'Товары'
#     header = 'Список товаров'
#     category = None
#     categories = Category.objects.all()
#     # display only available products
#     products = Product.objects.filter(available=True)
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     template = loader.get_template('product/products.html')
#     context = {'category': category,
#                    'categories': categories,
#                    'products': products,
#                    'page_title': title,
#                    'header_page': header}
#     return HttpResponse(template.render(context, request))


# Single Product page
# def product_detail(request, id, slug):
#     title = 'Товары'
#     product = get_object_or_404(Product,
#                                 id=id,
#                                 slug=slug,
#                                 available=True)
#     header = product.name
#     template = loader.get_template('product/productdetail.html')
#     context = {'product': product,
#                    'page_title': title,
#                    'header_page': header}
#     return HttpResponse(template.render(context, request))
#
# # Delete Product
# def deleteproduct(request, id):
#     try:
#         product = Product.objects.get(id=id)
#         product.delete()
#         return redirect(to='/product')
#     except TypeError as e:
#         return HttpResponseNotFound("TypeError", e, product,
#                                     "<h2>Товар с таким ID не существует!</h2>")
#
# # Add Product
# def addproduct(request):
#     title = 'Добавить товар'
#     header = 'Добавить товар'
#     if request.method == "POST":
#         form = ProductAddForm(request.POST)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.slug = slugify(s=request.POST.get("name"))
#             product.created_by = request.user.userprofile
#             product.save()
#             return redirect(to='/product')
#     else:
#         form = ProductAddForm()
#         template = loader.get_template('product/addproduct.html')
#         context = {'form': form, 'page_title': title, 'header_page': header}
#         return HttpResponse(template.render(context, request))
#
# # Edit Product
# def editproduct(request, id):
#     title = 'Изменить товар'
#     header = 'Изменить товар'
#     product = get_object_or_404(Product, id=id)
#     if request.method == "POST":
#         form = ProductAddForm(request.POST, instance=product)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.slug = slugify(s=request.POST.get("name"))
#             product.save()
#             return redirect(to='/product')
#     else:
#         form = ProductAddForm(instance=product)
#     template = loader.get_template('product/addproduct.html')
#     context = {'form': form, 'page_title': title, 'header_page': header}
#     return HttpResponse(template.render(context, request))