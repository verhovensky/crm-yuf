from django.db import models
from product.models import Product
from client.models import Client
from account.models import UserProfile
# Decimal
import decimal
from django.core.validators import MinValueValidator
from django.utils import timezone

# Order Status choices
PENDING = 'Обработка'
DONE = 'Оплачено'
RET = 'Возврат'
BRAK = 'Брак'


STATUSORD = (
    (PENDING, 'Обработка'),
    (DONE, 'Оплачено'),
    (RET, 'Возврат'),
	(BRAK, 'Брак')
)


class Order(models.Model):
    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        db_table = "order"
        ordering = ['-created']

    # Client.client_orders.all()
    # Client associated with the Order, can be null and blank for comfort
    this_order_client = models.ForeignKey(Client, related_name='client_orders', null=True, blank=True, verbose_name="От клиента", on_delete=models.SET_NULL)
    # Account associated with this order, who created order
    this_order_account = models.ForeignKey(UserProfile, related_name='user_orders', null=True, verbose_name="Создавший", on_delete=models.SET_NULL)
    status = models.CharField(choices=STATUSORD, default=STATUSORD[0], max_length=16, blank=False, verbose_name="Статус")
    delivery_time = models.DateTimeField(validators=[MinValueValidator(limit_value=timezone.now())], verbose_name="Доставка на")
    self_pick = models.BooleanField(null=False, default=False, verbose_name="Самовывоз")
    cash_on_delivery = models.BooleanField(null=False, default=False, verbose_name="Оплата при получении")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата оформления")
    updated = models.DateTimeField(auto_now=True, verbose_name="Статус изменен")
    description = models.TextField(blank=True, max_length=500, verbose_name="Примечание")

    def __str__(self):
        return 'Заказ {}'.format(self.pk)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return '{}'.format(self.pk)

    def get_cost(self):
        summa = sum(decimal.Decimal(self.price) * decimal.Decimal(self.quantity))
        return summa.quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)