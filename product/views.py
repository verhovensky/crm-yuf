from django.shortcuts import HttpResponse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Category, Product
from .forms import ProductAddForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from cart.forms import CartAddProductForm


class ProductListView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      ListView):
    permission_required = 'product.view_product'
    permission_denied_message = 'not authorized'
    paginate_by = 10
    cart_product_form = CartAddProductForm()
    extra_context = {'page_title': 'Товары',
                     'page_header': 'Все товары',
                     'cart_product_form': cart_product_form}
    context_object_name = 'products'
    queryset = Product.objects.filter(available=True).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryListView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       ListView):
    paginate_by = 10
    permission_required = 'category.view_category'
    permission_denied_message = 'not authorized'
    cart_product_form = CartAddProductForm()
    extra_context = {'page_title': 'Товары',
                     'page_header': 'Все товары',
                     'cart_product_form': cart_product_form}
    context_object_name = 'products'

    def get_queryset(self):
        # https://docs.djangoproject.com/en/2.2/topics/db/queries/#lookups-that-span-relationships
        return Product.objects.filter(category__slug=self.kwargs['slug'],
                                      available=True).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# Single Product page
class SingleProductView(LoginRequiredMixin, DetailView):
    model = Product
    permission_required = 'category.view_category'
    permission_denied_message = 'not authorized'
    cart_product_form = CartAddProductForm()
    extra_context = {'page_title': 'Товар',
                     'categories': Category.objects.all(),
                     'cart_product_form': cart_product_form}
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, pk=self.kwargs.get('pk'))


class ProductCreateView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        CreateView):

    permission_required = 'product.add_product'
    permission_denied_message = 'not authorized'
    template_name = 'product/product_form.html'
    extra_context = {'page_title': 'Добавить товар',
                     'header_page': 'Добавить товар',
                     'categories': Category.objects.all()}
    form_class = ProductAddForm
    success_url = 'product:single_product'


class ProductDeleteView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        DeleteView):
    model = Product
    permission_required = 'product.delete_product'
    permission_denied_message = 'not authorized'
    # success_url = reverse_lazy('product:product_list')

    def post(self, *args, **kwargs):
        object = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        object.delete()
        # no need for redirect, thanks to jQuery
        return HttpResponse(status=200)


class ProductUpdateView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        UpdateView):
    model = Product
    permission_required = 'product.change_product'
    permission_denied_message = 'not authorized'
    form_class = ProductAddForm
    extra_context = {'page_title': 'Изменить товар',
                     'header_page': 'Изменить товар',
                     'categories': Category.objects.all()}
    success_url = 'product:product_list'
