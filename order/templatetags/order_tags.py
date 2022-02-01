from django import template

register = template.Library()


@register.filter(name='status_to_string')
def convert_status_to_string(value):
    if value == 1:
        return 'Обработка'
    if value == 2:
        return 'Оплачено'
    if value == 3:
        return 'Возврат'
    if value == 4:
        return 'Брак'
    if value == 5:
        return 'Просрочено'
    else:
        return f'Неизвестно {str(value)}'
