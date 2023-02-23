# Generated by Django 4.1 on 2022-09-18 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_blogpost_summ_bert'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='article',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='maltego_csv',
            field=models.FilePathField(blank=True, null=True, path='image/plots/maltego_csv/'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='rainette_explor',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='barplot',
            field=models.FilePathField(blank=True, null=True, path='image/plots/barplots/'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='wordcloud',
            field=models.FilePathField(blank=True, null=True, path='image/plots/wordclouds/'),
        ),
    ]
