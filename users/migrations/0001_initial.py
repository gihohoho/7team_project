# Generated by Django 4.2.5 on 2023-09-14 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Username')),
                ('last_login', models.DateTimeField(auto_now=True, null=True, verbose_name='last login')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('mbti', models.CharField(blank=True, max_length=4, null=True)),
                ('tmi', models.TextField(blank=True, null=True)),
                ('blog', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
