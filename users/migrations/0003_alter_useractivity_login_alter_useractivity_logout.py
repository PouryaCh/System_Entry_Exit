# Generated by Django 5.1 on 2024-08-21 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_useractivity_login_alter_useractivity_logout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='login',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='logout',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
