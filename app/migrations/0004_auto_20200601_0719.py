# Generated by Django 3.0.6 on 2020-06-01 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200601_0710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pemesanan',
            name='keterangan',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
