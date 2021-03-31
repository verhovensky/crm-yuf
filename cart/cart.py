from decimal import Decimal
import decimal
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
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # modified, чтобы убедиться, что он сохранен
        self.session.modified = True

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add product to cart
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            # implement correct quantity addition
            in_cart_quantity = self.cart[product_id]['quantity']
            self.cart[product_id]['quantity'] = Decimal(in_cart_quantity) + Decimal(quantity)
            # TODO : implement in Order model: self.cart[product_id]['quantity'] - Product.stock
            # ordered = self.cart[product_id]['quantity']
            # actual_product = Product.objects.get(pk=int(product_id))
            # actual_product.stock = actual_product.stock - ordered
            # for serialization through JSON
            to_be_serialized = self.cart[product_id]['quantity']
            self.cart[product_id]['quantity'] = to_be_serialized.quantize(Decimal('.01'), rounding=decimal.ROUND_DOWN)
        self.save()

    def remove(self, product):
        """
        Remove products from cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item_total_price = item['total_price'] = Decimal(item['price']) * Decimal(item['quantity'])
            item['total_price'] = item_total_price.quantize(Decimal('.01'), rounding=decimal.ROUND_DOWN)
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
        summa = sum(Decimal(item['price']) * Decimal(item['quantity']) for item in
                   self.cart.values())
        return summa.quantize(Decimal('.01'), rounding=decimal.ROUND_DOWN)

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

