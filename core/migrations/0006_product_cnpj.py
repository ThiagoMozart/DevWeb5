# Generated by Django 4.1.2 on 2022-12-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_product_date_registered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cnpj',
            field=models.CharField(default='70.878.917/0001-79', max_length=50),
            preserve_default=False,
        ),
    ]