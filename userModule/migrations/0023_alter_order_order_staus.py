# Generated by Django 4.2 on 2023-05-31 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userModule', '0022_alter_order_order_staus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_staus',
            field=models.CharField(choices=[('pending', 'pending'), ('order confirmed', 'order confirmed'), ('shipped', 'shipped'), ('out for delivery', 'out for delivery'), ('delivered', 'delivered'), ('cancellation', (('out for pickup', 'out for pickup'), ('cancelled', 'cancelled')))], default='panding', max_length=50),
        ),
    ]
