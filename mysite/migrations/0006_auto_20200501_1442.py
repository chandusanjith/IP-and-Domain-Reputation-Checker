# Generated by Django 3.0.5 on 2020-05-01 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_auto_20200501_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='ips',
            name='IbmXForce',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='ips',
            name='Pysbil',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='ips',
            name='Sans',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='ips',
            name='VirusTotal',
            field=models.TextField(default=''),
        ),
    ]