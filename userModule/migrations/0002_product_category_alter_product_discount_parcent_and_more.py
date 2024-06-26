# Generated by Django 4.2 on 2023-05-11 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userModule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='product_category',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('product_type', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_parcent',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
        migrations.CreateModel(
            name='product_subCategory',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('product_sub_category', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=300)),
                ('FK_product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userModule.product_category')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='FK_product_sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userModule.product_subcategory'),
        ),
    ]
