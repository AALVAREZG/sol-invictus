# Generated by Django 4.1.4 on 2022-12-30 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plotdata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
        migrations.AlterField(
            model_name='location',
            name='lon',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
    ]