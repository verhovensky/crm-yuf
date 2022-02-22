from account.models import UserProfile
from .models import Order
#from .tasks import expire_order
from datetime import timedelta
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save


order_change_signal = Signal(providing_args=['from_status', 'to_status',
                                             'order_sum', 'user'])


@receiver(order_change_signal, sender=Order, dispatch_uid='order_change_status')
def order_change_status(sender, **kwargs):
    """ Change order status along with
    userprofile.closed_sales
    userprofile.sales_amount
    Attributes decrease/increase based on current Order.status
    and changed Order.status
    """
    fr = kwargs['kwargs']["from_status"]
    to = kwargs['kwargs']["to_status"]
    # if to_status = 2 (payed):
    # add userprofile.closed_sales
    # add userprofile.sales_amount
    # if from_status = 2 (payed)
    # decrease userprofile.closed_sales
    # decrease userprofile.sales_amount
    print(kwargs)
    print(sender)
    print(f'Order status ORIGINAL = {fr} CHANGED = {to}')


@receiver(post_save, sender=Order, dispatch_uid="add_celery_task")
def add_task(sender, instance, created, **kwargs):
    """ Add task for order to expire
    If order status changed, do nothing"""
    if created:
        print('Created')
        #expire_order.apply_async(kwargs={'order_id': instance.pk},
        #                         eta=instance.delivery_time + timedelta(minutes=75),
        #                         queue='order',
        #                         serializer='json')
    else:
        pass

