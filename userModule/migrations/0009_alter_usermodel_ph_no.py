# Generated by Django 4.2 on 2023-05-13 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userModule', '0008_alter_usermodel_email_alter_usermodel_ph_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='ph_No',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
