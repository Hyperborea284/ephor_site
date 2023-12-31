# Generated by Django 4.2.5 on 2023-09-24 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0038_useraccesslog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccesslog',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='useraccesslog',
            name='external_ip',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='useraccesslog',
            name='internal_ip',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='useraccesslog',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='useraccesslog',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='useraccesslog',
            name='user_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
