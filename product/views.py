from django.shortcuts import loader, get_object_or_404, HttpResponse, redirect
from django.http import HttpResponseNotFound
from .models import Category, Product
from .forms import ProductAddForm
from client.apps import slugify

# Product list
def product_list(request, category_slug=None):
    title = 'Товары'
    header = 'Список товаров'
    category = None
    categories = Category.objects.all()
    # display only available products
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    template = loader.get_template('product/products.html')
    context = {'category': category,
                   'categories': categories,
                   'products': products,
                   'page_title': title,
                   'header_page': header}
    return HttpResponse(template.render(context, request))


# Single Product page
def product_detail(request, id, slug):
    title = 'Товары'
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    header = product.name
    template = loader.get_template('product/productdetail.html')
    context = {'product': product,
                   'page_title': title,
                   'header_page': header}
    return HttpResponse(template.render(context, request))

# Delete Product
def deleteproduct(request, id):
    try:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect(to='/product')
    except TypeError as e:
        return HttpResponseNotFound("TypeError", e, product,
                                    "<h2>Товар с таким ID не существует!</h2>")

# Add Product
def addproduct(request):
    title = 'Добавить товар'
    header = 'Добавить товар'
    if request.method == "POST":
        form = ProductAddForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.slug = slugify(s=request.POST.get("name"))
            product.created_by = request.user
            product.save()
            return redirect(to='/product')
    else:
        form = ProductAddForm()
        template = loader.get_template('product/addproduct.html')
        context = {'form': form, 'page_title': title, 'header_page': header}
        return HttpResponse(template.render(context, request))

# Edit Product
def editproduct(request, id):
    title = 'Изменить товар'
    header = 'Изменить товар'
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        form = ProductAddForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.slug = slugify(s=request.POST.get("name"))
            product.save()
            return redirect(to='/product')
    else:
        form = ProductAddForm(instance=product)
    template = loader.get_template('product/addproduct.html')
    context = {'form': form, 'page_title': title, 'header_page': header}
    return HttpResponse(template.render(context, request))