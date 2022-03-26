from .models import Order
import decimal
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def check_out_of_stock(cart, res=None):
    if res is None:
        res = {'result': True}
    for x, y in enumerate(cart):
        if y['product'].stock < decimal.Decimal(y['quantity']):
            res.update({'result': False, 'errors': {}})
            less = y['product'].stock - decimal.Decimal(y['quantity'])
            res['errors'].update({y['product'].name: abs(less)})
        else:
            pass
    return res


def make_status_expired(order_id) -> bool:
    """ Makes order.status expired based on order status
    If order status is other than processing - do nothing
    Else - make order.status expired, and return products to inventory

    :param order_id """
    o = Order.objects.only('status').get(pk=order_id)
    if o.status == 1:
        o.status = 5
        o.save()
        logging.info(f"Order {order_id} expired")
        return True
    return False


def sub_product_quantity_of_order(product, quantity):
    if product:
        quantity = decimal.Decimal(quantity)
        product.stock -= quantity
        product.save()
    else:
        pass


def add_product_quantity_of_order(product, quantity):
    if product:
        quantity = decimal.Decimal(quantity)
        product.stock += quantity
        product.save()
    else:
        pass


def add_closed_sales(user, amount):
    user.closed_sales += 1
    user.sales_amount += amount


def sub_closed_sales(user, amount):
    user.closed_sales -= 1
    user.sales_amount -= amount


# def email_notify_creator(user_id)
