from django.db import models
from django.core.validators import RegexValidator
from account.models import UserProfile

TG = 1
WA = 2
FB = 3
INST = 4
SOC = 5
FRI = 6
MAIL = 7
NEYK = 8

ORIGINS = (
    (TG, "Telegram"),
    (WA, "WhatsApp"),
    (FB, "Facebook"),
    (INST, "Instagram"),
    (SOC, "Соцсети"),
    (FRI, "Сарафанное радио"),
    (MAIL, "E-mail рассылка"),
    (NEYK, "Отсутствует")
)


IND = 1
UR = 2
COM = 3
OAO = 4
OSO = 5
OOO = 6
INDP = 7
ZAO = 8
NKO = 9
NPO = 10
FOND = 11
BANK = 12
NEYK = 13

CLIENTTYPE = (
    (IND, "Физ лицо"),
    (UR, "Юр лицо"),
    (COM, "Компания"),
    (OAO, "ОАО"),
    (OSO, "ОсОО"),
    (OOO, "ООО"),
    (INDP, "ИП"),
    (ZAO, "ЗАО"),
    (NKO, "НКО"),
    (NPO, "НПО"),
    (FOND, "Фонд"),
    (BANK, "Банк"),
    (NEYK, "Отсутствует")
)


class Client(models.Model):

    class Meta:
        ordering = ["name"]
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        db_table = "client"

    name = models.CharField(
        max_length=32,
        verbose_name="ФИО")
    slug = models.SlugField(max_length=200, default="")
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,16}$",
        message="Телефон должен быть в формате: "
                "'+7867865432'. Макс. длинна = 16 знаков")
    phone_number = models.CharField(
        max_length=16,
        validators=[phone_regex],
        blank=True, unique=True,
        verbose_name="Телефон")
    type = models.IntegerField(
        choices=CLIENTTYPE,
        default=CLIENTTYPE[12][0],
        blank=True,
        verbose_name="Тип")
    origin = models.IntegerField(
        choices=ORIGINS,
        default=ORIGINS[7][0],
        blank=True,
        verbose_name="Источник")
    email = models.EmailField(
        blank=True,
        verbose_name="Email")
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан")
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        blank=True,
        default=1,
        verbose_name="Создавший")
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлен")

    def __str__(self):
        return f"{self.name}, {self.phone_number}"
