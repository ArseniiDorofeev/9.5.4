from django import template

register = template.Library()


@register.filter
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр цензурирования применяется только к переменным строкового типа!")

    if value.lower() == "редиска":
        # Если значение равно "Редиска", заменяем все символы кроме первого на "*"
        first_char = value[0]
        censored_chars = '*' * (len(value) - 1)
        return first_char + censored_chars

    return value