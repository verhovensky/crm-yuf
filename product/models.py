from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.urls import reverse
from django.conf import settings
from client.apps import slugify


class Category(MPTTModel):
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
        unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name='Родительская категория')
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:category_list",
                       args=[str(self.slug)])

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    class Meta:
        ordering = ("name",)
        verbose_name = "товар"
        verbose_name_plural = "товары"
        db_table = "product"

    category = TreeForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория')

    name = models.CharField(
        max_length=32,
        verbose_name="Название",
        unique=True)
    slug = models.SlugField(max_length=45)
    image = models.ImageField(
        upload_to="products/%Y/%m/%d",
        blank=True,
        verbose_name="Фото")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=1,
        validators=[MinValueValidator(Decimal("1.0"))],
        verbose_name="Цена")
    stock = models.DecimalField(
        max_digits=10,
        decimal_places=1,
        validators=[MinValueValidator(Decimal("1.0"))],
        verbose_name="Кол-во")
    available = models.BooleanField(
        default=True,
        verbose_name="На складе")
    created = models.DateTimeField(
        auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        default=1,
        verbose_name="Создавший")
    updated = models.DateTimeField(auto_now=True)

    def calc_total_product(self):
        if self.price and self.available:
            return Decimal(self.price) \
                   * Decimal(self.stock)
        else:
            return self.price

    calc_total_product.short_description = "Общая сумма"

    def __str__(self):
        return self.name

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product:single_product",
                       args=[self.slug, self.pk])
