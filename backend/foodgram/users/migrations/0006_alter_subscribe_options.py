# Generated by Django 3.2.19 on 2023-07-09 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230630_1206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscribe',
            options={'ordering': ('id',), 'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
    ]