# Generated by Django 3.2.13 on 2022-09-20 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0003_remove_product_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]
