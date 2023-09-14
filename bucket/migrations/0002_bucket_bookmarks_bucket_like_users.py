# Generated by Django 4.2.5 on 2023-09-14 01:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bucket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucket',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='bookmark_buckets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bucket',
            name='like_users',
            field=models.ManyToManyField(blank=True, related_name='like_buckets', to=settings.AUTH_USER_MODEL),
        ),
    ]
