from order.models import Order
import logging
from django.dispatch import Signal, receiver
from order.utils import sub_product_quantity_of_order, \
    add_product_quantity_of_order, add_closed_sales, sub_closed_sales

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

order_change_signal = Signal(
    ["from_status", "to_status",
     "order_sum", "user"])


@receiver(order_change_signal,
          sender=Order,
          dispatch_uid="order_change_status")
def order_change_status(sender, from_status: int,
                        to_status: int,
                        order: Order, user, **kwargs) -> None:
    """ Responsible for making closed_amount increase
    and decrease along with order status change

    :param from_status: Original order status which needs to be changed.
    :param to_status: Status which needs to be assigned to order.
    :param order: Order instance being changed.
    :param user: User which order is changing.
    :type user: User
    :returns: True if order status changed, False if remains the same
    """
    if from_status in (1, 2) and to_status not in (1, 2) or \
            from_status == 2 and to_status == 1:
        # add product back to inventory on statuses (3, 4, 5)
        for i in order.items.all().only("product_id", "quantity"):
            add_product_quantity_of_order(product=i.product_id,
                                          quantity=str(i.quantity))
        sub_closed_sales(user=user, amount=order.total_sum)
    if from_status in (1, 3, 4, 5) and to_status == 2:
        # sub product from inventory on PAYED (2) status
        for i in order.items.all().only("product_id", "quantity"):
            sub_product_quantity_of_order(product=i.product_id,
                                          quantity=str(i.quantity))
        add_closed_sales(user=user, amount=order.total_sum)
    order.status = to_status
    order.save()
    logging.info(f"Order {order.pk} status changed"
                 f" to {order.status} from {from_status}")
