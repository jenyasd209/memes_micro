# Generated by Django 2.1.2 on 2018-11-19 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myUser', '0003_auto_20181117_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='count_comment',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='count_post',
            field=models.IntegerField(default=0),
        ),
    ]
