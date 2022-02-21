from .models import Order


def check_out_of_stock(ql, pl, res=None, plindex=0):
    if res is None:
        res = {}
    for i in ql:
        if i <= pl[plindex].stock:
            res.update({pl[plindex].name: 'ok'})
            plindex += 1
        else:
            res.update({pl[plindex].name: 'out'})
            plindex += 1
    return res


def make_status_expired(order_id) -> bool:
    # If Order.other than processing (1)
    # do nothing
    # If Order.other processing (1)
    # mark expired
    o = Order.objects.get(pk=order_id)
    if o:
        o.status = 5
        o.save()
        return True
    return False
