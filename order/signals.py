from account.models import UserProfile
from .models import Order
from django.dispatch import Signal, receiver


order_change_signal = Signal(providing_args=['from_status', 'to_status',
                                             'order_sum', 'user'])


@receiver(order_change_signal, sender=Order, dispatch_uid='order_change_status')
def order_change_status(sender, **kwargs):
    print(kwargs)
    print(sender)
    fs = kwargs["from_status"]
    to = kwargs["to_status"]
    print(f'Order status ORIGINAL = {fs} CHANGED = {to}')

