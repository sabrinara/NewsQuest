# Generated by Django 5.0.2 on 2024-04-11 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_usernewspaperaccount_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usernewspaperaccount',
            name='image',
        ),
    ]
