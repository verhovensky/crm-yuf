from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
#from django.dispatch import receiver
from django.core.validators import RegexValidator, MinValueValidator
from decimal import Decimal


S = 'Продавец'
M = 'Менеджер'
G = 'Гость'

ROLE_CHOICES = (
    (S, 'Продавец'),
    (M, 'Менеджер'),
    (G, 'Гость')
    )


class UserProfile(models.Model):
    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"
        db_table = "profile"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,16}$',
                                 message="Номер телефона должен быть в формате: '+700112299'. Макс. длинна = 16 знаков")
    phone_number = models.CharField(max_length=16, validators=[phone_regex], blank=True, verbose_name="Телефон")
    created = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Создан")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    role = models.CharField(choices=ROLE_CHOICES, default=S, max_length=12, blank=True, verbose_name="Роль")
    photo = models.ImageField(upload_to='users/%Y/%m/%d', default='users/no-user-photo.jpg', blank=True, verbose_name="Фото")
    # for closed sales and amount records
    closed_sales = models.PositiveIntegerField(default=0, verbose_name="Закрыто сделок")
    sales_amount = models.DecimalField(default=0.0, max_digits=20, decimal_places=1, validators=[MinValueValidator(Decimal('1.0'))], verbose_name='Продано на сумму')


    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = UserProfile(user=user)
            user_profile.save()

    post_save.connect(create_profile, sender=User)


    def __str__(self):
        # return 'Профиль пользователя {}'.format(self.user)
        return '{} {}'.format(self.get_role_display(), self.user)

    def display_role_template(self):
        return self.role