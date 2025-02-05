from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Customer

@receiver(signal=post_save, sender= settings.AUTH_USER_MODEL)
def create_cutomer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Customer.objects.create(user=user)