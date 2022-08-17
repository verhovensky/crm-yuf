from django.urls import reverse_lazy
from account.models import UserProfile
from product.models import Product
from client.models import Client
from django.db import models


class Order(models.Model):
    PROCESSING = 1
    PAYED = 2
    RETURNED = 3
    BAD = 4
    EXPIRED = 5

    STATUS = (
        (PROCESSING, 'Обработка'),
        (PAYED, 'Оплачено'),
        (RETURNED, 'Возврат'),
        (BAD, 'Брак'),
        (EXPIRED, 'Просрочено'))

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        db_table = "order"
        ordering = ['-created']

    full_name = models.CharField(max_length=32,
                                 verbose_name="ФИО заказчика",
                                 blank=True,
                                 default='',
                                 unique_for_date='delivery_time')
    phone = models.CharField(max_length=22)
    address = models.CharField(max_length=250,
                               verbose_name="Адрес доставки")
    this_order_client = models.ForeignKey(Client,
                                          related_name='customer',
                                          blank=True,
                                          verbose_name="От клиента",
                                          default='',
                                          on_delete=models.SET_DEFAULT)
    this_order_account = models.ForeignKey(UserProfile,
                                           related_name='employee',
                                           blank=True,
                                           verbose_name="Создавший",
                                           default='',
                                           on_delete=models.SET_DEFAULT)
    status = models.PositiveSmallIntegerField(choices=STATUS,
                                              default=PROCESSING,
                                              verbose_name='Статус')
    delivery_time = models.DateTimeField(verbose_name="Время доставки")
    self_pick = models.BooleanField(default=False,
                                    verbose_name="Самовывоз")
    cash_on_delivery = models.BooleanField(default=False,
                                           verbose_name="Оплата при получении")
    total_sum = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    default=0.0,
                                    verbose_name='Сумма заказа')
    updated_by = models.ForeignKey(UserProfile,
                                   related_name='user_changed_orders',
                                   blank=True,
                                   default='',
                                   verbose_name="Изменивший статус",
                                   on_delete=models.SET_DEFAULT)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name="Дата оформления")
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name="Статус изменен")
    description = models.TextField(blank=True,
                                   max_length=1200,
                                   verbose_name="Примечание")

    def __str__(self):
        return 'Заказ {}'.format(self.pk)

    def get_absolute_url(self):
        return reverse_lazy('order:detail', kwargs={'pk': self.pk})


class OrderItem(models.Model):
    """ Field product is needed to store product name, in case product gets deleted  """
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                default=0.0)
    name = models.CharField(max_length=200)
    product_id = models.ForeignKey(Product,
                                   related_name='product',
                                   blank=True,
                                   default='',
                                   on_delete=models.SET_DEFAULT)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                default=0.0)
    quantity = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   default=0.0)

    def __str__(self):
        return '{}'.format(self.pk)
