# Generated by Django 2.1.1 on 2018-09-07 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='series_year',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]