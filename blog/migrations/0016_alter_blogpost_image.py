# Generated by Django 4.1 on 2022-09-07 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_blogpost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
    ]
