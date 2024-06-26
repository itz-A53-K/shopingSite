# Generated by Django 4.2 on 2023-05-31 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userModule', '0021_order_last_modified_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_staus',
            field=models.CharField(choices=[('panding', 'panding'), ('order confirmed', 'order confirmed'), ('shipped', 'shipped'), ('out for delivery', 'out for delivery'), ('delivered', 'delivered'), ('cancellation', (('out for pickup', 'out for pickup'), ('cancelled', 'cancelled')))], default='panding', max_length=50),
        ),
    ]
