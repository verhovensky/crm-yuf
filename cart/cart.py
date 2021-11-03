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
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        # Session refresh cart
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add product to cart
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
            # reduce from stock
            product.stock = product.stock - quantity
            product.save()
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
            product.stock = product.stock - quantity
            product.save()
        else:
            # implement correct quantity addition
            in_cart_quantity = self.cart[product_id]['quantity']
            self.cart[product_id]['quantity'] = decimal.Decimal(in_cart_quantity) + decimal.Decimal(quantity)
            to_be_serialized = self.cart[product_id]['quantity']
            ready_dec_q = to_be_serialized.quantize(Decimal('.01'), rounding=decimal.ROUND_DOWN)
            self.cart[product_id]['quantity'] = json.dumps(ready_dec_q, cls=DjangoJSONEncoder).replace('"', '')
        self.save()

    def remove(self, product):
        """
        Remove products from cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            # add quantity back to stock
            product.stock = product.stock + Decimal(self.cart[product_id]['quantity'])
            product.save()
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = decimal.Decimal(item['price'])
            correct_str = item['quantity'].replace('"', '')
            rd_q = decimal.Decimal(correct_str)
            item_total_price = item['price'] * rd_q
            ready_dec = item_total_price.quantize(Decimal('.01'), rounding=decimal.ROUND_DOWN)
            item['total_price'] = json.dumps(ready_dec, cls=DjangoJSONEncoder).replace('"', '')
            yield item

    def __len__(self):
        """
        Total product TYPES in cart.
        One product type = total + 1
        """
        total = 0
        for item in self.cart.items():
            total += 1
        return total

    def get_total_price(self):
        all_totals = []
        for item in self.cart.values():
            ready_from_str = decimal.Decimal(item['total_price'])
            all_totals.append(ready_from_str)
        total_totals = sum(all_totals)
        return total_totals

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True