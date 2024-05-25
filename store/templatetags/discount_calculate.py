from django import template
register = template.Library()

@register.filter(name='calculate_discount')
def calculate_discount(old_price,new_price):
    discount = (float(old_price) - float(new_price)) / float(old_price) * 100
    return f"{discount:.0f}"


@register.filter(name='multiply_by_20')
def multiply_by_20(value):
    return value * 20
