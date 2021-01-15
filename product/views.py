from django.shortcuts import loader, get_object_or_404, HttpResponse
from .models import Category, Product

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