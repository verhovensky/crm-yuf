from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from product.models import Product
from client.models import Client
from order.models import Order, OrderItem

GROUPS_PERMISSIONS = {
    'Sellers': {
        Product: ['add', 'view'],
        Client: ['add', 'view'],
        Order: ['add', 'change', 'view'],
        OrderItem: ['add', 'change', 'delete', 'view'],
    },

    'Managers': {
        Product: ['add', 'change', 'view'],
        Client: ['add', 'change', 'view'],
        Order: ['add', 'change', 'delete', 'view'],
        OrderItem: ['add', 'change', 'delete', 'view'],
    },

    'Admins': {
        Product: ['add', 'change', 'delete', 'view'],
        Client: ['add', 'change', 'delete', 'view'],
        Order: ['add', 'change', 'delete', 'view'],
        OrderItem: ['add', 'change', 'delete', 'view'],
    },
}


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = 'Creates default groups:' \
           'Admins' \
           'Sellers' \
           'Mangers'

    def handle(self, *args, **options):
        for group_name in GROUPS_PERMISSIONS:
            group, created = Group.objects.get_or_create(name=group_name)
            for model_cls in GROUPS_PERMISSIONS[group_name]:
                for perm_index, perm_name in \
                        enumerate(GROUPS_PERMISSIONS[group_name][model_cls]):
                    codename = perm_name + "_" + model_cls._meta.model_name
                    try:
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        print(f"Adding {codename} to group {group.__str__()}")
                    except Permission.DoesNotExist:
                        print(f"{codename} not found")
