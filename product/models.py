from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    class Meta:
        ordering = ('name',)
        verbose_name = "товар"
        verbose_name_plural = "товары"
        db_table = "product"

    category = models.ForeignKey(Category, related_name='products')
    name = models.CharField(max_length=20, verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=1, validators=[MinValueValidator(Decimal('1.0'))], verbose_name='Цена')
    quantity = models.DecimalField(max_digits=10, decimal_places=1, validators=[MinValueValidator(Decimal('1.0'))], verbose_name='Кол-во')
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def calc_total_product(self):
        # if product available - calc total in decimal format
        if self.price and self.available==True:
            return Decimal(self.price) * Decimal(self.quantity)
        else:
            return self.price

    calc_total_product.short_description = 'Общая сумма'

    def __str__(self):
        return self.name