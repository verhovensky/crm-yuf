from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.core.validators import RegexValidator, MinValueValidator
from decimal import Decimal


class UserProfile(models.Model):
    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"
        db_table = "account"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,16}$',
                                 message="Макс. длинна = 16 знаков. Прим: +700112299")
    phone_number = models.CharField(max_length=16, validators=[phone_regex],
                                    blank=True, verbose_name="Телефон")
    created = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Создан")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    photo = models.ImageField(upload_to='users/%Y/%m/%d', default='users/no-user-photo.jpg',
                              blank=True, verbose_name="Фото")
    # for closed sales and amount records
    closed_sales = models.PositiveIntegerField(default=0, verbose_name="Закрыто сделок")
    sales_amount = models.DecimalField(default=0.0, max_digits=20, decimal_places=1,
                                       validators=[MinValueValidator(Decimal('0.0'))],
                                       verbose_name='Продано на сумму')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = UserProfile(user=user)
            user_profile.save()

    post_save.connect(create_profile, sender=User)

    def __str__(self):
        # return 'Профиль пользователя {}'.format(self.user)
        return f'Профиль пользователя {self.user}'
