# Generated by Django 4.2 on 2023-05-12 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userModule', '0006_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='ph_No',
            field=models.BigIntegerField(unique=True),
        ),
    ]
