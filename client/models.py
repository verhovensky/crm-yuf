from django.db import models
from django.core.validators import RegexValidator
from account.models import UserProfile

# Клиенты
# откуда клиент пришел, choices

TG = 'Telegram'
WA = 'WhatsApp'
FB = 'Facebook'
INST = 'Instagram'
SOC = 'Соцсети'
FRI = 'Сарафанное радио'
MAIL = 'E-mail рассылка'
NEYK = 'Отсутствует'

ORIGINS = (
    (TG, 'Telegram'),
    (WA, 'WhatsApp'),
    (FB, 'Facebook'),
    (INST, 'Instagram'),
    (SOC, 'Соцсети'),
    (FRI, 'Сарафанное радио'),
    (MAIL, 'E-mail рассылка'),
    (NEYK, 'Отсутствует')
)

# тип клиента, choices
# Тип: физ лица, юр лицо, компании, НКО, НПО, фонд, банк, ОАО, ООО, ИП

IND = 'Физ лицо'
UR = 'Юр лицо'
COM = 'Компания'
OAO = 'ОАО'
OSO = 'ОсОО'
OOO = 'ООО'
INDP = 'ИП'
ZAO = 'ЗАО'
NKO = 'НКО'
NPO = 'НПО'
FOND = 'Фонд'
BANK = 'Банк'
NEYK = 'Отсутствует'

CLIENTTYPE = (
    (IND, 'Физ лицо'),
    (UR, 'Юр лицо'),
    (COM, 'Компания'),
    (OAO, 'ОАО'),
    (OSO, 'ОсОО'),
    (OOO, 'ООО'),
    (INDP, 'ИП'),
    (ZAO, 'ЗАО'),
    (NKO, 'НКО'),
    (NPO, 'НПО'),
    (FOND, 'Фонд'),
    (BANK, 'Банк'),
    (NEYK, 'Отсутствует')
)


class Client(models.Model):

    class Meta:
        ordering = ['name']
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        db_table = "client"
        index_together = (('id', 'slug'),)

    name = models.CharField(max_length=32, blank=False, default=None, verbose_name="ФИО")
    slug = models.SlugField(max_length=200, default='', db_index=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,16}$', message="Номер телефона должен быть в формате: '+700112299'. Макс. длинна = 16 знаков")
    phone_number = models.CharField(max_length=16, validators=[phone_regex], blank=True, verbose_name="Телефон")
    type = models.CharField(choices=CLIENTTYPE, default=CLIENTTYPE[12], max_length=16, blank=True, verbose_name="Тип")
    origin = models.CharField(choices=ORIGINS, default=ORIGINS[7], max_length=16, blank=True, verbose_name="Источник")
    email = models.EmailField(blank=True, verbose_name="Email")
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Создан")
    # когда будет создан app USERS - надо будет СВЯЗАТЬ с каждым товар\заказу\клиент создавшего USER
    created_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT, blank=True, default=1, verbose_name='Создавший')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')


    def __str__(self):
        return self.name