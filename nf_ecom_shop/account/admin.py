from django.contrib import admin
from .models import Profile


class ProfilAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'reset_password_token',
        'reset_password_expire',
        )

admin.site.register(Profile, ProfilAdmin)