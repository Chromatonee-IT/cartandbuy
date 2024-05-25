from django import template
from ..models import subcategory

register = template.Library()

@register.simple_tag
def get_subcategories():
    subcategories = subcategory.objects.all() 
    return subcategories


