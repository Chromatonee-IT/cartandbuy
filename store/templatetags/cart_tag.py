from django import template
from ..models import Cart,cartItems
from django.db.models import Count, Q, F, Case, When

register = template.Library()

@register.simple_tag
def get_cart(request):
    cart = Cart.objects.get(user=request) 
    cart_items = cartItems.objects.filter(cart_ins=cart)
    cart_total = 0
    for data in cart_items:
        cart_total += data.product.itm_new_price*data.cart_count
    return cart_items,cart_total
