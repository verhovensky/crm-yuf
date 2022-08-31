from django.db.models import F
from .models import Order, OrderItem
import decimal
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def check_out_of_stock(cart, res=None) -> dict:
    if res is None and len(cart) > 0:
        res = {"result": True}
    else:
        return {"result": False, "errors": {"cart": "empty"}}
    for x, y in enumerate(cart):
        if y["product"].stock < decimal.Decimal(y["quantity"]):
            res.update({"result": False, "errors": {}})
            less = y["product"].stock - \
                   decimal.Decimal(y["quantity"])
            res["errors"].update({y["product"].name: abs(less)})
    return res


def make_status_expired(order_id) -> bool:
    """ Makes order.status expired based on order status
    If order status is other than processing - do nothing
    Else - make order.status expired, return products to inventory

    :param order_id """
    o = Order.objects.only("status").get(pk=order_id)
    if o.status == 1:
        o.status = 5
        o.save()
        logging.info(f"Order {order_id} expired")
        return True
    return False


def sub_product_quantity_of_order(product, quantity):
    if product:
        quantity = decimal.Decimal(quantity)
        product.stock = F("stock") - quantity
        product.save()


def add_product_quantity_of_order(product, quantity):
    if product:
        quantity = decimal.Decimal(quantity)
        product.stock = F("stock") + quantity
        product.save()


def add_closed_sales(user, amount):
    user.closed_sales = F("closed_sales") + 1
    user.sales_amount = F("sales_amount") + amount
    user.save()


def sub_closed_sales(user, amount):
    user.closed_sales = F("closed_sales") - 1
    user.sales_amount = F("sales_amount") - amount
    user.save()


def create_order_item(order: Order, item: dict) -> None:
    OrderItem.objects.create(
        order=order,
        name=item[1]["product"].name,
        price=decimal.Decimal(item[1]["price"]),
        quantity=decimal.Decimal(item[1]["quantity"]),
        product_id=item[1]["product"],
        total=item[1]["total_price"])

# def email_notify_creator(user_id)
