from django.db import models
from product.models import Product
from client.models import Client
from account.models import UserProfile
# Decimal
import decimal
from django.core.validators import MinValueValidator
from django.utils import timezone


class Order(models.Model):

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

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        db_table = "order"
        ordering = ['-created']

    full_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="ФИО заказчика")
    phone = models.CharField(max_length=22, null=True, blank=True)
    address = models.CharField(max_length=250, verbose_name="Адрес доставки")
    postal_code = models.CharField(max_length=20, null=True, blank=True, verbose_name="Почтовый индекс")
    # Client.client_orders.all()
    # Client associated with the Order, can be null and blank for comfort
    this_order_client = models.ForeignKey(Client, related_name='client_orders', null=True, blank=True,
                                          verbose_name="От клиента", on_delete=models.SET_NULL)
    # Account associated with this order, who created order
    this_order_account = models.ForeignKey(UserProfile, related_name='user_orders', null=True,
                                           verbose_name="Создавший", on_delete=models.SET_NULL)
    status = models.CharField(choices=STATUSORD, default=PENDING, max_length=16, blank=False,
                              verbose_name="Статус")
    # TODO: unique = True, error "unique":""
    delivery_time = models.DateTimeField(validators=[MinValueValidator(limit_value=timezone.now())],
                                         verbose_name="Время доставки",
                                         error_messages={"blank": "Выберите дату заказа",
                                                         "null": "Выберите реальную дату заказа",
                                                         "invalid_choice": "Нельзя создать заказ в прошлом!",
                                                         "invalid": "Нельзя создать заказ в прошлом!"})
    self_pick = models.BooleanField(null=False, default=False, verbose_name="Самовывоз")
    cash_on_delivery = models.BooleanField(null=False, default=False, verbose_name="Оплата при получении")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата оформления")
    updated = models.DateTimeField(auto_now=True, verbose_name="Статус изменен")
    description = models.TextField(blank=True, max_length=500, verbose_name="Примечание")

    def __str__(self):
        return 'Заказ {}'.format(self.pk)

    def get_total_cost(self):
        return sum([item.get_cost() for item in self.items.all()])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return '{}'.format(self.pk)

    def get_cost(self):
        return decimal.Decimal(self.price) * decimal.Decimal(self.quantity).\
            quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
