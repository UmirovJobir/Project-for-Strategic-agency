# Generated by Django 4.0.6 on 2022-09-21 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0006_rename_name_country_country_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code_product',
            field=models.BigIntegerField(unique=True),
        ),
    ]