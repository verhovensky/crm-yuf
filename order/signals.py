from .models import Order
import logging
from .tasks import expire_order
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from order.utils import sub_product_quantity_of_order, add_product_quantity_of_order, \
    add_closed_sales, sub_closed_sales

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

order_change_signal = Signal(providing_args=['from_status', 'to_status',
                                             'order_sum', 'user'])


@receiver(order_change_signal, sender=Order, dispatch_uid='order_change_status')
def order_change_status(sender, from_status, to_status, order, user, **kwargs):
    """ Responsible for making closed_amount increase
    and decrease along with order status change

    :param from_status: Original order status which needs to be changed.
    :type from_status: int
    :param to_status: Status which needs to be assigned to order.
    :type to_status: int
    :param order: Order instance being changed.
    :type order: Order
    :param user: User which order is changing.
    :type user: User
    :returns: True if order status changed, False if remains the same
    :rtype: Bool
    """
    try:
        if from_status == 1 and to_status == 2:
            order.status = to_status
            add_closed_sales(user=user, amount=order.total_sum)
        if from_status in (1, 2) and to_status not in (1, 2):
            # add product to inventory
            order.status = to_status
            for i in order.items.all().only('product_id', 'quantity'):
                add_product_quantity_of_order(product=i.product_id,
                                              quantity=str(i.quantity))
            sub_closed_sales(user=user, amount=order.total_sum)
        if from_status in (3, 4, 5) and to_status not in (1, 2):
            order.status = to_status
        if from_status in (3, 4, 5) and to_status == 2:
            order.status = to_status
            for i in order.items.all().only('product_id', 'quantity'):
                sub_product_quantity_of_order(product=i.product_id,
                                              quantity=str(i.quantity))
            add_closed_sales(user=user, amount=order.total_sum)
            # decrease product from inventory
    except Exception as e:
        logging.info(f'Exception at order.pk={order.pk}, '
                     f'user={user}', e)
    finally:
        user.save()
        order.save()
        logging.info(f"Order {order.pk} status changed"
                     f" to {order.status} from {from_status}")


@receiver(post_save, sender=Order, dispatch_uid="add_celery_task")
def add_task(sender, instance, created, **kwargs):
    """ Add task for order to expire
    If order status not processing (1), do nothing"""
    if created:
        logging.info(f'Creating task expiring for {instance.pk}')
        expire_order.apply_async(kwargs={'order_id': instance.pk},
                                 eta=instance.delivery_time,
                                 queue='order',
                                 serializer='json')
    else:
        pass
