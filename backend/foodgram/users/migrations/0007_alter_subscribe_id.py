# Generated by Django 3.2.19 on 2023-07-09 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_subscribe_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribe',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
