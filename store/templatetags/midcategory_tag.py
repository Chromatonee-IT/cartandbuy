from django import template
from ..models import midcategory

register = template.Library()

@register.simple_tag
def get_midcategories():
    midcategories = midcategory.objects.all() 
    return midcategories


