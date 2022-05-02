import os
import sys
import random
import string
from product.models import Product
from client.models import Client
from order.models import Order, OrderItem
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        if User.objects.filter(username='BaseAdmin').exists():
            self.stdout.write('User BaseAdmin already exists')
            sys.exit(0)
        pswd = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
        admin = User.objects.create_superuser(username='BaseAdmin',
                                              email=os.getenv('ADMIN_EMAIL'),
                                              password=pswd)
        try:
            admins_group = Group.objects.get(name='Admins')
            admins_group.user_set.add(admin)
        except Group.DoesNotExist:
            self.stdout.write(f"Group Admins does not exist! Creating...")
            admins_group = Group.objects.create(name='Admins')
            for model in [Client, Product, Order, OrderItem]:
                for perm in ['add', 'change', 'delete', 'view']:
                    codename = perm + "_" + model._meta.model_name
                    permission = Permission.objects.get(codename=codename)
                    admins_group.permissions.add(permission)
                    self.stdout.write(f"Add permission {perm} _{model._meta.model_name} to Admins group")
            admins_group.user_set.add(admin)
        finally:
            self.stdout.write(f"Admin created "
                              f"username: BaseAdmin "
                              f"password: {pswd}")
