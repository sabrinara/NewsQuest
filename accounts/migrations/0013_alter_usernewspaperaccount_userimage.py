# Generated by Django 5.0.2 on 2024-04-12 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_usernewspaperaccount_userimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernewspaperaccount',
            name='userImage',
            field=models.ImageField(blank=True, null=True, upload_to='accounts/static/profile_pic'),
        ),
    ]
