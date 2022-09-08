from django.db.models import Q
from django.shortcuts import HttpResponse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.urls import reverse
from .models import Category, Product
from .forms import ProductAddForm, CategoryAddForm
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView
from cart.forms import CartAddProductForm


class CategoryListView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       ListView):
    paginate_by = 10
    permission_required = "category.view_category"
    permission_denied_message = "not authorized"
    cart_product_form = CartAddProductForm()
    extra_context = {"page_title": "Товары",
                     "page_header": "Все товары",
                     "cart_product_form": cart_product_form}
    context_object_name = "products"

    def get_queryset(self):
        # return either products in category or all products of
        # super category
        category = get_object_or_404(Category,
                                     slug=self.kwargs["slug"])
        return Product.objects.filter(
            Q(category__slug=self.kwargs["slug"],
              available=True) |
            Q(category__in=
              category.get_descendants(include_self=True))) \
            .order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class CategoryCreateView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):

    form_class = CategoryAddForm
    permission_required = "product.view_product"
    permission_denied_message = "not authorized"
    template_name = "product/category_form.html"
    extra_context = {"page_title": "Добавить категорию",
                     "header_page": "Добавить категорию",
                     "categories": Category.objects.all()}


class CategoryUpdateView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         UpdateView):
    form_class = CategoryAddForm
    permission_required = "product.view_product"
    permission_denied_message = "not authorized"
    template_name = "product/category_form.html"
    extra_context = {"page_title": "Изменить категорию",
                     "header_page": "Изменить категорию",
                     "categories": Category.objects.all()}


class ProductListView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      ListView):
    permission_required = "product.view_product"
    permission_denied_message = "not authorized"
    paginate_by = 10
    cart_product_form = CartAddProductForm()
    extra_context = {"page_title": "Товары",
                     "page_header": "Все товары",
                     "cart_product_form": cart_product_form}
    context_object_name = "products"
    queryset = Product.objects.filter(
        available=True).order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


# Single Product page
class SingleProductView(LoginRequiredMixin, DetailView):
    model = Product
    permission_required = "category.view_category"
    permission_denied_message = "not authorized"
    cart_product_form = CartAddProductForm()
    extra_context = {"page_title": "Товар",
                     "categories": Category.objects.all(),
                     "cart_product_form": cart_product_form}
    context_object_name = "product"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Product, pk=self.kwargs.get("pk"))


class ProductCreateView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        CreateView):

    permission_required = "product.add_product"
    permission_denied_message = "not authorized"
    template_name = "product/product_form.html"
    extra_context = {"page_title": "Добавить товар",
                     "header_page": "Добавить товар",
                     "categories": Category.objects.all()}
    form_class = ProductAddForm

    def get_success_url(self):
        return reverse("product:single_product",
                       kwargs={
                           "slug": self.object.slug,
                           "pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        DeleteView):
    model = Product
    permission_required = "product.delete_product"
    permission_denied_message = "not authorized"

    def post(self, *args, **kwargs):
        obj = get_object_or_404(
            Product, pk=self.kwargs.get("pk"))
        obj.delete()
        # no need for redirect, thanks to jQuery
        return HttpResponse(status=200)


class ProductUpdateView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        UpdateView):
    model = Product
    permission_required = "product.change_product"
    permission_denied_message = "not authorized"
    form_class = ProductAddForm
    extra_context = {"page_title": "Изменить товар",
                     "header_page": "Изменить товар",
                     "categories": Category.objects.all()}
    success_url = "product:product_list"
