from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import customer
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import base64
from django.contrib.auth.signals import user_logged_in,user_logged_out
from store.models import LastLogin
import re
from django.db.models.signals import Signal


@receiver(post_save, sender=User)
def send_staff_permission_email(sender, instance, **kwargs):
    cust_ins = customer.objects.filter(user=instance).first()
    if instance.is_staff and cust_ins.vendor_active_email == False:
        cust_ins.vendor_active_email = True
        cust_ins.save()
        subject = 'Vendor access has been  granted'
        from_email = settings.EMAIL_HOST_USER
        to_email = [instance.customer.email]
        # static_image_url = f"{settings.BASE_URL}{settings.STATIC_URL}/images/logo-blue.png"
        base_url = settings.BASE_URL
        html_content = render_to_string('vedor_access_granted_email.html', {'base_url':base_url,'instance': instance})
        email = EmailMultiAlternatives(subject, 'This is a plain text message.', from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()

@receiver(user_logged_in)
def update_last_login(sender, user, request, **kwargs):
    last_login, created = LastLogin.objects.get_or_create(user=user)
    user_agent_raw = request.META.get('HTTP_USER_AGENT', '')[:100]
    browser_name = user_agent_raw.split('(')[0].strip()
    pattern = r'\((.*?)\)'
    matches = re.findall(pattern, user_agent_raw)
    device_name = matches[0]
    last_login_ip = request.META.get('REMOTE_ADDR')
    last_login.last_login_ip = last_login_ip
    last_login.browser_name = str(browser_name)
    last_login.device_name = str(device_name)
    last_login.save()
