# Generated by Django 4.1.4 on 2023-08-20 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_app', '0007_alter_like_data_post_id_alter_like_data_user_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post_blog',
            name='update_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
