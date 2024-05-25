from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver


@receiver(user_logged_out)
def handle_user_logout(sender, request, user, **kwargs):
  # Your custom logic here
  print(f"User '{user.username}' has logged out.")
