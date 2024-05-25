from django import template
from ..models import category

register = template.Library()

@register.simple_tag
def get_categories():
    categories = category.objects.all() 
    return categories
