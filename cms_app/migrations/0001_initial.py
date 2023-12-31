# Generated by Django 4.1.4 on 2023-08-20 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='info_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=8)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='like_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('post_id', models.CharField(max_length=100)),
                ('like_id', models.CharField(max_length=250)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='post_blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('content', models.CharField(max_length=50)),
                ('post_type', models.CharField(max_length=50)),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
