from django import template
from client.models import CLIENTTYPE, ORIGINS

register = template.Library()


@register.filter(name='type_to_string')
def convert_type_to_string(value):
    if value == CLIENTTYPE[0][0]:
        return 'Физ лицо'
    if value == CLIENTTYPE[1][0]:
        return 'Юр лицо'
    if value == CLIENTTYPE[2][0]:
        return 'Компания'
    if value == CLIENTTYPE[3][0]:
        return 'ОАО'
    if value == CLIENTTYPE[4][0]:
        return 'ОсОО'
    if value == CLIENTTYPE[5][0]:
        return 'ООО'
    if value == CLIENTTYPE[6][0]:
        return 'ИП'
    if value == CLIENTTYPE[7][0]:
        return 'ЗАО'
    if value == CLIENTTYPE[8][0]:
        return 'НКО'
    if value == CLIENTTYPE[9][0]:
        return 'НПО'
    if value == CLIENTTYPE[10][0]:
        return 'Фонд'
    if value == CLIENTTYPE[11][0]:
        return 'Банк'
    if value == CLIENTTYPE[12][0]:
        return 'Отсутствует'
    else:
        return f'Неизвестно {str(value)}'


@register.filter(name='origin_to_string')
def convert_origin_to_string(value):
    if value == ORIGINS[0][0]:
        return 'Telegram'
    if value == ORIGINS[1][0]:
        return 'WhatsApp'
    if value == ORIGINS[2][0]:
        return 'Facebook'
    if value == ORIGINS[3][0]:
        return 'Instagram'
    if value == ORIGINS[4][0]:
        return 'Соцсети'
    if value == ORIGINS[5][0]:
        return 'Сарафанное радио'
    if value == ORIGINS[6][0]:
        return 'E-mail рассылка'
    if value == ORIGINS[7][0]:
        return 'Отсутствует'
    else:
        return f'Неизвестно {str(value)}'
