import decimal
from django.conf import settings
from product.models import Product

# TODO: substract product quantity method
# TODO: update product quantity method
# TODO: product serialized class, incapsulate it into cart


class Cart(object):

    def __init__(self, request):
        """
        Cart init
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self._data_len = len(self.cart.items())

    def __iter__(self):
        for item in self.cart.values():
            item["total_price"] = \
                decimal.Decimal(item["price"]) \
                * decimal.Decimal(item["quantity"])
            item["total_price"] = str(item["total_price"])
            yield item

    def __len__(self):
        return self._data_len

    def id_to_product(self):
        """ Convert ids of products to product instances
        However, this may be redundant in DRF
        with serializers (ex. queryset param) """
        product_ids = self.cart.keys()
        products = Product.objects.\
            filter(id__in=product_ids).\
            only("pk", "name", "price", "stock")
        for product in products:
            self.cart[str(product.id)]["product"] = product

    def product_to_id(self):
        """ Convert products instances to ids
        However, this may be redundant in DRF
        with serializers (ex. queryset param) """
        product_instances = self.cart.keys()
        for product in product_instances:
            self.cart[product]["product"] = str(product)

    def get_total_price(self):
        """ Sum up prices of all products in cart """
        at = []
        for i, x in enumerate(self.cart.values()):
            tp = decimal.Decimal(x["price"]) * \
                               decimal.Decimal(x["quantity"])
            at.append(tp)
        return str(sum(at))

    def save(self):
        """ Save modified cart content in session """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product, quantity, update_quantity=False):
        """ Add product to cart """
        if str(product.id) not in self.cart:
            self.cart[str(product.id)] = {
                "id": str(product.id),
                "quantity": str(quantity),
                "price": str(product.price),
                "name": str(product.name),
                "img": str(product.image)}
        if update_quantity:
            upd = decimal.Decimal(
                self.cart[str(product.id)]["quantity"]) \
                  + decimal.Decimal(quantity)
            self.cart[str(product.id)]["quantity"] = str(upd)
        self.save()

    def remove(self, product):
        """ Remove product from cart """
        del self.cart[str(product.id)]
        self.save()

    def clear(self):
        """ Remove cart instance from session """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
