# Generated by Django 3.0.4 on 2020-03-20 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logomaker', '0006_auto_20200321_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='mark_time',
            field=models.IntegerField(default=0),
        ),
    ]