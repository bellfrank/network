# Generated by Django 4.0.2 on 2022-03-20 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_remove_user_following_remove_user_followers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='user',
        ),
        migrations.DeleteModel(
            name='Followers',
        ),
        migrations.DeleteModel(
            name='Following',
        ),
    ]