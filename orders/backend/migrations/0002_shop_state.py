# Generated by Django 2.1.5 on 2020-01-30 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='state',
            field=models.BooleanField(default=True, verbose_name='Статус получения заказов'),
        ),
    ]
