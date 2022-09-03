from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator
from decimal import Decimal

# TODO: single phone regex in all models
phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,16}$",
    message="Макс. длинна = 16 знаков. "
            "Прим: +700112299")


class User(AbstractUser):
    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    phone_number = models.CharField(
        max_length=16,
        validators=[phone_regex],
        blank=True,
        verbose_name="Телефон")
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения")
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d",
        default="users/no-user-photo.jpg",
        blank=True, verbose_name="Фото")
    # for closed sales and amount records
    closed_sales = models.IntegerField(
        default=0,
        verbose_name="Закрыто сделок")
    sales_amount = models.DecimalField(
        default=0.0,
        max_digits=20,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal("0.0"))],
        verbose_name="Продано на сумму")
    created = models.DateTimeField(
        auto_now_add=True, blank=True,
        verbose_name="Создан")
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлен")

    def __str__(self):
        return self.username
