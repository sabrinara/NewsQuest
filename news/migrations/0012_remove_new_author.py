# Generated by Django 5.0.2 on 2024-04-15 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_alter_new_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new',
            name='author',
        ),
    ]
