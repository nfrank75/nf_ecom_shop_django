from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save



class Profile(models.Model):

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    reset_password_token = models.CharField(max_length=50, default="", blank=True)
    
    reset_password_expire = models.DateTimeField(null=True, blank=True)

    createdAt = models.DateTimeField(auto_now_add = True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-createdAt',)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):

    print('instance', instance)

    user = instance

    if created:
        profile = user.profile
        profile.save()
    

