from decimal import Decimal
import decimal
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from product.models import Product


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

    def save(self):
        # Session refresh cart
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add product to cart
        """
        if str(product.id) not in self.cart:
            self.cart[str(product.id)] = {'quantity': decimal.Decimal(quantity),
                                          'price': str(product.price)}
        if update_quantity:
            self.cart[str(product.id)]['quantity'] = decimal.Decimal(self.cart[str(product.id)]['quantity']) \
                                                     + decimal.Decimal(quantity)
        self.cart[str(product.id)]['quantity'] = json.dumps(self.cart[str(product.id)]['quantity'].
                                                            quantize(Decimal('.01'),
                                                            rounding=decimal.ROUND_DOWN),
                                                            cls=DjangoJSONEncoder).replace('"', '')
        self.save()

    def remove(self, product):
        """
        Remove products from cart
        """
        product.stock = product.stock + Decimal(self.cart[str(product.id)]['quantity'])
        product.save()
        del self.cart[str(product.id)]
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item_total_price = decimal.Decimal(item['price']) * \
                               decimal.Decimal(item['quantity'].replace('"', ''))
            item['total_price'] = json.dumps(item_total_price.quantize(Decimal('.01'),
                                             rounding=decimal.ROUND_DOWN),
                                             cls=DjangoJSONEncoder).replace('"', '')
            yield item

    def __len__(self):
        return self._data_len

    def get_total_price(self):
        at = []
        for i, x in enumerate(self.cart.values()):
            tp = decimal.Decimal(x['price']) * \
                               decimal.Decimal(x['quantity'])
            at.append(tp)
        return sum(at)

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
