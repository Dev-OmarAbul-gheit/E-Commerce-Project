# Generated by Django 5.1.4 on 2025-01-29 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
