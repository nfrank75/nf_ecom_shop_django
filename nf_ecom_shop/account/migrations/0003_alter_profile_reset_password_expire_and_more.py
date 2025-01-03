# Generated by Django 5.1.4 on 2024-12-27 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_profile_options_profile_createdat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='reset_password_expire',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='reset_password_token',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
