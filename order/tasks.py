from __future__ import absolute_import, unicode_literals
from .utils import make_status_expired

from crmdev.my_celery import app


@app.task(queue='order')
def mynumsadd(**kwargs):
    print('TASK EXECUTE mynumsadd')
    res = kwargs['x'] + kwargs['y']
    return {'result':res}


@app.task(queue='order')
def expire_order(**kwargs):
    """ Returning make_status_expired function with order_id provided in kwargs
    All checks performed in make_status_expired function
    All other ORM related functions in utils.py of this app
    :param order_id """

    id = kwargs['order_id']
    result = make_status_expired(order_id=id)
    return result
