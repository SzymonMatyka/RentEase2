from django import template

register = template.Library()

@register.filter
def price_format(value):
    try:
        price = int(value)
        return f'{price:,}'.replace(',', ' ')
    except (ValueError, TypeError):
        return value
